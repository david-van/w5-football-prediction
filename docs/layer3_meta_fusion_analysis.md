# Layer 3: 元学习融合层 — 深度分析

## 1. 当前实现：简单加权平均

项目代码中（`examples/full_pipeline.py:138`）的实现非常简单：

```python
baseline_weight = 0.3
consensus_weight = 0.7

final_prediction = {
    'home_win': baseline_weight * baseline['home_win'] + consensus_weight * consensus['home_win'],
    'draw':     baseline_weight * baseline['draw']     + consensus_weight * consensus['draw'],
    'away_win': baseline_weight * baseline['away_win']  + consensus_weight * consensus['away_win']
}
```

这就是一个固定权重的线性加权。问题很明显：

- 权重 0.3/0.7 是人工拍的，没有数据支撑
- 不管什么比赛场景，权重都一样
- 没有考虑 baseline 和 consensus 各自的置信度
- 没有考虑不同场景下谁更准（比如强弱分明时 baseline 可能更准，冷门场景 consensus 可能更准）

---

## 2. 论文描述的"神经网络融合层"是什么

根据 MODEL_CARD.md 和 gemini3_analysis.zh.md 的描述，生产环境的元学习融合层应该是一个 **Stacking（堆叠泛化）** 架构：

### 2.1 什么是 Stacking

Stacking 是集成学习的经典方法。核心思想：**用一个"元模型"来学习如何最优地组合多个"基模型"的预测结果**。

```
                    ┌─────────────────┐
                    │   最终预测输出    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │  元模型(Meta)    │  ← 这就是"元学习融合层"
                    │  (神经网络)      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────┴───┐  ┌──────┴──────┐  ┌───┴────────┐
     │ Layer 1    │  │ Layer 2     │  │ 额外特征    │
     │ baseline   │  │ consensus   │  │ (上下文)    │
     │ 预测概率   │  │ 预测概率    │  │            │
     └────────────┘  └─────────────┘  └────────────┘
```

### 2.2 元模型的输入（特征向量）

元模型不是直接看原始比赛数据，而是看 Layer 1 和 Layer 2 的**输出**，再加上一些上下文特征：

| 输入特征 | 来源 | 说明 |
|---|---|---|
| `baseline_home_win` | Layer 1 | 基线模型预测的主胜概率 |
| `baseline_draw` | Layer 1 | 基线模型预测的平局概率 |
| `baseline_away_win` | Layer 1 | 基线模型预测的客胜概率 |
| `consensus_home_win` | Layer 2 | 共识机制预测的主胜概率 |
| `consensus_draw` | Layer 2 | 共识机制预测的平局概率 |
| `consensus_away_win` | Layer 2 | 共识机制预测的客胜概率 |
| `consensus_confidence` | Layer 2 | 共识机制的整体置信度 |
| `agreement_score` | Layer 2 | Agent 之间的一致性分数 |
| `elo_diff` | 原始数据 | ELO 差值（反映实力差距） |
| `max_odds_prob` | 原始数据 | 赔率隐含的最大概率（市场确定性） |

### 2.3 元模型的结构

一个小型神经网络就够了（输入维度才 10 个左右）：

```
输入层 (10个特征)
    │
全连接层 (32 neurons, ReLU)
    │
Dropout (0.2)
    │
全连接层 (16 neurons, ReLU)
    │
Dropout (0.2)
    │
输出层 (3 neurons, Softmax)  →  [home_win_prob, draw_prob, away_win_prob]
```

或者更简单地，用一个逻辑回归/小型 XGBoost 也行。关键不在于模型复杂度，而在于**让数据来决定权重**。

---

## 3. 为什么需要神经网络而不是固定权重

### 3.1 不同场景下最优权重不同

| 比赛场景 | baseline 更准还是 consensus 更准 | 原因 |
|---|---|---|
| 强队主场 vs 弱队 | baseline 更准 | 统计规律明确，LLM 容易过度解读 |
| 实力接近的比赛 | consensus 更准 | 需要定性信息打破平衡 |
| 有重大伤病/停赛 | consensus 更准 | baseline 看不到伤病信息 |
| 赛季初（数据少） | consensus 更准 | baseline 特征不稳定 |
| 赛季末（保级/争冠） | consensus 更准 | 动机因素影响大，统计模型捕捉不到 |

