# W-5 足球预测框架 — 数据流转分析

## 整体架构（三层流水线）

```
原始数据 → [Layer 1] 基线ML预测 → [Layer 2] AI共识辩论 → [Layer 3] 元学习融合 → 最终预测
```

---

## Layer 1: 基线 ML 预测（量化数据驱动）

### 所需数据

| 字段 | 说明 |
|---|---|
| `match_id` / `date` | 比赛标识与日期 |
| `home_team` / `away_team` | 主客队名称 |
| `home_elo` / `away_elo` / `elo_diff` | ELO 等级分及差值 |
| `home_form_l5` / `away_form_l5` | 近 5 场胜率（表现形态） |
| `home_avg_goals_l10` / `away_avg_goals_l10` | 近 10 场场均进球 |
| `home_avg_conceded_l10` / `away_avg_conceded_l10` | 近 10 场场均失球 |
| `h2h_home_wins` / `h2h_draws` / `h2h_away_wins` | 历史交锋胜/平/负比率 |
| `home_advantage` | 主场优势系数 |
| `outcome` | 结果标签 (0=主胜, 1=平, 2=客胜) |

### 两个基线模型

- **SimpleELOPredictor** (`src/models/baseline.py:211`): 基于 ELO 等级分差值 + 主场优势系数，直接计算三项概率
- **BaselinePredictor** (`src/models/baseline.py:20`): XGBoost + LightGBM 集成模型，需要用上述量化特征训练后预测

### 数据流

```
CSV → MatchDataLoader.load_matches()
    → FeatureEngineering(计算近况/交锋/进球统计)
    → BaselinePredictor.train()
    → predict_proba()
    → 输出 {home_win, draw, away_win} 概率
```

---

## Layer 2: AI 共识辩论机制（定性 + 定量）

### 所需数据（match_context 字典）

1. **`quantitative_features`** — 同上量化特征（ELO、近况、进球等）
2. **`qualitative_context`** — 非结构化文本信息，包括：
   - 近期球队新闻
   - 伤病/复出情况
   - 天气预报
   - 博彩市场情绪

### 5 个 AI Agent 角色

| Agent | 侧重数据 | LLM |
|---|---|---|
| Statistician（统计师） | 历史数据、统计趋势 | GPT-5.4 |
| Tactician（战术师） | 阵型、战术匹配 | Claude Opus 4.6 |
| Sentiment Analyst（舆情分析师） | 博彩赔率、社媒情绪 | Gemini 3.1 Pro |
| News Analyst（新闻分析师） | 伤病、士气、外部因素 | GPT-5.4 |
| Risk Assessor（风险评估师） | 不确定性、方差来源 | Claude Opus 4.6 |

### 辩论流程

```
Round 1: 各 Agent 独立分析 match_context + baseline预测
       → 各自输出概率/置信度/推理

Round 2+: 汇总同行分析
        → 加入 peer_analyses 上下文
        → 各 Agent 修正 (70%新 + 30%旧加权)

最终合成: 按置信度加权平均
        → consensus_prediction + agreement_score
```

---

## Layer 3: 元学习融合

当前实现为简单加权融合：

```
最终预测 = 0.3 × baseline预测 + 0.7 × consensus预测
```

> 论文中提到生产环境使用训练过的神经网络融合层

---

## 完整数据需求清单

```
必需数据：
├── 量化特征（结构化）
│   ├── ELO 等级分（主/客）
│   ├── 近 N 场胜率 (form)
│   ├── 近 N 场进球/失球均值
│   ├── 历史交锋统计 (H2H)
│   └── 主场优势系数
│
├── 定性信息（非结构化文本）
│   ├── 球队新闻/伤病报告
│   ├── 天气/场地状况
│   ├── 市场赔率/情绪
│   └── 战术/阵型信息
│
└── API Keys（LLM 服务）
    ├── OpenAI (GPT)
    ├── Anthropic (Claude)
    └── Google (Gemini)
```

## 核心思路

传统 ML 模型处理"硬数据"（量化特征），多个不同视角的 LLM Agent 处理"软数据"（新闻、情绪、战术等非结构化信息），然后通过辩论达成共识，最后融合两者得出最终预测。
