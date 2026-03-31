# W-5 数据处理方案：从原始 D1 数据到量化特征

## Context

当前项目已有 5 个赛季的德甲原始数据（`data/D1/D1_2122.csv` ~ `D1_2526.csv`），以及 demo 格式的特征数据（`data/sample/demo_matches.csv`）。现有 `FeatureEngineering` 类只有骨架方法，无法直接处理 D1 原始数据。需要实现完整的特征工程 pipeline，将 D1 原始 CSV 转换为模型可用的量化特征。

---

## 输入/输出规格

### 输入

- `data/D1/D1_2122.csv` ~ `D1_2526.csv`（5 个赛季，共约 1469 场比赛）
- 核心字段：`Date, HomeTeam, AwayTeam, FTHG, FTAG, FTR, HTHG, HTAG, HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR` + 赔率字段（`AvgH, AvgD, AvgA` 等）
- 不同赛季的列数不同（106~141 列），但上述核心字段在所有赛季中均存在

### 输出

- `data/D1/features.csv` — 与 `demo_matches.csv` 格式对齐的量化特征表

### 输出字段清单

| 字段 | 来源 | 说明 |
|---|---|---|
| `match_id` | 生成 | 格式 `D1_YYYYMMDD_Home_Away` |
| `date` | `Date` | 标准化为 `YYYY-MM-DD` |
| `season` | 文件名 | 赛季标识 `2122` / `2223` / `2324` / `2425` / `2526` |
| `home_team` | `HomeTeam` | 主队名称 |
| `away_team` | `AwayTeam` | 客队名称 |
| **ELO 特征** | | |
| `home_elo` | 计算 | 主队赛前 ELO 等级分 |
| `away_elo` | 计算 | 客队赛前 ELO 等级分 |
| `elo_diff` | 计算 | `home_elo - away_elo` |
| **近况特征** | | |
| `home_form_l5` | 计算 | 主队近 5 场综合胜率（win=1, draw=0.5, loss=0） |
| `away_form_l5` | 计算 | 客队近 5 场综合胜率 |
| `home_form_l5_home` | 计算 | 主队近 5 个**主场**胜率 |
| `away_form_l5_away` | 计算 | 客队近 5 个**客场**胜率 |
| **进球特征** | | |
| `home_avg_goals_l10` | 计算 | 主队近 10 场场均进球 |
| `away_avg_goals_l10` | 计算 | 客队近 10 场场均进球 |
| `home_avg_conceded_l10` | 计算 | 主队近 10 场场均失球 |
| `away_avg_conceded_l10` | 计算 | 客队近 10 场场均失球 |
| **H2H 特征** | | |
| `h2h_home_wins` | 计算 | 历史交锋中该主队的胜率 |
| `h2h_draws` | 计算 | 历史交锋平局率 |
| `h2h_away_wins` | 计算 | 历史交锋中该客队的胜率 |
| `h2h_total_matches` | 计算 | 历史交锋总场次（最多追溯 10 场） |
| **主场优势** | | |
| `home_advantage` | 计算 | 赔率隐含概率(60%) + 统计主场胜率(40%) 混合值 |
| **扩展统计特征** | | |
| `home_shots_efficiency_l10` | 计算 | 主队近 10 场射正率 `sum(HST) / sum(HS)` |
| `away_shots_efficiency_l10` | 计算 | 客队近 10 场射正率 `sum(AST) / sum(AS)` |
| `home_corner_dominance_l10` | 计算 | 主队近 10 场角球占比 `sum(HC) / sum(HC+AC)` |
| `away_corner_dominance_l10` | 计算 | 客队近 10 场角球占比 |
| `home_discipline_risk_l10` | 计算 | 主队近 10 场纪律风险 `sum(Y*1 + R*3) / N` |
| `away_discipline_risk_l10` | 计算 | 客队近 10 场纪律风险 |
| `home_first_half_strength_l10` | 计算 | 主队近 10 场上半场进球占比 `sum(HTG) / sum(FTG)` |
| `away_first_half_strength_l10` | 计算 | 客队近 10 场上半场进球占比 |
| `home_defensive_pressure_l10` | 计算 | 主队近 10 场场均被对手犯规数 |
| `away_defensive_pressure_l10` | 计算 | 客队近 10 场场均被对手犯规数 |
| **目标变量** | | |
| `outcome` | `FTR` | 0=主胜(H), 1=平(D), 2=客胜(A) |

---

## 实现方案