固定 0.3/0.7 权重无法适应这些变化。神经网络可以学到：
- 当 `elo_diff > 300` 且 `agreement_score > 0.8` 时，更信任 baseline
- 当 `agreement_score < 0.5`（Agent 分歧大）时，降低 consensus 权重
- 当 `consensus_confidence` 很高但 baseline 预测相反时，可能是冷门信号

### 3.2 置信度校准

元模型还能做 **概率校准**（calibration）。比如：
- baseline 说主胜 70%，consensus 也说主胜 70% → 实际可能是 75%（两者一致时更可信）
- baseline 说主胜 70%，consensus 说客胜 60% → 实际可能是平局概率被低估了

这种非线性关系，固定权重捕捉不到。

---

## 4. 如何训练元模型

### 4.1 数据准备

需要一批**已知结果**的比赛，对每场比赛都跑过 Layer 1 和 Layer 2，记录它们的输出：

```csv
match_id, bl_home, bl_draw, bl_away, cs_home, cs_draw, cs_away, cs_conf, agree, elo_diff, odds_prob, actual_outcome
M001,     0.55,   0.25,   0.20,   0.50,   0.30,   0.20,   0.82,  0.75,  120,    0.58,    0
M002,     0.30,   0.35,   0.35,   0.25,   0.40,   0.35,   0.65,  0.45,  -15,    0.35,    1
...
```

### 4.2 训练流程

```python
import torch
import torch.nn as nn

class MetaFusionNet(nn.Module):
    def __init__(self, input_dim=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(16, 3),  # home_win, draw, away_win
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.net(x)

# 训练
model = MetaFusionNet()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    predictions = model(features)        # features: [batch, 10]
    loss = criterion(predictions, labels) # labels: [batch] (0/1/2)
    loss.backward()
    optimizer.step()
```

### 4.3 训练数据量要求

- 最少需要 **200-300 场**有完整 Layer 1 + Layer 2 输出的比赛
- 理想情况下 **500+ 场**
- 必须用时间分割（temporal split），不能随机分割，否则会数据泄露

---

## 5. 实际落地的务实方案

考虑到跑一次 Layer 2（5 个 LLM Agent × 2 轮辩论 = 10 次 API 调用）成本不低，建议分三步：

### 第一步：加权平均 + 动态权重（立刻可做，不需要训练数据）

```python
def dynamic_fusion(baseline, consensus, agreement_score, elo_diff):
    # 根据场景动态调整权重
    if abs(elo_diff) > 200 and agreement_score > 0.7:
        # 强弱分明且 Agent 一致 → 更信任 baseline
        bw, cw = 0.5, 0.5
    elif agreement_score < 0.4:
        # Agent 分歧大 → 降低 consensus 权重
        bw, cw = 0.6, 0.4
    else:
        # 默认
        bw, cw = 0.3, 0.7

    return {k: bw * baseline[k] + cw * consensus[k] for k in baseline}
```

### 第二步：逻辑回归/XGBoost 元模型（需要 100+ 场训练数据）

用 sklearn 的 LogisticRegression 或 XGBClassifier 做 stacking，简单有效：

```python
from sklearn.linear_model import LogisticRegression

meta_model = LogisticRegression(multi_class='multinomial')
meta_model.fit(meta_features, actual_outcomes)
```

### 第三步：神经网络元模型（需要 300+ 场训练数据）

当积累了足够多的 Layer 1 + Layer 2 输出后，训练上面的 MetaFusionNet。

---

## 6. 总结

| 方案 | 复杂度 | 数据需求 | 预期效果 |
|---|---|---|---|
| 当前：固定 0.3/0.7 | 最低 | 无 | 基础，无法适应场景变化 |
| 第一步：动态规则权重 | 低 | 无 | 比固定权重好，但规则是人工设计的 |
| 第二步：逻辑回归/XGBoost | 中 | 100+ 场 | 数据驱动，能学到场景差异 |
| 第三步：神经网络 | 高 | 300+ 场 | 最优，能捕捉非线性关系和概率校准 |

核心思想：**元学习融合层的价值不在于模型多复杂，而在于让数据来决定"什么时候该信谁"，而不是人工拍一个固定权重。**
