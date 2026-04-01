#!/usr/bin/env python3
"""
Build quantified features from raw D1 CSV data.

Usage:
    python scripts/build_features.py                          # incremental (default)
    python scripts/build_features.py --mode full              # full rebuild
    python scripts/build_features.py --data-dir data/D1 --output data/D1/features.csv
"""

import argparse
import sys
import os

# Project root = parent of scripts/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from src.data.feature_pipeline import FeaturePipeline


def _resolve(path: str) -> str:
    """Turn a relative path into an absolute one based on project root."""
    if os.path.isabs(path):
        return path
    return os.path.join(PROJECT_ROOT, path)


def main():
    parser = argparse.ArgumentParser(
        description='Build quantified features from raw D1 match data.'
    )
    parser.add_argument(
        '--data-dir', default='data/D1',
        help='Directory containing raw D1_*.csv files (default: data/D1)'
    )
    parser.add_argument(
        '--output', default='data/D1/features.csv',
        help='Output feature CSV path (default: data/D1/features.csv)'
    )
    parser.add_argument(
        '--mode', choices=['incremental', 'full'], default='incremental',
        help='Run mode: incremental (default) or full rebuild'
    )

    args = parser.parse_args()

    pipeline = FeaturePipeline()
    pipeline.run(
        data_dir=_resolve(args.data_dir),
        output_path=_resolve(args.output),
        mode=args.mode,
    )


if __name__ == '__main__':
    main()