### 文件结构

```
新建：src/data/feature_pipeline.py     ← 核心特征工程模块
新建：scripts/build_features.py        ← 命令行入口（支持全量/增量两种模式）
修改：src/data/loader.py               ← 适配 features.csv 加载
生成：data/D1/features.csv             ← 输出的量化特征文件
生成：data/D1/pipeline_state.json      ← 增量更新所需的中间状态快照
```

### 核心模块：`src/data/feature_pipeline.py`

包含 6 个类，各自职责单一：

---

#### 1. `RawDataLoader` — 原始数据加载与拼接

**职责**：将 5 个赛季的 CSV 加载为一个统一的 DataFrame

**处理逻辑**：
- 扫描 `data/D1/` 下所有 `D1_*.csv` 文件
- 从文件名提取赛季标识（如 `D1_2122.csv` → `season='2122'`）
- 只保留核心列（比赛信息 + 比赛统计 + 赔率均值），丢弃各博彩公司的明细赔率列
- 统一日期格式：原始为 `dd/mm/yyyy`，转为 `datetime` 对象
- 处理 BOM 头（`D1_2526.csv` 有 UTF-8 BOM）
- 按日期升序排列，`reset_index`

**保留的列**：
```
Date, HomeTeam, AwayTeam,
FTHG, FTAG, FTR, HTHG, HTAG, HTR,
HS, AS, HST, AST, HF, AF, HC, AC, HY, AY, HR, AR,
AvgH, AvgD, AvgA, AHh,
season
```

---

#### 2. `EloCalculator` — ELO 等级分计算

**职责**：逐场迭代计算每支球队的 ELO 等级分

**算法**：
```
初始化：所有球队 ELO = 1500
K 因子 = 32
主场修正 = 100（计算期望胜率时，主队 rating + 100）

对每场比赛（按时间顺序）：
  1. 记录赛前 ELO → home_elo, away_elo（用于特征列）
  2. 计算期望胜率：
     E_home = 1 / (1 + 10^((away_elo - home_elo - 100) / 400))
     E_away = 1 - E_home
  3. 确定实际得分：
     主胜 → S_home=1, S_away=0
     平局 → S_home=0.5, S_away=0.5
     客胜 → S_home=0, S_away=1
  4. 更新 ELO：
     home_elo_new = home_elo + K * (S_home - E_home)
     away_elo_new = away_elo + K * (S_away - E_away)
  5. elo_diff = home_elo - away_elo（赛前值）
```

**冷启动**：新出现的球队（升级队）自动获得初始 ELO 1500

**跨赛季**：ELO 在赛季边界不重置，连续累积

---

#### 3. `RollingFeatureCalculator` — 滚动窗口特征计算

**职责**：为每场比赛计算主客双方的历史滚动统计特征

**核心原则**：
- **严格使用赛前数据**：只使用该场比赛之前的数据，绝不包含当场结果（防止数据泄漏）
- **跨赛季连续**：滚动窗口不在赛季边界截断
- **冷启动处理**：不足 N 场时用已有场次计算；不足 2 场时填默认值

**需要为每场比赛的主队和客队分别计算以下内容**：

对于一场比赛的某支球队，首先找到该队此前所有比赛记录（该队可能是主队也可能是客队），然后：

##### A. 近况 form（窗口=5）

```
取该队最近 5 场比赛：
- 对每场：该队赢 → 1.0，平 → 0.5，输 → 0.0
- form = mean(上述得分)
- 默认值：0.5

分主客场 form（窗口=5）：
- home_form_l5_home：该队最近 5 个主场比赛的 form
- away_form_l5_away：该队最近 5 个客场比赛的 form
```

**判断胜负的逻辑**（因为该队可能作为主队也可能作为客队出现）：
```
如果该队是 HomeTeam 且 FTR='H' → 赢
如果该队是 AwayTeam 且 FTR='A' → 赢
如果 FTR='D' → 平
否则 → 输
```

##### B. 进球统计（窗口=10）

```
取该队最近 10 场比赛：
- 如果该队是 HomeTeam：进球=FTHG，失球=FTAG
- 如果该队是 AwayTeam：进球=FTAG，失球=FTHG
- avg_goals = mean(进球)
- avg_conceded = mean(失球)
- 默认值：avg_goals=1.3, avg_conceded=1.3
```

##### C. 扩展统计特征（窗口=10）

以下每项均取该队最近 10 场的统计，注意**主客场字段映射**：

