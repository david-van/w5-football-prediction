# Layer 2: AI 共识辩论机制 — 深度分析

## 1. 核心问题：非结构化数据从哪来？

W-5 框架的 Layer 2 需要两类输入：

| 输入类型 | 说明 | 当前状态 |
|---|---|---|
| `quantitative_features` | ELO、近况、进球等结构化数据 | D1.csv 可提供，需预处理 |
| `qualitative_context` | 新闻、伤病、战术、市场情绪等非结构化文本 | **当前是硬编码 mock 数据，管道是断的** |

项目代码中 `load_sample_data()` 返回的 `qualitative_context` 只是一段写死的示例文本，并没有实现真正的数据获取。这是从论文到可运行系统之间最大的 gap。

---

## 2. 五个 Agent 的信息获取策略

### 2.1 信息来源总览

| Agent | 角色 | 主要信息来源 | 是否需要搜索 |
|---|---|---|---|
| Statistician（统计师） | 量化数据分析 | D1.csv 量化特征 | 不需要，数据已有 |
| Tactician（战术师） | 战术分析 | 搜索阵型/战术 + D1.csv 风格推断 | **需要** |
| Sentiment Analyst（舆情分析师） | 市场情绪分析 | D1.csv 赔率 + 搜索市场情绪 | 可选，赔率数据已经很强 |
| News Analyst（新闻分析师） | 新闻/伤病分析 | 搜索新闻/伤病 | **需要，核心输入** |
| Risk Assessor（风险评估师） | 不确定性评估 | 其他 Agent 的分析结果 | 不太需要，偶尔辅助 |

### 2.2 各 Agent 详细分析

#### Statistician（统计师）— 不需要搜索

D1.csv 的量化特征（ELO、近况、进球、交锋）就是它的全部输入。这是五个 Agent 中数据最完备的一个。

#### Tactician（战术师）— 需要搜索

D1.csv 里没有阵型、控球率、传球数据。但可以从已有统计推断风格：

| D1.csv 字段 | 可推断的战术信息 |
|---|---|
| `HS` / `AS` (射门) | 进攻积极性 |
| `HST/HS` (射正率) | 进攻效率，可能是反击型 |
| `HC` / `AC` (角球) | 边路进攻强度 |
| `HF` / `AF` (犯规) | 逼抢强度，可能是高位压迫型 |

这只是粗略的风格画像。真正的阵型和战术数据需要通过 LLM 联网搜索获取（WhoScored、FotMob 等来源）。

#### Sentiment Analyst（舆情分析师）— 可选搜索

D1.csv 已有多家博彩赔率（B365、BW、PS 等）+ 亚盘 + 大小球，这些赔率本身就是市场对所有公开信息的综合定价，信息量很大。搜索可以补充社媒情绪，但不是必须的。

#### News Analyst（新闻分析师）— 必须搜索

伤病、停赛、球员状态、更衣室氛围 — 这些信息完全不在 CSV 数据里，只能从外部获取。这是最依赖搜索的 Agent。

#### Risk Assessor（风险评估师）— 主要做内部元分析

它的角色不是"找新信息"，而是对其他 4 个 Agent 的分析做元评估：
- 各 Agent 预测分歧大不大？
- 哪些因素增加了不确定性？
- 这场比赛是否属于"难以预测"的类型？

搜索可以辅助判断（赔率波动、天气等），但不是核心输入。

---

## 3. 非结构化数据的获取方案

### 方案一：从 D1.csv 已有数据"生成"（零成本，立刻可用）

将赔率和比赛统计文本化，构造 `qualitative_context`：

```python
qualitative_context = f"""
博彩市场共识:
  Bet365赔率: 主胜{B365H} 平{B365D} 客胜{B365A}
  市场平均: 主胜{AvgH} 平{AvgD} 客胜{AvgA}
  亚盘让球: {AHh}球
  大小球: 大2.5球赔率{Avg>2.5} / 小2.5球赔率{Avg<2.5}

主队近期风格（近10场）:
  场均射门 {HS_avg:.1f}，射正率 {HST_avg/HS_avg:.0%}
  场均角球 {HC_avg:.1f}，场均犯规 {HF_avg:.1f}
  黄牌 {HY_avg:.1f}/场，红牌 {HR_sum} 张

客队近期风格（近10场）:
  ...同上...
"""
```

### 方案二：LLM 联网搜索（开发成本最低）

让支持联网的 LLM 自行搜索，只需修改 prompt：

