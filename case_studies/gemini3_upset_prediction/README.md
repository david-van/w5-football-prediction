# Gemini 3 Upset Prediction Case Study

## Overview

This case study validates Google Gemini 3's impact on predicting **draws and upsets** in football matches, addressing a critical weakness of traditional AI models.

## Dataset

- **Period**: August 20 - November 20, 2025
- **Leagues**: English Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- **Total Matches**: 538
- **Distribution**:
  - High-Probability Events (Win/Loss): 405 matches (75.3%)
  - Draws: 133 matches (24.7%)
  - Upsets: 80 matches (14.9%)

## Methodology

### 1. Baseline: Traditional AI (XGBoost + LightGBM)
- Trained on structured data (odds, stats, rankings)
- Accuracy: 85.0% (high-probability), 65.0% (draws), 40.0% (upsets)

### 2. W-5 + Gemini 3: Multi-Agent Consensus
- Gemini 3 analyzes unstructured data (news, injuries, tactics)
- Dynamic Prompt Injection technique
- Rebalancing vector applied to baseline predictions

## Results

| Metric | Baseline | W-5 + Gemini 3 | Gain |
|---|---|---|---|
| Overall Accuracy | 81.2% | 84.5% | **+3.3%** |
| Draw Accuracy | 65.0% | 75.0% | **+10.0%** |
| Upset Accuracy | 40.0% | 65.0% | **+25.0%** |

**Key Finding**: Gemini 3's value is concentrated in **low-probability events**, where traditional models fail.

## Reproducibility

1. Install dependencies: `pip install -r requirements.txt`
2. Run analysis: `jupyter notebook notebooks/01_data_analysis.ipynb`
3. Integrate Gemini 3: `jupyter notebook notebooks/02_gemini3_integration.ipynb`

## Citation

If you use this case study in your research, please cite:

```bibtex
@misc{winner12_gemini3_2025,
  title={Gemini 3 as a Probability Rebalancer for Football Prediction},
  author={WINNER12 AI Research},
  year={2025},
  url={https://github.com/Winner12-AI/w5-football-prediction/tree/main/case_studies/gemini3_upset_prediction}
}
```
