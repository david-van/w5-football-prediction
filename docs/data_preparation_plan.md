# W-5 框架 — 数据准备与特征工程方案

## 1. 历史数据需求：需要往前追溯

只用 2025-26 当季数据，开头几轮的特征计算会有严重的 **冷启动问题**：

| 特征 | 所需历史深度 | 原因 |
|---|---|---|
| ELO 等级分 | 至少 2-3 个赛季 | ELO 需要逐场迭代累积，初始值差异大 |
| form_l5 (近 5 场) | 至少上赛季后半段 | 新赛季前 5 轮无法计算 |
| avg_goals_l10 (近 10 场) | 至少上赛季 | 新赛季前 10 轮数据不足 |
| H2H 交锋 | 3-5 个赛季 | 德甲两队每赛季只交手 2 次，需要累积 |

**建议**：从 football-data.co.uk 下载德甲 2022-23、2023-24、2024-25 三个赛季的 D1.csv，拼接后使用。

---

## 2. home_advantage 的计算

demo 数据里 `home_advantage` 是 0.5~0.7 的浮点数，有三种计算思路：

### 方案 A：赔率隐含概率（推荐，数据现成）

D1.csv 里已经有多家博彩赔率，可以直接算：

```python
# 用市场平均赔率的隐含概率
home_implied = 1 / AvgH
away_implied = 1 / AvgA
draw_implied = 1 / AvgD

# 去除超额赔付后，主队隐含胜率即可作为 home_advantage 的代理
total = home_implied + away_implied + draw_implied
home_advantage = home_implied / total
```

这个最好，因为赔率本身就是市场对实力+主场优势的综合定价。

### 方案 B：统计主场胜率

```python
# 该队最近 N 个主场比赛的胜率
home_wins = 最近20个主场中赢的场次
home_advantage = home_wins / 20
```

### 方案 C：主客场表现差

```python
# 主场场均得分 vs 客场场均得分的差值归一化
home_advantage = sigmoid(home_avg_goals - away_avg_goals)
```

**推荐**：方案 A + B 结合 — 赔率隐含概率反映市场共识，统计胜率反映球队自身主场属性。

---

## 3. D1.csv 额外数据的使用规划

### 路线一：喂给 ML 基线模型（作为量化特征）

```
原始比赛统计 → 滚动窗口聚合 → 新特征

shots_efficiency_l10     = HST_l10 / HS_l10          # 近10场射正率
defensive_pressure_l10   = AF_l10 / 90               # 场均被犯规(被压迫度)
corner_dominance_l10     = HC_l10 / (HC_l10+AC_l10)   # 角球占比(攻击压迫度)
discipline_risk_l10      = (HY*1 + HR*3)_l10 / 10    # 纪律风险指数
first_half_strength_l10  = HTHG_l10 / FTHG_l10       # 上半场进球占比(先发制人能力)
```

这些滚动特征和现有的 form、goals 特征一起送入 XGBoost/LightGBM。

### 路线二：喂给 AI Agent（作为定性/定量上下文）

```python
qualitative_context = f"""
市场赔率共识：
  - Bet365: 主胜{B365H} 平{B365D} 客胜{B365A}
  - 市场最高赔率: 主{MaxH} 平{MaxD} 客{MaxA}
  - 亚盘让球: {AHh} 球

近期比赛风格（主队近10场）：
  - 场均射门 {HS_avg:.1f}，射正率 {HST_avg/HS_avg:.0%}
  - 场均角球 {HC_avg:.1f}，场均犯规 {HF_avg:.1f}
  - 黄牌 {HY_avg:.1f}/场，红牌 {HR_sum} 张

近期比赛风格（客队近10场）：
  - ...同上...
"""
```

赔率数据给 **Sentiment Analyst**，比赛统计给 **Tactician** 和 **Statistician**。

---

## 总结：完整数据处理流程

```
D1.csv (多赛季)
│
├─→ 预处理脚本
│   ├─ 计算 ELO (逐场累积)
│   ├─ 计算滚动特征 (form, goals, shots, corners, cards...)
│   ├─ 计算 H2H 交锋统计
│   ├─ 计算 home_advantage (赔率+统计)
│   └─ 输出: features.csv (W-5格式)
│
├─→ Layer 1: XGBoost/LightGBM 训练 + 预测
│
└─→ Layer 2: 构造 match_context
    ├─ quantitative_features: 从 features.csv
    └─ qualitative_context: 赔率 + 比赛风格统计 → 文本化
```