| 特征 | 公式 | 说明 | 默认值 |
|---|---|---|---|
| 射正率 | `sum(该队射正) / sum(该队射门)` | 射门=0 时返回 0 | 0.33 |
| 角球占比 | `sum(该队角球) / sum(双方角球)` | 双方=0 时返回 0.5 | 0.5 |
| 纪律风险 | `sum(该队黄牌*1 + 该队红牌*3) / N` | 场均加权犯规 | 1.5 |
| 上半场进球占比 | `sum(该队半场进球) / sum(该队全场进球)` | 全场=0 时返回 0.5 | 0.5 |
| 被犯规数 | `sum(对手犯规数) / N` | 场均被对手犯规次数 | 12.0 |

**字段映射表**（该队作为主队 vs 客队时使用不同列）：

| 统计项 | 该队是 HomeTeam | 该队是 AwayTeam |
|---|---|---|
| 该队射门 | `HS` | `AS` |
| 该队射正 | `HST` | `AST` |
| 该队角球 | `HC` | `AC` |
| 对手角球 | `AC` | `HC` |
| 该队黄牌 | `HY` | `AY` |
| 该队红牌 | `HR` | `AR` |
| 该队半场进球 | `HTHG` | `HTAG` |
| 该队全场进球 | `FTHG` | `FTAG` |
| 对手犯规 | `AF` | `HF` |

---

#### 4. `H2HCalculator` — 历史交锋计算

**职责**：计算每场比赛中两队的历史交锋统计

**算法**：
```
对每场比赛 (home=A, away=B)：
  1. 在此前所有比赛中查找 A vs B 的记录（包含 A 主场 vs B 和 B 主场 vs A）
  2. 取最近 10 场交锋
  3. 统计从"当前主队 A"的视角：
     - A 在交锋中赢的场次（A 为主队时 FTR='H'，或 A 为客队时 FTR='A'）
     - 平局场次（FTR='D'）
     - A 输的场次
  4. 输出比率：h2h_home_wins, h2h_draws, h2h_away_wins, h2h_total_matches
  5. 无交锋记录时返回 (0.33, 0.33, 0.33, 0)
```

---

#### 5. `HomeAdvantageCalculator` — 主场优势

**职责**：为每场比赛计算一个 0~1 的主场优势系数

**方案**：赔率隐含概率 (60%) + 统计主场胜率 (40%) 混合

##### 赔率部分（权重 0.6）
```
使用原始数据中的 AvgH, AvgD, AvgA（市场平均赔率）：
home_implied = (1 / AvgH) / (1/AvgH + 1/AvgD + 1/AvgA)

解释：去除博彩公司超额赔付 (overround) 后的主队隐含胜率
优点：赔率是市场对"实力 + 主场优势"的综合定价，信息量最大
```

##### 统计部分（权重 0.4）
```
取该主队最近 20 个主场比赛：
home_stat = 主场胜场数 / 总主场比赛数

不足 20 场时用已有场次计算
不足 2 场时默认 0.45（德甲平均主场胜率约 45%）
```

##### 混合
```
如果赔率数据完整：
  home_advantage = 0.6 * home_implied + 0.4 * home_stat

如果赔率缺失（AvgH/AvgD/AvgA 任一为 NaN）：
  home_advantage = home_stat（退化为纯统计）
```

---

#### 6. `FeaturePipeline` — 主 Pipeline 编排

**职责**：串联以上所有计算器，支持全量构建和增量追加两种模式

```python
class FeaturePipeline:
    def run(self, data_dir='data/D1', output_path='data/D1/features.csv',
            mode='incremental'):
        state_path = os.path.join(data_dir, 'pipeline_state.json')

        if mode == 'incremental' and self._can_incremental(output_path, state_path):
            return self._run_incremental(data_dir, output_path, state_path)
        else:
            return self._run_full(data_dir, output_path, state_path)

    def _run_full(self, data_dir, output_path, state_path):
        # Step 1: 加载并拼接所有赛季的原始数据
        df = RawDataLoader().load_all(data_dir)

        # Step 2: 计算 ELO（依赖时间顺序，逐行迭代）
        elo_calc = EloCalculator()
        df = elo_calc.compute(df)

        # Step 3: 计算滚动特征（form, goals, 扩展统计）
        df = RollingFeatureCalculator().compute(df)

        # Step 4: 计算 H2H 交锋统计
        df = H2HCalculator().compute(df)

        # Step 5: 计算主场优势
        df = HomeAdvantageCalculator().compute(df)

        # Step 6: 生成 match_id, 标准化 outcome, 选择输出列
        df = self._finalize(df)

        # Step 7: 保存 features.csv
        df[OUTPUT_COLUMNS].to_csv(output_path, index=False)

        # Step 8: 保存 pipeline_state.json（供后续增量使用）
        self._save_state(state_path, df, elo_calc.ratings)

        return df

    def _run_incremental(self, data_dir, output_path, state_path):
        # Step 1: 加载状态 + 识别新比赛
        state = self._load_state(state_path)
        all_raw = RawDataLoader().load_all(data_dir)
        new_matches = all_raw[all_raw['date'] > state['last_match_date']]

        if new_matches.empty:
            print("No new matches found.")
            return None

        # Step 2: 从状态恢复各计算器，仅对新比赛计算特征
        # Step 3: 追加到 features.csv
        # Step 4: 更新 pipeline_state.json

        return new_df
```

