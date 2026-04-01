#!/usr/bin/env python3
"""
基线模型训练与评估脚本。

用法：
    python scripts/train_baseline.py                              # 默认：ensemble 集成，20% 测试集
    python scripts/train_baseline.py --model-type xgboost         # 仅 XGBoost
    python scripts/train_baseline.py --test-size 0.3              # 30% 测试集
"""

import argparse
import sys
import os

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

# Project root = parent of scripts/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from src.data.loader import MatchDataLoader
from src.models.baseline import BaselinePredictor, SimpleELOPredictor


# 元数据列，不参与训练
EXCLUDE_COLS = ['match_id', 'home_team', 'away_team', 'outcome', 'date', 'season']


def _resolve(path: str) -> str:
    """Turn a relative path into an absolute one based on project root."""
    if os.path.isabs(path):
        return path
    return os.path.join(PROJECT_ROOT, path)


def evaluate_baseline_predictor(train_df, test_df, model_type, loader):
    """Train and evaluate the BaselinePredictor (XGBoost + LightGBM)."""
    print("=" * 60)
    print(f"BaselinePredictor (mode: {model_type})")
    print("=" * 60)

    feature_cols = [c for c in train_df.columns if c not in EXCLUDE_COLS]

    X_train, y_train = loader.split_features_target(train_df, feature_cols=feature_cols)
    X_test, y_test = loader.split_features_target(test_df, feature_cols=feature_cols)

    print(f"训练集: {len(X_train)} 条, 测试集: {len(X_test)} 条")
    print(f"特征 ({len(feature_cols)} 个): {feature_cols}\n")

    predictor = BaselinePredictor(model_type=model_type)
    metrics = predictor.train(X_train, y_train)

    # 在测试集上评估
    y_pred = predictor.predict(X_test)
    y_proba = predictor.predict_proba(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"\n测试集准确率: {acc:.4f}")
    print("\n分类报告:")
    print(classification_report(
        y_test, y_pred,
        target_names=['主胜', '平局', '客胜']
    ))

    # 特征重要性
    importance = predictor.get_feature_importance()
    print("特征重要性 Top 10:")
    print(importance.head(10).to_string(index=False))
    print()

    return acc, metrics


def evaluate_elo_predictor(train_df, test_df):
    """Train and evaluate the SimpleELOPredictor."""
    print("=" * 60)
    print("SimpleELOPredictor")
    print("=" * 60)

    elo = SimpleELOPredictor()

    # 阶段 1: 从训练数据积累 ELO 等级分
    for _, row in train_df.iterrows():
        elo.update_ratings(row['home_team'], row['away_team'], int(row['outcome']))

    print(f"从 {len(train_df)} 场训练比赛中积累 ELO 等级分")
    print(f"跟踪球队数: {len(elo.ratings)}\n")

    # 阶段 2: 在测试集上预测
    correct = 0
    total = 0
    predictions = []

    for _, row in test_df.iterrows():
        home = row['home_team']
        away = row['away_team']

        home_rating = elo.ratings.get(home, 1500)
        away_rating = elo.ratings.get(away, 1500)

        proba = elo.predict_proba(home_rating, away_rating)
        pred = np.argmax(proba)
        actual = int(row['outcome'])

        predictions.append(pred)
        if pred == actual:
            correct += 1
        total += 1

        # 用实际结果更新 ELO，供后续预测使用
        elo.update_ratings(home, away, actual)

    acc = correct / total if total > 0 else 0
    y_test = test_df['outcome'].values.astype(int)

    print(f"测试集准确率: {acc:.4f}")
    print("\n分类报告:")
    print(classification_report(
        y_test, predictions,
        target_names=['主胜', '平局', '客胜']
    ))

    return acc


def main():
    parser = argparse.ArgumentParser(
        description='Train and evaluate baseline models.'
    )
    parser.add_argument(
        '--features', default='data/D1/features.csv',
        help='Path to features CSV (default: data/D1/features.csv)'
    )
    parser.add_argument(
        '--test-size', type=float, default=0.2,
        help='Test set proportion (default: 0.2)'
    )
    parser.add_argument(
        '--model-type', choices=['xgboost', 'lightgbm', 'ensemble'],
        default='ensemble',
        help='BaselinePredictor model type (default: ensemble)'
    )

    args = parser.parse_args()

    features_path = _resolve(args.features)
    data_dir = os.path.dirname(features_path)
    filename = os.path.basename(features_path)

    # 1. 加载数据
    loader = MatchDataLoader(data_dir=data_dir)
    df = loader.load_matches(filename)
    print(f"已加载 {len(df)} 场比赛数据，来源: {features_path}\n")

    # 2. 基于时间的训练/测试集划分
    train_df, test_df = loader.create_train_test_split(
        df, test_size=args.test_size, time_based=True
    )

    # 3. 评估两个模型
    baseline_acc, _ = evaluate_baseline_predictor(
        train_df, test_df, args.model_type, loader
    )
    elo_acc = evaluate_elo_predictor(train_df, test_df)

    # 4. 汇总对比
    print("=" * 60)
    print("汇总对比")
    print("=" * 60)
    print(f"BaselinePredictor ({args.model_type}): {baseline_acc:.4f}")
    print(f"SimpleELOPredictor:                    {elo_acc:.4f}")
    print(f"差值:                                  {baseline_acc - elo_acc:+.4f}")


if __name__ == '__main__':
    main()