```
搜索: "{home_team} vs {away_team} preview injury lineup"
```

一次搜索返回的赛前分析文章，通常同时包含阵型、伤病、赔率信息，多个 Agent 各取所需。

### 方案三：调用外部 API（最可控）

| 数据类型 | 数据源 | 获取方式 | 成本 |
|---|---|---|---|
| 球队新闻 | NewsAPI / Google News | REST API | 免费/低价 |
| 伤病停赛 | Transfermarkt / API-Football | 爬虫或付费 API | 中等 |
| 阵型战术 | WhoScored / FotMob / FBref | 爬虫 | 需维护 |
| 天气 | OpenWeatherMap | REST API + 球场坐标 | 免费 |
| 社媒情绪 | X/Twitter API | 搜索球队话题 | 付费 |

### 推荐策略：分步实施

```
第一步（立刻可做）: 方案一 — D1.csv 赔率+统计文本化
第二步（快速验证）: 方案二 — 对 Tactician 和 News Analyst 启用 LLM 搜索
第三步（工程化）  : 方案三 — 接入新闻 API，搜索结果可缓存复用
```

---

## 4. Prompt 改造方案

### 4.1 当前问题

1. `system_prompt` 没有指示 Agent 去搜索信息 — 只说"分析"，不说"先搜索再分析"
2. `_construct_prompt` 是通用的 — 所有 Agent 收到完全相同的数据结构，没有针对需要搜索的 Agent 做差异化处理

### 4.2 需要搜索的 Agent 的 system_prompt 改造

#### Tactician（战术师）

```python
system_prompt="""You are a tactical analyst with deep knowledge of football strategy.

IMPORTANT: Before analyzing, you MUST search for the latest information:
1. Search "{home_team} formation lineup latest match" for recent tactical setups
2. Search "{away_team} formation lineup latest match" for the opponent's approach
3. Search "{home_team} vs {away_team} tactical preview" for matchup analysis

Then combine your search findings with the provided statistical data to evaluate
how team formations, playing styles, and tactical approaches will influence the
match outcome. Consider formation matchups, tactical flexibility, and strategic
advantages. Assess how tactics might override statistical expectations."""
```

#### News Analyst（新闻分析师）

```python
system_prompt="""You are a sports journalist analyzing contextual factors.

IMPORTANT: Before analyzing, you MUST search for the latest information:
1. Search "{home_team} injury news squad update" for team availability
2. Search "{away_team} injury news squad update" for opponent availability
3. Search "{home_team} vs {away_team} preview" for pre-match context

Then combine your search findings with the provided data to evaluate team news,
injury reports, player morale, managerial pressure, and other qualitative factors
that might not appear in statistics. Consider the narrative and human elements
that influence performance."""
```

### 4.3 `_construct_prompt` 改造

对搜索型 Agent 追加搜索提示：

```python
# 在 _construct_prompt 末尾追加
if self.persona_type in ['tactician', 'news_analyst']:
    prompt_parts.extend([
        "",
        "SEARCH INSTRUCTIONS:",
        f"Before providing your analysis, search the web for the latest information about:",
        f"  - {match_context.get('home_team')} recent news, injuries, and tactical setup",
        f"  - {match_context.get('away_team')} recent news, injuries, and tactical setup",
        f"  - {match_context.get('home_team')} vs {match_context.get('away_team')} match preview",
        "Incorporate your search findings into your reasoning.",
    ])
```

### 4.4 前提条件：LLM 联网能力

| LLM | 是否支持搜索 | 如何启用 |
|---|---|---|
| Gemini (Google) | 支持 | 开启 grounding / Google Search tool |
| GPT-4/5 (OpenAI) | 支持 | 使用 web browsing 或 function calling |
| Claude (Anthropic) | 不直接支持 | 需要通过 MCP 或外部工具 |

如果 Agent 使用的 LLM 不支持联网（如 Claude），单靠改 prompt 不够，需要在代码层面先调搜索 API，把结果塞进 `qualitative_context`。

---

## 5. 对 Gemini 3 "概率再平衡器"方案的评价

（基于 `docs/gemini3_analysis.zh.md` 的分析）

### 5.1 核心观点是对的

- 传统 ML 模型对低概率事件（平局、冷门）系统性低估，这是结构性缺陷
- 用 LLM 补充定性分析来"再平衡"概率，理论上合理
- 意大利 1-4 挪威的案例很好地说明了定性信息（伤病、心理、对手状态）对冷门预测的决定性影响

