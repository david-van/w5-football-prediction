"""
Feature Engineering Pipeline

Transforms raw D1 CSV data (from football-data.co.uk) into quantified feature data
suitable for the W-5 baseline ML models.

Supports two modes:
- Full: recompute all features from scratch
- Incremental: only compute features for new matches, append to existing features.csv
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Output column order (aligned with demo_matches.csv)
# ---------------------------------------------------------------------------
OUTPUT_COLUMNS = [
    'match_id', 'date', 'season', 'home_team', 'away_team',
    # ELO
    'home_elo', 'away_elo', 'elo_diff',
    # Form
    'home_form_l5', 'away_form_l5',
    'home_form_l5_home', 'away_form_l5_away',
    # Goals
    'home_avg_goals_l10', 'away_avg_goals_l10',
    'home_avg_conceded_l10', 'away_avg_conceded_l10',
    # H2H
    'h2h_home_wins', 'h2h_draws', 'h2h_away_wins', 'h2h_total_matches',
    # Home advantage
    'home_advantage',
    # Extended stats
    'home_shots_efficiency_l10', 'away_shots_efficiency_l10',
    'home_corner_dominance_l10', 'away_corner_dominance_l10',
    'home_discipline_risk_l10', 'away_discipline_risk_l10',
    'home_first_half_strength_l10', 'away_first_half_strength_l10',
    'home_defensive_pressure_l10', 'away_defensive_pressure_l10',
    # Target
    'outcome',
]

# Columns we keep from the raw CSV
RAW_KEEP_COLUMNS = [
    'Date', 'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG',
    'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC',
    'HY', 'AY', 'HR', 'AR',
    'AvgH', 'AvgD', 'AvgA',
]

OUTCOME_MAP = {'H': 0, 'D': 1, 'A': 2}


# ===================================================================
# 1. RawDataLoader
# ===================================================================

class RawDataLoader:
    """Load and concatenate raw D1 CSV files into a single DataFrame."""

    def load_all(self, data_dir: str) -> pd.DataFrame:
        data_path = Path(data_dir)
        csv_files = sorted(data_path.glob('D1_*.csv'))
        if not csv_files:
            raise FileNotFoundError(f"No D1_*.csv files found in {data_dir}")

        frames = []
        for f in csv_files:
            season = self._extract_season(f.name)
            df = pd.read_csv(f, encoding='utf-8-sig')

            # Keep only the columns we need (some may be missing in certain seasons)
            keep = [c for c in RAW_KEEP_COLUMNS if c in df.columns]
            df = df[keep].copy()
            df['season'] = season
            frames.append(df)

        combined = pd.concat(frames, ignore_index=True)

        # Parse date
        combined['date'] = pd.to_datetime(combined['Date'], dayfirst=True)
        combined = combined.sort_values('date').reset_index(drop=True)

        # Fill missing numeric stats with 0
        stat_cols = ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC',
                     'HY', 'AY', 'HR', 'AR', 'HTHG', 'HTAG']
        for col in stat_cols:
            if col in combined.columns:
                combined[col] = pd.to_numeric(combined[col], errors='coerce').fillna(0).astype(int)

        return combined

    @staticmethod
    def _extract_season(filename: str) -> str:
        m = re.search(r'D1_(\d{4})', filename)
        return m.group(1) if m else 'unknown'


# ===================================================================
# 2. EloCalculator
# ===================================================================

class EloCalculator:
    """Compute ELO ratings iteratively across all matches."""

    def __init__(self, k_factor: float = 32, home_advantage: float = 100,
                 initial_rating: float = 1500):
        self.k = k_factor
        self.home_adv = home_advantage
        self.initial = initial_rating
        self.ratings: Dict[str, float] = {}

    def _get_rating(self, team: str) -> float:
        if team not in self.ratings:
            self.ratings[team] = self.initial
        return self.ratings[team]

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        home_elos = []
        away_elos = []

        for _, row in df.iterrows():
            home = row['HomeTeam']
            away = row['AwayTeam']

            h_elo = self._get_rating(home)
            a_elo = self._get_rating(away)

            # Record pre-match ELO
            home_elos.append(round(h_elo, 1))
            away_elos.append(round(a_elo, 1))

            # Expected scores (with home advantage)
            e_home = 1.0 / (1.0 + 10 ** ((a_elo - h_elo - self.home_adv) / 400))
            e_away = 1.0 - e_home

            # Actual scores
            result = row.get('FTR', '')
            if result == 'H':
                s_home, s_away = 1.0, 0.0
            elif result == 'D':
                s_home, s_away = 0.5, 0.5
            else:
                s_home, s_away = 0.0, 1.0

            # Update
            self.ratings[home] = h_elo + self.k * (s_home - e_home)
            self.ratings[away] = a_elo + self.k * (s_away - e_away)

        df = df.copy()
        df['home_elo'] = home_elos
        df['away_elo'] = away_elos
        df['elo_diff'] = df['home_elo'] - df['away_elo']
        return df


# ===================================================================
# 3. RollingFeatureCalculator
# ===================================================================

class RollingFeatureCalculator:
    """Compute rolling window features for each match."""

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        # Pre-build per-team history index for O(1) lookups
        # team_history[team] = list of (row_index, is_home) tuples in chronological order
        team_history: Dict[str, List[int]] = {}
        team_home_history: Dict[str, List[int]] = {}
        team_away_history: Dict[str, List[int]] = {}

        n = len(df)
        # Pre-allocate result arrays
        results = {col: np.full(n, np.nan) for col in [
            'home_form_l5', 'away_form_l5',
            'home_form_l5_home', 'away_form_l5_away',
            'home_avg_goals_l10', 'away_avg_goals_l10',
            'home_avg_conceded_l10', 'away_avg_conceded_l10',
            'home_shots_efficiency_l10', 'away_shots_efficiency_l10',
            'home_corner_dominance_l10', 'away_corner_dominance_l10',
            'home_discipline_risk_l10', 'away_discipline_risk_l10',
            'home_first_half_strength_l10', 'away_first_half_strength_l10',
            'home_defensive_pressure_l10', 'away_defensive_pressure_l10',
        ]}

        for i, row in df.iterrows():
            home = row['HomeTeam']
            away = row['AwayTeam']

            # Compute features using history BEFORE this match
            home_hist = team_history.get(home, [])
            away_hist = team_history.get(away, [])
            home_home_hist = team_home_history.get(home, [])
            away_away_hist = team_away_history.get(away, [])

            # --- Form ---
            results['home_form_l5'][i] = self._calc_form(df, home_hist, home, window=5)
            results['away_form_l5'][i] = self._calc_form(df, away_hist, away, window=5)
            results['home_form_l5_home'][i] = self._calc_form(df, home_home_hist, home, window=5)
            results['away_form_l5_away'][i] = self._calc_form(df, away_away_hist, away, window=5)

            # --- Goals ---
            h_goals, h_conceded = self._calc_goals(df, home_hist, home, window=10)
            a_goals, a_conceded = self._calc_goals(df, away_hist, away, window=10)
            results['home_avg_goals_l10'][i] = h_goals
            results['away_avg_goals_l10'][i] = a_goals
            results['home_avg_conceded_l10'][i] = h_conceded
            results['away_avg_conceded_l10'][i] = a_conceded

            # --- Extended stats ---
            h_ext = self._calc_extended_stats(df, home_hist, home, window=10)
            a_ext = self._calc_extended_stats(df, away_hist, away, window=10)
            results['home_shots_efficiency_l10'][i] = h_ext['shots_efficiency']
            results['away_shots_efficiency_l10'][i] = a_ext['shots_efficiency']
            results['home_corner_dominance_l10'][i] = h_ext['corner_dominance']
            results['away_corner_dominance_l10'][i] = a_ext['corner_dominance']
            results['home_discipline_risk_l10'][i] = h_ext['discipline_risk']
            results['away_discipline_risk_l10'][i] = a_ext['discipline_risk']
            results['home_first_half_strength_l10'][i] = h_ext['first_half_strength']
            results['away_first_half_strength_l10'][i] = a_ext['first_half_strength']
            results['home_defensive_pressure_l10'][i] = h_ext['defensive_pressure']
            results['away_defensive_pressure_l10'][i] = a_ext['defensive_pressure']

            # Update history AFTER computing features (no data leakage)
            team_history.setdefault(home, []).append(i)
            team_history.setdefault(away, []).append(i)
            team_home_history.setdefault(home, []).append(i)
            team_away_history.setdefault(away, []).append(i)

        df = df.copy()
        for col, arr in results.items():
            df[col] = arr
        return df

    @staticmethod
    def _calc_form(df: pd.DataFrame, hist_indices: List[int],
                   team: str, window: int = 5) -> float:
        if len(hist_indices) < 2:
            return 0.5
        recent = hist_indices[-window:]
        scores = []
        for idx in recent:
            row = df.iloc[idx]
            ftr = row['FTR']
            is_home = row['HomeTeam'] == team
            if (is_home and ftr == 'H') or (not is_home and ftr == 'A'):
                scores.append(1.0)
            elif ftr == 'D':
                scores.append(0.5)
            else:
                scores.append(0.0)
        return round(np.mean(scores), 4)

    @staticmethod
    def _calc_goals(df: pd.DataFrame, hist_indices: List[int],
                    team: str, window: int = 10) -> Tuple[float, float]:
        if len(hist_indices) < 2:
            return 1.3, 1.3
        recent = hist_indices[-window:]
        scored = []
        conceded = []
        for idx in recent:
            row = df.iloc[idx]
            if row['HomeTeam'] == team:
                scored.append(row['FTHG'])
                conceded.append(row['FTAG'])
            else:
                scored.append(row['FTAG'])
                conceded.append(row['FTHG'])
        return round(np.mean(scored), 4), round(np.mean(conceded), 4)

    @staticmethod
    def _calc_extended_stats(df: pd.DataFrame, hist_indices: List[int],
                             team: str, window: int = 10) -> Dict[str, float]:
        defaults = {
            'shots_efficiency': 0.33,
            'corner_dominance': 0.5,
            'discipline_risk': 1.5,
            'first_half_strength': 0.5,
            'defensive_pressure': 12.0,
        }
        if len(hist_indices) < 2:
            return defaults

        recent = hist_indices[-window:]
        shots = shots_on = 0
        corners_own = corners_total = 0
        yellow = red = 0
        ht_goals = ft_goals = 0
        opp_fouls = 0
        n = len(recent)

        for idx in recent:
            row = df.iloc[idx]
            is_home = row['HomeTeam'] == team
            if is_home:
                shots += row['HS']
                shots_on += row['HST']
                corners_own += row['HC']
                corners_total += row['HC'] + row['AC']
                yellow += row['HY']
                red += row['HR']
                ht_goals += row['HTHG']
                ft_goals += row['FTHG']
                opp_fouls += row['AF']
            else:
                shots += row['AS']
                shots_on += row['AST']
                corners_own += row['AC']
                corners_total += row['HC'] + row['AC']
                yellow += row['AY']
                red += row['AR']
                ht_goals += row['HTAG']
                ft_goals += row['FTAG']
                opp_fouls += row['HF']

        return {
            'shots_efficiency': round(shots_on / shots, 4) if shots > 0 else 0.0,
            'corner_dominance': round(corners_own / corners_total, 4) if corners_total > 0 else 0.5,
            'discipline_risk': round((yellow + red * 3) / n, 4),
            'first_half_strength': round(ht_goals / ft_goals, 4) if ft_goals > 0 else 0.5,
            'defensive_pressure': round(opp_fouls / n, 4),
        }


# ===================================================================
# 4. H2HCalculator
# ===================================================================

class H2HCalculator:
    """Compute head-to-head statistics for each match."""

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        n = len(df)
        h2h_hw = np.full(n, 0.33)
        h2h_d = np.full(n, 0.33)
        h2h_aw = np.full(n, 0.33)
        h2h_total = np.zeros(n, dtype=int)

        # Build matchup history: key = frozenset({teamA, teamB})
        # value = list of (index, home_team, away_team, FTR)
        matchup_history: Dict[frozenset, List[Tuple[int, str, str, str]]] = {}

        for i, row in df.iterrows():
            home = row['HomeTeam']
            away = row['AwayTeam']
            key = frozenset({home, away})

            hist = matchup_history.get(key, [])
            if len(hist) > 0:
                # Take up to last 10 encounters
                recent = hist[-10:]
                wins = draws = losses = 0
                for _, h_team, _, ftr in recent:
                    if ftr == 'D':
                        draws += 1
                    elif (h_team == home and ftr == 'H') or (h_team == away and ftr == 'A'):
                        # Current home team won this past encounter
                        wins += 1
                    else:
                        losses += 1
                total = len(recent)
                h2h_hw[i] = round(wins / total, 4)
                h2h_d[i] = round(draws / total, 4)
                h2h_aw[i] = round(losses / total, 4)
                h2h_total[i] = total

            # Record this match for future lookups
            matchup_history.setdefault(key, []).append(
                (i, home, away, row['FTR'])
            )

        df = df.copy()
        df['h2h_home_wins'] = h2h_hw
        df['h2h_draws'] = h2h_d
        df['h2h_away_wins'] = h2h_aw
        df['h2h_total_matches'] = h2h_total
        return df


# ===================================================================
# 5. HomeAdvantageCalculator
# ===================================================================

class HomeAdvantageCalculator:
    """Compute home advantage coefficient (odds + statistical blend)."""

    ODDS_WEIGHT = 0.6
    STAT_WEIGHT = 0.4
    DEFAULT_HOME_ADV = 0.45

    def compute(self, df: pd.DataFrame) -> pd.DataFrame:
        n = len(df)
        home_adv = np.full(n, self.DEFAULT_HOME_ADV)

        # Track each team's home match results
        team_home_results: Dict[str, List[float]] = {}

        for i, row in df.iterrows():
            home = row['HomeTeam']

            # --- Statistical part: recent 20 home matches ---
            home_results = team_home_results.get(home, [])
            if len(home_results) >= 2:
                recent = home_results[-20:]
                stat_val = np.mean(recent)
            else:
                stat_val = self.DEFAULT_HOME_ADV

            # --- Odds part ---
            avg_h = row.get('AvgH', np.nan)
            avg_d = row.get('AvgD', np.nan)
            avg_a = row.get('AvgA', np.nan)

            if pd.notna(avg_h) and pd.notna(avg_d) and pd.notna(avg_a) and avg_h > 0:
                imp_h = 1.0 / avg_h
                imp_d = 1.0 / avg_d
                imp_a = 1.0 / avg_a
                odds_val = imp_h / (imp_h + imp_d + imp_a)
                home_adv[i] = round(
                    self.ODDS_WEIGHT * odds_val + self.STAT_WEIGHT * stat_val, 4
                )
            else:
                home_adv[i] = round(stat_val, 4)

            # Update home results AFTER computing feature
            ftr = row.get('FTR', '')
            team_home_results.setdefault(home, []).append(
                1.0 if ftr == 'H' else (0.5 if ftr == 'D' else 0.0)
            )

        df = df.copy()
        df['home_advantage'] = home_adv
        return df


# ===================================================================
# 6. FeaturePipeline
# ===================================================================

class FeaturePipeline:
    """Orchestrate the full feature engineering pipeline."""

    def run(self, data_dir: str = 'data/D1',
            output_path: str = 'data/D1/features.csv',
            mode: str = 'incremental') -> pd.DataFrame:

        state_path = os.path.join(data_dir, 'pipeline_state.json')

        if mode == 'incremental' and self._can_incremental(output_path, state_path):
            return self._run_incremental(data_dir, output_path, state_path)
        else:
            if mode == 'incremental':
                print("[INFO] State/features files not found, falling back to full mode.")
            return self._run_full(data_dir, output_path, state_path)

    # ------------------------------------------------------------------
    # Full mode
    # ------------------------------------------------------------------

    def _run_full(self, data_dir: str, output_path: str,
                  state_path: str) -> pd.DataFrame:
        print("[1/7] Loading raw data...")
        raw_df = RawDataLoader().load_all(data_dir)
        print(f"      Loaded {len(raw_df)} matches from {raw_df['season'].nunique()} seasons.")

        print("[2/7] Computing ELO ratings...")
        elo_calc = EloCalculator()
        df = elo_calc.compute(raw_df)

        print("[3/7] Computing rolling features...")
        df = RollingFeatureCalculator().compute(df)

        print("[4/7] Computing H2H statistics...")
        df = H2HCalculator().compute(df)

        print("[5/7] Computing home advantage...")
        df = HomeAdvantageCalculator().compute(df)

        print("[6/7] Finalizing features...")
        df = self._finalize(df)

        print(f"[7/7] Saving to {output_path}...")
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        df[OUTPUT_COLUMNS].to_csv(output_path, index=False)

        # Save state for incremental updates
        self._save_state(state_path, raw_df, elo_calc.ratings)
        print(f"      State saved to {state_path}")
        print(f"      Done! {len(df)} rows written.")
        return df[OUTPUT_COLUMNS]

    # ------------------------------------------------------------------
    # Incremental mode
    # ------------------------------------------------------------------

    def _run_incremental(self, data_dir: str, output_path: str,
                         state_path: str) -> Optional[pd.DataFrame]:
        print("[1/5] Loading state and raw data...")
        state = self._load_state(state_path)
        raw_df = RawDataLoader().load_all(data_dir)

        last_date = pd.to_datetime(state['last_match_date'])
        new_matches_raw = raw_df[raw_df['date'] > last_date].copy()

        if new_matches_raw.empty:
            print("      No new matches found. features.csv is up to date.")
            return None

        print(f"      Found {len(new_matches_raw)} new matches.")

        # Reconstruct recent history from state
        recent_df = pd.DataFrame(state['recent_matches'])
        if not recent_df.empty:
            recent_df['date'] = pd.to_datetime(recent_df['date'])
            # Fill missing stat columns with 0
            for col in ['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC',
                         'HY', 'AY', 'HR', 'AR', 'HTHG', 'HTAG']:
                if col in recent_df.columns:
                    recent_df[col] = pd.to_numeric(recent_df[col], errors='coerce').fillna(0).astype(int)

        # Context = recent history + new matches (for rolling calculations)
        context_df = pd.concat([recent_df, new_matches_raw], ignore_index=True)
        context_df = context_df.sort_values('date').reset_index(drop=True)

        print("[2/5] Computing features for new matches...")
        # ELO: restore ratings and continue
        elo_calc = EloCalculator()
        elo_calc.ratings = {k: float(v) for k, v in state['elo_ratings'].items()}
        context_df = elo_calc.compute(context_df)

        # Rolling features on the whole context
        context_df = RollingFeatureCalculator().compute(context_df)
        context_df = H2HCalculator().compute(context_df)
        context_df = HomeAdvantageCalculator().compute(context_df)

        # Extract only new match rows
        new_start = len(recent_df)
        new_df = context_df.iloc[new_start:].copy()
        new_df = self._finalize(new_df)
        new_features = new_df[OUTPUT_COLUMNS]

        print(f"[3/5] Appending {len(new_features)} rows to {output_path}...")
        new_features.to_csv(output_path, mode='a', header=False, index=False)

        print("[4/5] Updating state...")
        # Build updated raw for state saving: old recent + new matches raw
        all_raw_for_state = pd.concat([recent_df, new_matches_raw], ignore_index=True)
        all_raw_for_state = all_raw_for_state.sort_values('date').reset_index(drop=True)
        self._save_state(state_path, all_raw_for_state, elo_calc.ratings)

        print(f"[5/5] Done! {len(new_features)} new rows appended.")
        return new_features

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _finalize(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        # Generate match_id
        df['match_id'] = df.apply(
            lambda r: f"D1_{r['date'].strftime('%Y%m%d')}_{r['HomeTeam']}_{r['AwayTeam']}",
            axis=1
        )
        # Standardize date format
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        # Rename teams
        df['home_team'] = df['HomeTeam']
        df['away_team'] = df['AwayTeam']
        # Map outcome
        df['outcome'] = df['FTR'].map(OUTCOME_MAP)
        return df

    @staticmethod
    def _can_incremental(output_path: str, state_path: str) -> bool:
        return os.path.exists(output_path) and os.path.exists(state_path)

    @staticmethod
    def _save_state(state_path: str, raw_df: pd.DataFrame,
                    elo_ratings: Dict[str, float]):
        # Collect each team's most recent 20 matches
        teams = set(raw_df['HomeTeam'].unique()) | set(raw_df['AwayTeam'].unique())
        recent_indices = set()
        for team in teams:
            team_mask = (raw_df['HomeTeam'] == team) | (raw_df['AwayTeam'] == team)
            team_rows = raw_df[team_mask].tail(20)
            recent_indices.update(team_rows.index.tolist())

        recent_df = raw_df.loc[sorted(recent_indices)].copy()

        # Convert to serializable format
        recent_records = []
        for _, row in recent_df.iterrows():
            record = {}
            for col in RAW_KEEP_COLUMNS:
                if col in row.index:
                    val = row[col]
                    if pd.isna(val):
                        record[col] = None
                    elif isinstance(val, (np.integer,)):
                        record[col] = int(val)
                    elif isinstance(val, (np.floating,)):
                        record[col] = float(val)
                    else:
                        record[col] = val
            # Include date as string and season
            record['date'] = row['date'].strftime('%Y-%m-%d') if hasattr(row['date'], 'strftime') else str(row['date'])
            if 'season' in row.index:
                record['season'] = row['season']
            recent_records.append(record)

        state = {
            'last_match_date': raw_df['date'].max().strftime('%Y-%m-%d') if hasattr(raw_df['date'].max(), 'strftime') else str(raw_df['date'].max()),
            'total_matches': len(raw_df),
            'elo_ratings': {k: round(v, 2) for k, v in elo_ratings.items()},
            'recent_matches': recent_records,
        }

        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _load_state(state_path: str) -> dict:
        with open(state_path, 'r', encoding='utf-8') as f:
            return json.load(f)
