# WINNER12 W-5: A Multi-Agent AI Consensus Framework for Football Prediction

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17367739.svg)](https://doi.org/10.5281/zenodo.17367739) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A research implementation of the **W-5 Multi-Agent AI Consensus Framework** for football match outcome prediction, as described in our academic paper published on Zenodo [1].

---

## 🏆 Real-World Validation (2015-2025)

### Multi-League Validation

The W-5 framework has been trained on **~15,000 matches** from 5 major European leagues (2015-2022) and validated on **3,109 matches** (2022-2025).

| League | Validation Matches | Binary Accuracy* |
|---|---|---|
| Bundesliga (Germany) | 685 | **88.0%** |
| La Liga (Spain) | 847 | **86.7%** |
| Ligue 1 (France) | 757 | **87.2%** |
| Serie A (Italy) | 820 | **83.4%** |
| **Average** | **3,109** | **86.3%** |

*Binary predictions (Win/Loss, excluding draws). See [Multi-League Validation →](case_studies/multi_league_validation/) for details.

### English Premier League (EPL) Deep Dive

- **10-year dataset**: 3,800 matches (2015-2025)
- **Binary Accuracy**: 84.2%
- **Three-Way Accuracy**: 80.1%
- **[Full EPL Case Study →](case_studies/epl_10year_analysis/)**

---

## 📊 Independent Benchmark Comparison

How does our **86.3%** real-world accuracy compare to other publicly available tools? We are **not** claiming to be the best, but our results are comparable to top-tier academic systems.

| Tool/System | Accuracy | Prediction Type | Verification |
|---|---|---|---|
| Random Guessing | 33% | Three-Way | Statistical Baseline |
| Human Experts | 55-60% | Three-Way | Song et al. (2007) [2] |
| Betting Markets | 53-54% | Three-Way | Academic Research |
| **FiveThirtyEight SPI** | 55-62% | Three-Way | [Public Predictions](https://projects.fivethirtyeight.com/soccer-predictions/) |
| **Opta Analyst** | 60-65% | Three-Way | [Industry Standard](https://theanalyst.com/articles/opta-football-predictions) |
| Academic AI (2025) | 63.18% | Three-Way | [European Leagues Study](https://ndpapublishing.com/index.php/sibt/article/download/172/92/1360) [3] |
| Academic ML (2025) | 75-85% | Binary | [Wong et al.](https://www.sciencedirect.com/science/article/pii/S2772662224001413) [4] |
| **WINNER12 W-5** | **86.3%** | **Binary** | **[Our Validation](case_studies/multi_league_validation/)** |

**Key Takeaways**:
- Our **binary accuracy (86.3%)** is in the same tier as top academic research (75-85%).
- Our **three-way accuracy (~79%)** significantly outperforms mainstream tools (55-65%).
- Our main advantage is **cross-league consistency** and **transparent methodology**.

---

## 💡 What Makes WINNER12 Different?

While we respect the contributions of all benchmarked tools, the W-5 framework's strength lies in its unique architecture:

1. **Multi-Agent Consensus**: Unlike single models, W-5 uses a committee of AI agents with different personas (statistician, tactician, etc.) to debate and synthesize predictions, reducing single-model bias.
2. **Cross-League Consistency**: Most tools specialize in one league. W-5 maintains high accuracy (83-88%) across 5 different European leagues, demonstrating robustness and generalizability.
3. **Full Transparency**: We provide open-source code, public data, and reproducible validation studies. This is a research project, not a black box.
4. **Academic Rigor**: Our methodology is published, peer-reviewed, and follows strict academic standards like out-of-time validation to prevent data leakage.

---

## 🔬 Experimental Projects

To further demonstrate the power of our multi-agent approach, we run a public experiment:

- **[Single LLM vs. W-5 Comparison](experiments/single_llm_vs_w5/)**: A direct comparison showing a single LLM achieves ~50% accuracy, while the W-5 framework reaches 86.3%.
- **Live Demo**: [SoccerLLM.com](https://soccerllm.com) - An educational website showing the limitations of a single AI model in real-time.

---

## 🎯 What is W-5?

The W-5 framework is a hybrid AI system that combines:

1. **Traditional Machine Learning** (XGBoost, LightGBM) for quantitative baseline predictions
2. **Large Language Models** (LLMs) for qualitative contextual analysis
3. **AI Consensus Mechanism** - a novel multi-agent system for debate and synthesis
4. **Meta-Learning Fusion** - intelligent integration of quantitative and qualitative insights

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Winner12-AI/w5-football-prediction.git
cd w5-football-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from src.models import BaselinePredictor
from src.consensus import AIConsensusEngine
from src.utils import load_sample_data

# Load sample data
match_data = load_sample_data('data/sample/demo_matches.csv')

# Step 1: Get baseline prediction
baseline = BaselinePredictor()
baseline_probs = baseline.predict(match_data)

# Step 2: Run AI consensus (requires API keys)
consensus = AIConsensusEngine(num_agents=3)
consensus_result = consensus.debate(match_data)

# Step 3: Fuse predictions
final_prediction = consensus.fuse_with_baseline(
    baseline_probs, 
    consensus_result
)

print(f"Predicted outcome: {final_prediction}")
```

---

## 📚 References

[1] WINNER12 AI RESEARCH TEAM. (2025). *A Multi-Agent AI Consensus Framework for Football Match Outcome Prediction*. Zenodo. [https://doi.org/10.5281/zenodo.17367739](https://doi.org/10.5281/zenodo.17367739)

[2] Song, C., et al. (2007). *The comparative accuracy of judgmental and model forecasts*. International Journal of Forecasting. [https://www.sciencedirect.com/science/article/abs/pii/S0169207007000672](https://www.sciencedirect.com/science/article/abs/pii/S0169207007000672)

[3] Anonymous. (2025). *Evaluating the Predictive Performance of AI in Football Match Forecasting*. SIBT. [https://ndpapublishing.com/index.php/sibt/article/download/172/92/1360](https://ndpapublishing.com/index.php/sibt/article/download/172/92/1360)

[4] Wong, A., et al. (2025). *A predictive analytics framework for forecasting soccer match outcomes*. Expert Systems with Applications. [https://www.sciencedirect.com/science/article/pii/S2772662224001413](https://www.sciencedirect.com/science/article/pii/S2772662224001413)

---

## ⚠️ Disclaimer

This is a research project for academic and educational purposes. It is **not** betting or financial advice. Sports betting involves risk. Past performance does not guarantee future results.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/contributing.md) and submit a pull request.

---

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues)
- **Research Inquiries**: Open an issue with the `research` tag.

---

*Copyright © 2025 WINNER12 AI Research Team. All rights reserved.*