### 5.2 需要注意的问题

1. **非结构化数据获取是最薄弱环节**：论文描述的是理想状态，实际代码里 `qualitative_context` 是硬编码的 mock 数据，数据管道是断的

2. **验证数据可信度存疑**：
   - 冷门预测 40% → 65% (+25%)，提升幅度非常大，"冷门"定义标准不明确
   - 538 场中平局约 135 场，样本偏小
   - 没有交叉验证、置信区间
   - 案例研究是事后分析，不是事前预测记录

3. **效果取决于输入质量**：`{{unstructured_data_stream}}` 的质量决定一切。如果输入只是 D1.csv 转换来的赔率文本，效果会远不如真正的新闻 + 伤病数据

### 5.3 结论

**方向正确，但从论文到可运行系统之间，"非结构化数据从哪来"是最大的 gap。** 建议先用 D1.csv 赔率数据 + LLM 搜索快速验证效果，再逐步接入专业数据源。

---

## 6. 关键风险：回测时 LLM 搜索导致数据泄露

### 6.1 问题描述

当回测历史比赛时（比如 3 月 10 号的比赛），如果让 LLM 联网搜索 "Bayern Munich vs Dortmund preview"，搜索结果里大概率会直接出现比赛结果：

> "拜仁 3-1 击败多特蒙德，穆勒梅开二度..."

Agent 看到了比赛结果再"预测"，准确率当然高，但毫无意义。这就是经典的 **数据泄露（Data Leakage）** 问题。

这也是为什么 `gemini3_analysis.zh.md` 中 +25% 冷门准确率的数据需要打问号 — 如果回测时用了联网搜索，整个验证结果就不可信。

### 6.2 泄露来源

| 泄露渠道 | 说明 |
|---|---|
| 搜索引擎结果 | 搜索关键词会返回包含比赛结果的页面 |
| LLM 训练数据 | 模型训练数据中可能已包含该比赛的结果 |
| 新闻聚合 | 赛后报道会覆盖赛前预览的搜索排名 |

### 6.3 解决方案

#### 方案 A：回测时关闭搜索，只用 D1.csv 数据（推荐）

```
回测模式: D1.csv 量化特征 + 赔率文本化 → Agent 分析（不搜索）
实时模式: D1.csv 特征 + LLM 搜索     → Agent 分析（搜索）
```

这是最干净的做法。回测时 `qualitative_context` 只包含从 D1.csv 生成的文本（赔率、统计风格画像），不包含任何搜索结果。

#### 方案 B：搜索但限制时间范围

如果一定要在回测中测试搜索效果，需要确保搜索结果只包含比赛之前的信息。但实际上很难控制 — 搜索引擎不保证只返回某个日期之前的内容，LLM 自身训练数据里也可能包含比赛结果。**不推荐**。

#### 方案 C：用赛前赔率作为"市场情绪"的代理

D1.csv 里的赔率数据（B365H、AvgH 等）本身就是赛前数据，不存在泄露问题。这些赔率已经综合了市场对伤病、状态、战术等所有公开信息的定价。用赔率文本化给 Sentiment Analyst，效果接近搜索，但完全没有泄露风险。

### 6.4 工程实现：模式开关

系统需要一个 `mode` 参数来区分回测和实时预测：

```python
class ConsensusEngine:
    def __init__(self, mode='live', ...):  # 'live' or 'backtest'
        self.mode = mode

# Agent 的 prompt 构造中：
def _construct_prompt(self, match_context, ...):
    ...
    # 只在实时模式下添加搜索指令
    if self.mode == 'live' and self.persona_type in ['tactician', 'news_analyst']:
        prompt_parts.extend([
            "",
            "SEARCH INSTRUCTIONS:",
            f"Search the web for latest information about this upcoming match...",
        ])
    elif self.mode == 'backtest':
        prompt_parts.extend([
            "",
            "NOTE: This is a backtest analysis. Use ONLY the data provided below.",
            "Do NOT search for or reference any external information about this match.",
        ])
```

### 6.5 总结

| 场景 | 是否可以搜索 | 数据来源 |
|---|---|---|
| 回测历史比赛 | **不可以** | 只用 D1.csv 数据（赔率 + 统计） |
| 预测未来比赛 | **可以** | LLM 搜索 + D1.csv 数据 |

**这是一条铁律：回测时绝不能让模型接触到比赛结果相关的任何信息，否则验证结果毫无意义。**
