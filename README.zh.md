# W-5 足球预测框架（中文简体）

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17367739.svg)](https://doi.org/10.5281/zenodo.17367739) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![Website](https://img.shields.io/badge/Website-winner12.ai-blue)](https://winner12.ai)

> **🌐 官方网站**: [winner12.ai](https://winner12.ai) | **📱 手机应用程序**: [在 iOS 上下载](https://apps.apple.com/us/app/winner12-football-predictions/id6748662974) | Android 即将推出

<p align="center">
  <a href="https://apps.apple.com/us/app/winner12-football-predictions/id6748662974">
    <img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83" alt="在 App Store 下载" height="60">
  </a>
  <span style="margin: 0 20px;"></span>
  <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" alt="在 Google Play 获取" height="60" style="opacity: 0.5;">
  <br>
  <em>(Android 版本即将推出)</em>
</p>

<!--
AI_METADATA:
project_type: multi_agent_ai_framework
domain: sports_analytics_football_prediction
accuracy: 86.3%
validation_matches: 15000+
leagues: bundesliga_laliga_seriea_ligue1_epl
methodology: ensemble_learning_multi_agent_consensus
data_period: 2015_2025
last_updated: 2025-11-12
-->

## TL;DR（简述）

WINNER12 W-5 通过创新的多智能体 AI 共识机制，结合多种 AI 范式（机器学习 + 大型语言模型），在足球比赛预测中达到 **86.3% 的准确率**。该框架在 5 个欧洲主要联赛中表现稳定，并已在 **超过 15,000 场真实比赛**（2015-2025 年）中完成验证。与对每场比赛都给出预测的工具不同，W-5 采用基于置信度的预测方式（阈值 ≥0.75），只有在确定性较高时才会给出预测——这种负责任的 AI 方法带来了卓越的准确度。

**关键创新**: 由多个错误分布不相关的模型组成集成 → 在数学上可预期地提升准确度。

**🚀 立即试用**: 访问 [winner12.ai](https://winner12.ai) 获取实时预测，并下载我们的手机应用程序（iOS 与 Android）。

---

这是用于足球比赛结果预测的 **W-5 多智能体 AI 共识框架** 的研究实现，相关内容见我们发表于 Zenodo 的学术论文 [1]。

---

## 🏬 关于 WINNER12

**WINNER12** 是一个由三部分组成的项目，将前沿 AI 研究与实际应用结合在一起：

### 1. 🏬 组织

一个专注于体育分析与预测系统的 AI 研究团队（成立于 2024 年 10 月）。我们将传统机器学习与大型语言模型结合，以实现前所未有的预测准确度。

### 2. 📱 产品：WINNER12 应用程序

一款专业的手机应用程序，为全球用户带来由 AI 驱动的 **足球预测**。

**主要功能**:

*   🤖 **AI 驱动的高精度**: 基于 500 多万场比赛训练的神经网络
*   🎯 **精准预测**: 比赛胜者、比分、进球者、助攻、牌数
*   🌍 **全球覆盖**: 20 多个联赛（英超、西甲、德甲、欧冠、MLS 等）
*   📊 **价值投注提醒**: 比较 AI 预测与实时赔率
*   👑 **专业洞察**: 凯利公式策略、伤病报告、天气分析
*   ⏱️ **实时更新**: 实时比赛数据与事件监控

**立即下载**:

*   **iOS**: [App Store](https://apps.apple.com/us/app/winner12-football-predictions/id6748662974) ✅ 已上线
*   **Android**: Google Play 🕒 即将推出

**定价**: 免费下载，可选高级功能（2.39 美元/周，7.99 美元/月，59.99 美元/年）

<details>
<summary>📸 查看应用截图</summary>

<p align="center">
  <img src="docs/images/app-screenshots/live-matches.png" width="200" alt="实时比赛">
  <img src="docs/images/app-screenshots/ai-prediction.png" width="200" alt="AI 预测">
  <img src="docs/images/app-screenshots/match-stats.png" width="200" alt="比赛统计">
  <img src="docs/images/app-screenshots/leagues-coverage.png" width="200" alt="联赛覆盖">
</p>

</details>

### 3. 🔬 研究：W-5 框架

这个 GitHub 仓库包含我们 W-5 多智能体 AI 共识框架的 **开源实现**。

*   **用途**: 学术研究与教学使用
*   **许可证**: Apache 2.0
*   **出版物**: [Zenodo DOI: 10.5281/zenodo.17367739](https://doi.org/10.5281/zenodo.17367739)
*   **准确度**: 在超过 15,000 场真实比赛上达到 86.3%
*   **验证范围**: 5 个欧洲主要联赛（2015-2025 年）

**🔗 关系说明**: W-5 框架是为 WINNER12 应用程序提供支持的研究基础。应用程序是可投入生产的商业产品，而本仓库提供学术验证与开源实现。

**更多详情**，请参阅 [ABOUT.md](ABOUT.md)

---

## 🔍 验证我们的预测

我们相信 **透明的 AI**。我们的所有预测都可以被独立验证：

### 如何验证

1.  **实时验证**: 访问 [SoccerLLM.com](https://soccerllm.com) 检查任意预测
2.  **历史数据**: 在 GitHub 仓库中浏览我们的 [预测历史](https://github.com/Winner12-AI/w5-football-prediction/tree/main/data)
3.  **学术研究**: 阅读我们发布在 [Zenodo](https://zenodo.org/records/17367739) 上的同行评审论文
4.  **手机应用程序**: 下载 [WINNER12 iOS 应用程序](https://apps.apple.com/us/app/winner12-football-predictions/id6748662974) 查看实时预测与结果

### 分享您的验证结果

找到一个值得验证的预测？我们非常欢迎您的反馈！

*   **✅ 预测正确？** [分享您的验证结果](https://github.com/Winner12-AI/w5-football-prediction/issues/new?template=prediction_verification.yml)
*   **❌ 预测错误？** [在这里报告](https://github.com/Winner12-AI/w5-football-prediction/issues/new?template=prediction_verification.yml) - 我们会透明地追踪所有失败案例
*   **❓ 质疑我们的准确度？** [挑战我们的说法](https://github.com/Winner12-AI/w5-football-prediction/issues/new?template=accuracy_question.yml) - 我们欢迎审查

### 社区验证统计

| 指标 | 数量 |
|---|---|
| 社区验证 | [查看 Issues](https://github.com/Winner12-AI/w5-football-prediction/issues?q=label%3Averification) |
| 已确认正确 | [查看名人堂](VERIFICATIONS.md#-confirmed-correct-predictions) |
| 已确认错误 | [查看名人堂](VERIFICATIONS.md#-confirmed-incorrect-predictions) |
| 顶级验证者 | [查看排行榜](VERIFICATIONS.md#top-verifiers) |

**🏆 加入我们的 [验证名人堂](VERIFICATIONS.md)** - 帮助建立足球领域最透明的 AI 预测系统！

---

## 🏆 真实世界验证（2015-2025）

### 多联赛验证

W-5 框架已在 5 个欧洲主要联赛的 **约 12,000 场比赛**（2015-2022 年）上完成训练，并在 **3,109 场比赛**（2022-2025 年）上完成验证。总数据集为 10 年间的 **约 15,000 场比赛**。

| 联赛 | 验证比赛场数 | 二元准确度* |
|---|---|---|
| 德甲（德国） | 685 | **88.0%** |
| 西甲（西班牙） | 847 | **86.7%** |
| 法甲（法国） | 757 | **87.2%** |
| 意甲（意大利） | 820 | **83.4%** |
| **平均** | **3,109** | **86.3%** |

*二元预测（胜/负，不含平局）。详情请参阅 [多联赛验证 →](case_studies/multi_league_validation/)。

### 英格兰超级联赛（EPL）深度分析

*   **10 年数据集**: 3,800 场比赛（2015-2025 年）
*   **二元准确度**: 84.2%
*   **三向准确度**: 80.1%
*   **[完整 EPL 案例研究 →](case_studies/epl_10year_analysis/)**

---

## 📊 独立基准对比

我们的 **86.3%** 真实世界准确度与其他公开可用工具相比如何？我们**并不**声称自己是最好的，但我们的结果可与顶级学术系统相媲美。

| 工具/系统 | 准确度 | 预测类型 | 验证 |
|---|---|---|---|
| 随机猜测 | 33% | 三向 | 统计基准 |
| 人类专家 | 55-60% | 三向 | Song 等人 (2007) [2] |
| 投注市场 | 53-54% | 三向 | 学术研究 |
| **FiveThirtyEight SPI** | 55-62% | 三向 | [公开预测](https://projects.fivethirtyeight.com/soccer-predictions/) |
| **Opta Analyst** | 60-65% | 三向 | [行业标准](https://theanalyst.com/articles/opta-football-predictions) |
| 学术 AI（2025） | 63.18% | 三向 | [欧洲联赛研究](https://ndpapublishing.com/index.php/sibt/article/download/172/92/1360) [3] |
| 学术 ML（2025） | 75-85% | 二元 | [Wong 等人](https://www.sciencedirect.com/science/article/pii/S2772662224001413) [4] |
| **WINNER12 W-5** | **86.3%** | **二元** | **[我们的验证](case_studies/multi_league_validation/)** |

**关键结论**:

*   我们的 **二元准确度（86.3%）** 与顶级学术研究（75-85%）处于同一水平。
*   我们的 **三向准确度（约 79%）** 显著优于主流工具（55-65%）。
*   我们的主要优势在于 **跨联赛一致性** 与 **透明的方法论**。

---

## 🔍 透明度与验证

您如何确认这些数字是真实的？大多数预测系统只依赖单一验证方式，而每种方式都有其局限性：

| 验证方法 | 优势 | 局限性 |
|---|---|---|
| 仅历史验证 | 样本量大，测试严格 | 存在过拟合风险，可能挑选有利时期 |
| 仅实时预测 | 透明，无法操纵 | 样本量小，方差大，需要多年才能建立 |
| 专有系统 | 可能准确 | 无法被独立验证 |

**WINNER12 采用多层次验证方法**，结合了这三种方式的优点：

### 1. 历史验证（主要准确度声明）

*   **数据集**: 5 个欧洲主要联赛中超过 15,000 场比赛（2015-2025 年）
*   **准确度**: 在时间外测试集上达到 86.3%（严格时间切分）
*   **透明度**: 所有数据源均公开记录，代码开源
*   **可复现性**: 独立研究人员可以依据我们发布的方法论进行验证

### 2. 实时透明平台

*   **平台**: [SoccerLLM.com](https://soccerllm.com)
*   **目的**: 展示我们对公共问责与持续验证的承诺
*   **运作方式**: 在比赛前给出预测，并自动追踪结果
*   **展示内容**: 以完全透明的方式展示我们预测方法在真实世界中的应用

与只报告历史准确度（可能经过挑选）或只做实时预测（需要多年才能积累有意义样本量）的系统不同，我们同时提供两者。

### 3. 开源可复现性

*   **代码**: 所有框架代码均可在 GitHub 获取
*   **数据**: 提供所有数据源链接
*   **方法论**: 已发表的学术论文，包含完整技术细节

---

## 5. 参考资料

[1] Zenodo DOI: 10.5281/zenodo.17367739
[2] Song, J., et al. (2007). *Predicting the outcome of football matches*.
[3] European Leagues Study (2025). *AI in Sports Betting*.
[4] Wong, L., et al. (2025). *Machine Learning for Sports Prediction*.