---

## 增量更新机制

### 问题背景

当前赛季（2526）的数据 `D1_2526.csv` 会持续更新，每轮新比赛结果会追加到该文件中。如果每次都全量重算 1469+ 场比赛的特征，既浪费时间又不必要。需要一种增量更新机制：**只计算新增比赛的特征，追加到 `features.csv` 末尾**。

### 核心难点

ELO 和滚动特征依赖历史状态——要计算第 1470 场的特征，必须知道第 1469 场之后各队的 ELO、近况、交锋记录。因此需要保存一份**中间状态快照**。

### 方案：状态文件 + 增量追加

#### 新增文件：`data/D1/pipeline_state.json`

全量计算完成后，自动保存 pipeline 末尾状态：

```json
{
  "last_match_date": "2026-03-29",
  "total_matches": 1469,
  "elo_ratings": {
    "Bayern Munich": 1687,
    "Dortmund": 1623,
    "RB Leipzig": 1601,
    "...": "..."
  },
  "recent_matches": [
    {
      "date": "2026-03-29",
      "HomeTeam": "Bayern Munich",
      "AwayTeam": "Dortmund",
      "FTHG": 2, "FTAG": 1, "FTR": "H",
      "HTHG": 1, "HTAG": 0,
      "HS": 15, "AS": 8, "HST": 7, "AST": 3,
      "HF": 10, "AF": 14, "HC": 6, "AC": 3,
      "HY": 2, "AY": 3, "HR": 0, "AR": 0,
      "AvgH": 1.85, "AvgD": 3.6, "AvgA": 4.2
    }
  ]
}
```

**`recent_matches` 的范围**：保留每支球队最近 20 场比赛的原始记录（20 是所有滚动窗口中最大的：home_advantage 用 20 个主场）。由于德甲 18 支球队 x 20 场 = 最多 360 条记录（实际会有重叠，约 200~250 条），数据量很小。

#### 增量流程

```
scripts/build_features.py --mode incremental  （默认模式）

1. 检查 features.csv 和 pipeline_state.json 是否存在
   ├─ 都不存在 → 自动回退到全量模式
   └─ 都存在 → 进入增量模式

2. 加载原始数据（所有 D1_*.csv）

3. 与 pipeline_state.json 中的 last_match_date 对比
   ├─ 无新比赛 → 打印 "No new matches found" 并退出
   └─ 有新比赛 → 提取新增比赛列表

4. 从 pipeline_state.json 恢复状态：
   - ELO 字典 → EloCalculator
   - 近期比赛记录 → RollingFeatureCalculator / H2HCalculator / HomeAdvantageCalculator

5. 仅对新增比赛逐场计算特征（与全量模式使用相同的计算逻辑）

6. 将新特征行追加到 features.csv 末尾

7. 更新 pipeline_state.json（新的 ELO、新的 recent_matches）
```

#### 命令行接口

```
# 增量更新（默认，自动检测新比赛）
python scripts/build_features.py

# 强制全量重算（覆盖已有 features.csv）
python scripts/build_features.py --mode full

# 指定路径
python scripts/build_features.py --data-dir data/D1 --output data/D1/features.csv
```

#### 一致性保障

