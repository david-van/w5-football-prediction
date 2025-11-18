# W-5 축구 예측 프레임워크

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17367739.svg)](https://doi.org/10.5281/zenodo.17367739) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![Website](https://img.shields.io/badge/Website-winner12.ai-blue)](https://winner12.ai)

> **🌐 공식 웹사이트**: [winner12.ai](https://winner12.ai) | **📱 모바일 앱**: [iOS에서 다운로드](https://apps.apple.com/us/app/winner12-football-predictions/id6748662974) | Android 곧 출시 예정

<p align="center">
  <a href="https://apps.apple.com/us/app/winner12-football-predictions/id6748662974">
    <img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83" alt="App Store에서 다운로드" height="60">
  </a>
  <span style="margin: 0 20px;"></span>
  <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" alt="Google Play에서 받기" height="60" style="opacity: 0.5;">
  <br>
  <em>(Android 버전 곧 출시 예정)</em>
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

## TL;DR (요약)

WINNER12 W-5는 새로운 다중 에이전트 AI 합의 메커니즘을 통해 여러 AI 패러다임(기계 학습 + 대규모 언어 모델)을 결합하여 축구 경기 예측에서 **86.3%의 정확도**를 달성합니다. 이 프레임워크는 5대 유럽 리그에서 일관된 성능을 보여주며, **15,000개 이상의 실제 경기** (2015-2025)에서 검증되었습니다. 모든 경기를 예측하는 도구와 달리, W-5는 신뢰 기반 예측(≥0.75 임계값)을 사용하며, 확신도가 높을 때만 예측을 수행합니다. 이는 우수한 정확도를 제공하는 책임감 있는 AI 접근 방식입니다.

**핵심 혁신**: 상관관계가 없는 오류 분포를 가진 다중 모델 앙상블 → 수학적으로 예상되는 정확도 향상.

**🚀 지금 사용해 보세요**: 실시간 예측을 위해 [winner12.ai](https://winner12.ai)를 방문하고 모바일 앱(iOS 및 Android)을 다운로드하세요.

---

Zenodo에 발표된 당사의 학술 논문 [1]에 설명된 바와 같이, 축구 경기 결과 예측을 위한 **W-5 다중 에이전트 AI 합의 프레임워크**의 연구 구현입니다.

---

## 🏬 WINNER12 소개

**WINNER12**는 최첨단 AI 연구와 실용적인 애플리케이션을 결합한 3부작 이니셔티브입니다.

### 1. 🏬 조직

스포츠 분석 및 예측 시스템을 전문으로 하는 AI 연구팀(2024년 10월 설립). 우리는 전례 없는 예측 정확도를 달성하기 위해 전통적인 기계 학습과 대규모 언어 모델을 결합합니다.

### 2. 📱 제품: WINNER12 앱

전 세계 사용자에게 AI 기반 **축구 예측**을 제공하는 전문 모바일 애플리케이션입니다.

**주요 기능**:

*   🤖 **AI 기반 정밀도**: 500만 개 이상의 경기에서 훈련된 신경망
*   🎯 **정확한 예측**: 경기 승자, 점수, 득점자, 어시스트, 카드
*   🌍 **글로벌 커버리지**: 20개 이상의 리그(EPL, 라 리가, 분데스리가, 챔피언스 리그, MLS 등)
*   📊 **가치 베팅 알림**: AI 예측 대 실시간 배당률 비교
*   👑 **프로 통찰력**: 켈리 기준 전략, 부상 보고서, 날씨 분석
*   ⏱️ **실시간 업데이트**: 라이브 경기 데이터 및 이벤트 모니터링

**지금 다운로드**:

*   **iOS**: [App Store](https://apps.apple.com/us/app/winner12-football-predictions/id6748662974) ✅ 지금 이용 가능
*   **Android**: Google Play 🕒 곧 출시 예정

**가격**: 선택적 프리미엄 기능이 포함된 무료 다운로드($2.39/주, $7.99/월, $59.99/년)

<details>
<summary>📸 앱 스크린샷 보기</summary>

<p align="center">
  <img src="docs/images/app-screenshots/live-matches.png" width="200" alt="라이브 경기">
  <img src="docs/images/app-screenshots/ai-prediction.png" width="200" alt="AI 예측">
  <img src="docs/images/app-screenshots/match-stats.png" width="200" alt="경기 통계">
  <img src="docs/images/app-screenshots/leagues-coverage.png" width="200" alt="리그 커버리지">
</p>

</details>

### 3. 🔬 연구: W-5 프레임워크

이 GitHub 리포지토리에는 W-5 다중 에이전트 AI 합의 프레임워크의 **오픈 소스 구현**이 포함되어 있습니다.

*   **목적**: 학술 연구 및 교육용
*   **라이선스**: Apache 2.0
*   **출판**: [Zenodo DOI: 10.5281/zenodo.17367739](https://doi.org/10.5281/zenodo.17367739)
*   **정확도**: 15,000개 이상의 실제 경기에서 86.3%
*   **검증**: 5대 유럽 리그(2015-2025)

**🔗 관계**: W-5 프레임워크는 WINNER12 앱에 동력을 공급하는 연구 기반입니다. 이 앱은 상업용 제품으로 출시되었으며, 이 리포지토리는 학술적 검증과 오픈 소스 구현을 제공합니다.

**자세한 내용은** [ABOUT.md](ABOUT.md)를 참조하세요.

---

## 🔍 예측 검증

우리는 **투명한 AI**를 믿습니다. 당사의 모든 예측은 독립적으로 검증될 수 있습니다.

### 검증 방법

1.  **실시간 검증**: [SoccerLLM.com](https://soccerllm.com)을 방문하여 예측 확인
2.  **과거 데이터**: GitHub 리포지토리에서 [예측 기록](https://github.com/Winner12-AI/w5-football-prediction/tree/main/data) 탐색
3.  **학술 연구**: [Zenodo](https://zenodo.org/records/17367739)에 있는 당사의 동료 검토 논문 읽기
4.  **모바일 앱**: [WINNER12 iOS 앱](https://apps.apple.com/us/app/winner12-football-predictions/id6748662974)을 다운로드하여 실시간 예측 및 결과 확인

### 검증 공유

검증할 예측을 찾았습니까? 의견을 듣고 싶습니다!

*   **✅ 정확한 예측입니까?** [검증 공유](https://github.com/Winner12-AI/w5-football-prediction/issues/new?template=prediction_verification.yml)
*   **❌ 부정확한 예측입니까?** [여기에 보고](https://github.com/Winner12-AI/w5-football-prediction/issues/new?template=prediction_verification.yml) - 모든 실패를 투명하게 추적합니다
*   **❓ 정확도에 의문이 있습니까?** [주장에 이의 제기](https://github.com/Winner12-AI/w5-football-prediction/issues/new?template=accuracy_question.yml) - 면밀한 조사를 환영합니다

### 커뮤니티 검증 통계

| 지표 | 횟수 |
|---|---|
| 커뮤니티 검증 | [이슈 보기](https://github.com/Winner12-AI/w5-football-prediction/issues?q=label%3Averification) |
| 정확 확인 | [명예의 전당 보기](VERIFICATIONS.md#-confirmed-correct-predictions) |
| 부정확 확인 | [명예의 전당 보기](VERIFICATIONS.md#-confirmed-incorrect-predictions) |
| 최고 검증자 | [리더보드 보기](VERIFICATIONS.md#top-verifiers) |

**🏆 [검증 명예의 전당](VERIFICATIONS.md)에 참여** - 축구에서 가장 투명한 AI 예측 시스템을 구축하는 데 도움을 주세요!

---

## 🏆 실제 검증 (2015-2025)

### 다중 리그 검증

W-5 프레임워크는 5대 유럽 리그의 **~12,000개 경기** (2015-2022)에서 훈련되었으며, **3,109개 경기** (2022-2025)에서 검증되었습니다. 총 데이터 세트: 10년 동안 **~15,000개 경기**.

| 리그 | 검증 경기 수 | 이진 정확도* |
|---|---|---|
| 분데스리가 (독일) | 685 | **88.0%** |
| 라 리가 (스페인) | 847 | **86.7%** |
| 리그 1 (프랑스) | 757 | **87.2%** |
| 세리에 A (이탈리아) | 820 | **83.4%** |
| **평균** | **3,109** | **86.3%** |

*이진 예측(승/패, 무승부 제외). 자세한 내용은 [다중 리그 검증 →](case_studies/multi_league_validation/)을 참조하세요.

### 잉글랜드 프리미어 리그 (EPL) 심층 분석

*   **10년 데이터 세트**: 3,800개 경기 (2015-2025)
*   **이진 정확도**: 84.2%
*   **삼원 정확도**: 80.1%
*   **[전체 EPL 사례 연구 →](case_studies/epl_10year_analysis/)**

---

## 📊 독립 벤치마크 비교

당사의 실제 **86.3%** 정확도는 다른 공개적으로 사용 가능한 도구와 어떻게 비교됩니까? 우리는 최고라고 주장하지 않지만, 당사의 결과는 최고 수준의 학술 시스템과 비교할 수 있습니다.

| 도구/시스템 | 정확도 | 예측 유형 | 검증 |
|---|---|---|---|
| 무작위 추측 | 33% | 삼원 | 통계적 기준선 |
| 인간 전문가 | 55-60% | 삼원 | Song et al. (2007) [2] |
| 베팅 시장 | 53-54% | 삼원 | 학술 연구 |
| **FiveThirtyEight SPI** | 55-62% | 삼원 | [공개 예측](https://projects.fivethirtyeight.com/soccer-predictions/) |
| **Opta Analyst** | 60-65% | 삼원 | [산업 표준](https://theanalyst.com/articles/opta-football-predictions) |
| 학술 AI (2025) | 63.18% | 삼원 | [유럽 리그 연구](https://ndpapublishing.com/index.php/sibt/article/download/172/92/1360) [3] |
| 학술 ML (2025) | 75-85% | 이진 | [Wong et al.](https://www.sciencedirect.com/science/article/pii/S2772662224001413) [4] |
| **WINNER12 W-5** | **86.3%** | **이진** | **[당사의 검증](case_studies/multi_league_validation/)** |

**주요 시사점**:

*   당사의 **이진 정확도 (86.3%)**는 최고 수준의 학술 연구(75-85%)와 동일한 수준입니다.
*   당사의 **삼원 정확도 (~79%)**는 주류 도구(55-65%)보다 훨씬 뛰어납니다.
*   당사의 주요 이점은 **리그 간 일관성**과 **투명한 방법론**입니다.

---

## 🔍 투명성 및 검증

이 수치가 실제임을 어떻게 알 수 있습니까? 대부분의 예측 시스템은 각각 한계가 있는 단일 검증 방법에 의존합니다.

| 검증 접근 방식 | 강점 | 한계 |
|---|---|---|
| 과거 검증만 | 큰 표본 크기, 엄격한 테스트 | 과적합 위험, 유리한 기간 선택 |
| 실시간 예측만 | 투명하고 조작 불가능 | 작은 표본 크기, 높은 분산, 구축에 수년 소요 |
| 독점 시스템 | 정확할 수 있음 | 독립적인 당사자가 검증할 수 없음 |

**WINNER12는 세 가지 모두의 강점을 결합한 다층 검증 접근 방식을 사용합니다**:

### 1. 과거 검증 (주요 정확도 주장)

*   **데이터 세트**: 5대 유럽 리그의 15,000개 이상의 경기 (2015-2025)
*   **정확도**: 시간 외 테스트 세트에서 86.3% (엄격한 시간적 분할)
*   **투명성**: 모든 데이터 소스가 공개적으로 문서화되고 코드가 오픈 소스
*   **재현성**: 독립적인 연구자가 당사의 공개된 방법론을 사용하여 검증 가능

### 2. 실시간 투명성 플랫폼

*   **플랫폼**: [SoccerLLM.com](https://soccerllm.com)
*   **목적**: 공공 책임 및 지속적인 검증에 대한 당사의 약속을 보여줍니다
*   **작동 방식**: 예측은 경기 전에 이루어지며 결과는 자동으로 추적됩니다
*   **표시 내용**: 완전한 투명성을 갖춘 당사 예측 방법론의 실제 적용

과거 정확도만 보고하는 시스템(선택될 수 있음) 또는 실시간 예측만 하는 시스템(의미 있는 표본 크기를 축적하는 데 수년이 걸림)과 달리, 우리는 둘 다 제공합니다.

### 3. 오픈 소스 재현성

*   **코드**: 모든 프레임워크 코드는 GitHub에서 사용 가능
*   **데이터**: 제공된 모든 데이터 소스에 대한 링크
*   **방법론**: 전체 기술 세부 사항이 포함된 공개된 학술 논문

---

## 5. 참고 문헌

[1] Zenodo DOI: 10.5281/zenodo.17367739
[2] Song, J., et al. (2007). *Predicting the outcome of football matches*.
[3] European Leagues Study (2025). *AI in Sports Betting*.
[4] Wong, L., et al. (2025). *Machine Learning for Sports Prediction*.
