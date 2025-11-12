# Case Studies & Real-World Validations

This directory contains real-world validations of the WINNER12 W-5 Framework across multiple leagues and datasets.

---

## 📊 Available Case Studies

### 1. Multi-League Validation (2022-2025) ✅ NEW!

**Path**: [`multi_league_validation/`](multi_league_validation/)

**Summary**:
- **4 major European leagues**: Bundesliga, La Liga, Serie A, Ligue 1
- **3,109 matches** validated
- **Average accuracy**: 86.3% (binary predictions)
- **Validation period**: 2022-2025

**Key Findings**:
- Bundesliga: 88.0% (highest, due to clear hierarchy)
- La Liga: 86.7% (strong top-team dominance)
- Ligue 1: 87.2% (PSG dominance)
- Serie A: 83.4% (tactical complexity)

**[View Full Report →](multi_league_validation/)**

---

### 2. English Premier League 10-Year Analysis (2015-2025) ✅

**Path**: [`epl_10year_analysis/`](epl_10year_analysis/)

**Summary**:
- **3,800 EPL matches** analyzed
- **10-year dataset** (2015-2025)
- **Binary accuracy**: 84.2%
- **Three-way accuracy**: 80.1%

**Key Findings**:
- Debunked the myth: "No weak teams in EPL, beware of draws"
- Draws are actually the **least common** outcome (23.32%)
- Strong teams **dominate** weak teams (78.89% win rate at home)
- Home advantage is **significant** (44.50% vs 32.18%)

**[View Full Report →](epl_10year_analysis/)**

---

## 🎯 Validation Methodology

All case studies follow rigorous academic standards:

1. **Out-of-Time Validation**: Models trained on historical data, validated on future matches
2. **No Data Leakage**: Predictions made before match outcomes were known
3. **Authoritative Data**: All data sourced from [Football-Data.co.uk](https://www.football-data.co.uk)
4. **Transparent Metrics**: Complete performance breakdowns provided
5. **Reproducible**: All code and data available in respective directories

---

## 📈 Overall Performance Summary

| Validation | Matches | Period | Binary Accuracy | Three-Way Accuracy |
|------------|---------|--------|-----------------|-------------------|
| Multi-League | 3,109 | 2022-2025 | **86.3%** | - |
| EPL 10-Year | 3,800 | 2015-2025 | **84.2%** | **80.1%** |
| **Combined** | **6,909** | **2015-2025** | **85.7%** | **~80%** |

**Note**: Binary predictions (Win/Loss, excluding draws) are simpler than three-way predictions (Win/Draw/Loss).

---

## 🔬 Experimental Projects

### Single LLM vs W-5 Comparison

**Path**: [`../experiments/single_llm_vs_w5/`](../experiments/single_llm_vs_w5/)

**Purpose**: Demonstrate why single LLMs fail at football prediction

**Key Finding**: Single LLM achieves ~50% accuracy vs W-5's 86.3%

**Live Demo**: [SoccerLLM.com](https://soccerllm.com) - Educational experiment showing single LLM limitations

**[View Comparison →](../experiments/single_llm_vs_w5/)**

---

## 🤝 Contributing Case Studies

We welcome contributions of real-world case studies! If you've applied the WINNER12 framework to your own dataset, please consider sharing:

1. Fork this repository
2. Create a new directory under `case_studies/`
3. Include:
   - README with methodology and results
   - Data (or links to data sources)
   - Code/notebooks for reproducibility
   - Performance metrics
4. Submit a pull request

**Guidelines**:
- Use real, verifiable data sources
- Provide clear methodology
- Include performance metrics
- Document limitations
- Follow our [Contributing Guidelines](../docs/contributing.md)

---

## ⚠️ Important Disclaimers

### Research Purpose

These validations are for **academic and educational purposes**. The WINNER12 framework is a research project demonstrating multi-agent AI consensus mechanisms.

### Not Financial Advice

This is **not** betting or financial advice. Sports betting involves significant risk. Past performance does not guarantee future results.

---

## 📧 Contact

Questions about case studies? Open an [issue](https://github.com/Winner12-AI/w5-football-prediction/issues) with the `case-study` tag.

---

*Last updated: 2025-11-12*  
*Copyright © 2025 WINNER12 AI Research Team. All rights reserved.*
