# Plan: 创建基线模型训练与评估脚本

## Context

已完成从原始德甲数据到量化特征的转换（`features.csv` 已生成，1467 条数据）。两个基线模型类（`BaselinePredictor` 和 `SimpleELOPredictor`）的训练/预测逻辑已在 `src/models/baseline.py` 中实现完毕，但缺少一个**运行脚本**将 `features.csv` 喂给模型进行训练、评估并输出结果。

## 要做的事

创建 `scripts/train_baseline.py`，串联特征数据与两个基线模型。

## 实现细节

### 脚本结构（沿用 `build_features.py` 的组织模式）

```
scripts/train_baseline.py
├── PROJECT_ROOT / sys.path 设置
├── argparse CLI 参数
│   ├── --features   特征文件路径 (默认 data/D1/features.csv)
│   ├── --test-size  测试集比例 (默认 0.2)
│   └── --model-type xgboost / lightgbm / ensemble (默认 ensemble)
└── main()
    ├── 1. 加载数据
    ├── 2. 训练 & 评估 BaselinePredictor
    ├── 3. 训练 & 评估 SimpleELOPredictor
    └── 4. 输出对比报告
```

### 核心流程

1. **加载数据**：用 `MatchDataLoader(data_dir).load_matches('features.csv')` 加载
2. **时间切分**：用 `loader.create_train_test_split(df, test_size, time_based=True)` 做基于时间的划分（避免数据泄露）
3. **特征/标签分离**：用 `loader.split_features_target(df)` 自动分离，但需额外排除 `season` 列（字符串类型，不适合直接喂给数值模型）
4. **BaselinePredictor 训练**：`predictor.train(X_train, y_train)` → 在测试集上 `predict(X_test)` → 计算准确率、分类报告
5. **SimpleELOPredictor 评估**：按时间顺序遍历训练集 `update_ratings()` 积累 ELO，然后在测试集上逐行 `predict_proba()` → 计算准确率
6. **输出对比**：打印两个模型的准确率、各类别精确率/召回率、特征重要性 Top 10

### 需修复的问题：`season` 列未被排除

`loader.py` 的 `split_features_target()` 自动排除列表为 `['match_id', 'home_team', 'away_team', 'outcome', 'date']`，漏掉了 `season`。  
`season` 是字符串（如 `"2122"`），混入特征会导致 XGBoost/LightGBM 报错。

**修复方式**：在训练脚本中手动指定 `feature_cols` 参数，补上 `season` 的排除：

```python
exclude = ['match_id', 'home_team', 'away_team', 'outcome', 'date', 'season']
feature_cols = [c for c in df.columns if c not in exclude]
X, y = loader.split_features_target(df, feature_cols=feature_cols)
```

不改动 `loader.py` 源码，仅在调用侧处理。

## 涉及文件

| 文件 | 操作 |
|------|------|
| `scripts/train_baseline.py` | **新建** — 训练评估脚本 |

### 复用的已有代码

- `src/data/loader.py` → `MatchDataLoader.load_matches()`, `split_features_target()`, `create_train_test_split()`
- `src/models/baseline.py` → `BaselinePredictor`, `SimpleELOPredictor`

## 验证方式

```bash
python scripts/train_baseline.py
python scripts/train_baseline.py --model-type xgboost --test-size 0.3
```

预期输出：两个模型的准确率和分类报告，无报错。
