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

# Allow running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data.feature_pipeline import FeaturePipeline


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
        data_dir=args.data_dir,
        output_path=args.output,
        mode=args.mode,
    )


if __name__ == '__main__':
    main()
