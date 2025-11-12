# Model Card: WINNER12 v1.0 - EPL Prediction Model

## Model Details

**Model Name**: WINNER12 Football Prediction Framework v1.0  
**Model Type**: Multi-Agent AI Consensus System with ML Baseline  
**Training Date**: 2025-11  
**Model Version**: 1.0  
**License**: MIT  

### Model Architecture

The WINNER12 framework combines traditional machine learning with large language model consensus:

1. **Baseline ML Models**:
   - XGBoost classifier
   - LightGBM classifier
   - Feature set: 50+ engineered features

2. **Multi-Agent LLM Layer**:
   - GPT-4 agent
   - Claude agent
   - Gemini agent
   - Debate-based consensus mechanism

3. **Meta-Learning Fusion**:
   - Intelligent synthesis of ML and LLM predictions
   - Confidence score calibration
   - Selective prediction strategy

## Intended Use

### Primary Use Cases

- **Academic Research**: Studying AI consensus mechanisms in sports prediction
- **Educational Purposes**: Teaching machine learning and multi-agent systems
- **Proof of Concept**: Demonstrating hybrid ML+LLM architectures

### Out-of-Scope Use Cases

- **Commercial Betting**: Not intended for gambling or betting applications
- **Financial Decisions**: Not financial or investment advice
- **Real-Time Trading**: Not designed for high-frequency or automated betting

## Training Data

### Dataset

- **Source**: Football-Data.co.uk
- **League**: English Premier League (EPL)
- **Time Period**: 2015/16 - 2021/22 seasons
- **Total Matches**: 2,800
- **Features**: Match results, team statistics, odds, historical records

### Data Processing

- Team strength calculated from season-end rankings
- Home advantage factor derived from historical win rates
- Recent form computed from last 5 matches
- Head-to-head records aggregated

## Evaluation Data

### Validation Set

- **Time Period**: 2022/23 - 2024/25 seasons
- **Total Matches**: 760
- **Validation Type**: Out-of-time (temporal split)
- **No Data Leakage**: Model never saw validation data during training

## Performance Metrics

### Overall Performance (Validation Set)

| Metric | All Predictions | High-Confidence (≥0.75) |
|--------|----------------|------------------------|
| **Accuracy** | 43.3% | **80.1%** |
| **Precision** | 43.3% | 80.1% |
| **Recall** | 43.3% | 80.1% |
| **F1-Score** | 43.3% | 80.1% |
| **Coverage** | 100% | 31.1% |

### Performance by Scenario

| Scenario | Matches | Accuracy | Confidence Range |
|----------|---------|----------|-----------------|
| Strong Home vs Weak Away | 84 | 89.3% | 0.82 - 0.95 |
| Weak Home vs Strong Away | 84 | 77.4% | 0.78 - 0.92 |
| Other High-Confidence | 68 | 72.1% | 0.75 - 0.85 |

### Abstention Strategy

- **Abstention Rate**: 68.9% (524/760 matches)
- **Philosophy**: Prioritize quality over quantity
- **Threshold**: Confidence ≥0.75 for predictions

## Limitations

### Known Limitations

1. **Selective Prediction**: Model abstains from 69% of matches
   - Only predicts high-confidence scenarios
   - May miss profitable opportunities in uncertain matches

2. **Scenario Dependency**: Performance varies by match type
   - Excellent on clear strength differentials (89%)
   - Poor on evenly-matched teams (43%)

3. **External Factors Not Modeled**:
   - Player injuries and suspensions
   - Managerial changes
   - Emotional factors (derbies, rivalries)
   - Weather conditions
   - Referee bias

4. **Temporal Drift**: Team strength changes over time
   - Model requires periodic retraining
   - Historical patterns may not hold in future

5. **League-Specific**: Trained only on EPL
   - May not generalize to other leagues
   - Different leagues have different dynamics

### Failure Cases

The model performs poorly on:

- **Derby Matches**: Emotional intensity disrupts statistical patterns
- **End-of-Season Matches**: External motivations (relegation, European qualification)
- **Newly Promoted Teams**: Limited historical data
- **Mid-Season Form Changes**: Sudden improvements or declines

## Ethical Considerations

### Responsible Use

- **Not for Gambling**: This model is for research, not betting
- **Transparency**: All limitations are disclosed
- **No Guarantees**: Past performance doesn't guarantee future results

### Potential Misuse

- **Gambling Addiction**: Using this model for betting may lead to financial harm
- **Overconfidence**: 80% accuracy still means 20% failure rate
- **Data Bias**: Model reflects historical biases in football

### Fairness

- **No Discrimination**: Model doesn't use protected attributes
- **Equal Treatment**: All teams evaluated by same criteria
- **Transparent Criteria**: Ranking-based strength assessment

## Maintenance

### Update Schedule

| Component | Frequency | Last Update |
|-----------|-----------|-------------|
| Historical Data | Quarterly | 2025-11-12 |
| Model Retraining | Every 6 months | 2025-11-12 |
| Performance Metrics | Monthly | 2025-11-12 |

### Monitoring

- **Accuracy Tracking**: Monthly validation on recent matches
- **Drift Detection**: Monitoring for concept drift
- **Calibration Checks**: Ensuring confidence scores remain accurate

## Contact

- **Maintainer**: WINNER12 AI Research Team
- **Issues**: [GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues)
- **Research Inquiries**: Open an issue with tag `research`

---

*Model Card last updated: 2025-11-12*