| 场景 | 处理方式 |
|---|---|
| `features.csv` 存在但 `pipeline_state.json` 丢失 | 回退全量重算，重新生成两个文件 |
| `pipeline_state.json` 存在但 `features.csv` 丢失 | 回退全量重算 |
| 原始 CSV 中历史数据被修改（比如更正了比分错误） | 增量模式无法感知 → 需用户手动 `--mode full` |
| 新赛季 CSV 文件出现（如未来的 `D1_2627.csv`） | 增量模式自动识别其中的新比赛并处理 |
| `D1_2526.csv` 中间行被修改（非末尾追加） | 增量模式只看日期新于 `last_match_date` 的行，不处理中间修改 → 需 `--mode full` |

#### 性能对比

| 模式 | 处理量 | 预计耗时 |
|---|---|---|
| 全量 | ~1469 场 | 数秒（纯 Python 计算，无 IO 瓶颈） |
| 增量 | 每轮 9 场（德甲单轮） | < 1 秒 |

> 注：即使全量重算也很快（纯 pandas 计算，无 API 调用），增量模式的核心价值在于**避免覆盖**，保证 `features.csv` 的稳定性，以及支持自动化定期更新的工作流。

---

### 命令行入口：`scripts/build_features.py`

```
用法：
  python scripts/build_features.py                              # 增量更新（默认）
  python scripts/build_features.py --mode full                  # 全量重算
  python scripts/build_features.py --data-dir data/D1 --output data/D1/features.csv

参数：
  --data-dir   原始 CSV 所在目录（默认 data/D1）
  --output     输出特征文件路径（默认 data/D1/features.csv）
  --mode       运行模式：incremental（默认）| full（强制全量）
```

### 修改：`src/data/loader.py`

- 更新 `MatchDataLoader`，使其能加载 `features.csv`（列名与 `demo_matches.csv` 兼容）
- 将 `FeatureEngineering` 类的骨架方法指向 `feature_pipeline` 中的实际实现

---

## 关键设计决策

| # | 决策 | 原因 |
|---|---|---|
| 1 | **数据泄漏防护** — 所有特征只用赛前数据 | 防止模型训练时使用未来信息，这是预测任务的根本要求 |
| 2 | **冷启动不丢弃** — 数据不足时用已有数据计算+默认值填充 | 保留更多训练样本；模型可以学到"数据不足时特征趋近默认值"的模式 |
| 3 | **ELO 从 1500 起步** — 不做赛季前预设 | 通过 2121 赛季的 306 场比赛自然收敛，避免人工干预 |
| 4 | **跨赛季连续计算** — ELO/form 不在赛季边界重置 | 球队实力在赛季间是连续的，赛季边界不应产生断裂 |
| 5 | **升降级自动处理** — 新球队获默认值 | 新升级球队获得 ELO=1500 和默认特征值，随后通过比赛自然调整 |
| 6 | **赔率+统计混合主场优势** — 60/40 权重 | 赔率包含市场共识信息量大；统计反映球队个体主场属性；两者互补 |

---

## 数据质量注意事项

1. **日期格式**：D1 原始数据为 `dd/mm/yyyy`，需要正确 parse（不能用默认的美式日期）
2. **BOM 头**：`D1_2526.csv` 含 UTF-8 BOM（`\ufeff`），需要用 `encoding='utf-8-sig'` 读取
3. **赔率列名差异**：不同赛季的博彩公司列不同，但 `AvgH/AvgD/AvgA` 在所有赛季均存在
4. **球队名一致性**：检查同一球队在不同赛季是否有拼写变化（如 `M'gladbach` vs `Gladbach`）
5. **缺失值**：个别比赛可能缺少部分统计数据，需要在滚动计算中妥善处理

---

## 验证清单

| # | 验证项 | 预期 |
|---|---|---|
| 1 | `features.csv` 行数 | = 输入比赛总数（~1469 行） |
| 2 | 无 NaN 值 | 所有字段均有值（冷启动有默认值填充） |
| 3 | ELO 范围 | 约 1300~1700（合理区间） |
| 4 | form 值 | [0, 1] 范围内 |
| 5 | 射正率 | [0, 1] 范围内 |
| 6 | 角球占比 | [0, 1] 范围内 |
| 7 | h2h 三项之和 | ≈ 1.0（允许浮点误差） |
| 8 | home_advantage | [0, 1] 范围内 |
| 9 | outcome 分布 | 0/1/2 三类，比例大致合理（主胜~45%, 平~25%, 客胜~30%） |
| 10 | 与 `demo_matches.csv` 列对齐 | 核心列名一致，可被 `BaselinePredictor` 直接使用 |
| 11 | 端到端测试 | 用 `BaselinePredictor` 加载 `features.csv` 成功训练并预测 |
