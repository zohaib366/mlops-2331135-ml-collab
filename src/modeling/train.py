"""Train a baseline model on the white wine quality dataset.

Starter code adapted from the Kaggle notebook "Popular ML/NN/CNN/RNN Models
code snippets" (data loading and scaling from its wine section, Random Forest
from its classification section).
Source: <paste Kaggle notebook link and author here>

Run:  python src/modeling/train.py
      python src/modeling/train.py --data path/to/other.csv
"""

import argparse
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# This file lives in <repo>/src/modeling/, so the repo root is two levels up
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data" / "raw" / "winequality-white.csv"

SEED = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
MAX_DEPTH = 6
TARGET = "quality"


def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            "Place winequality-white.csv in data/raw/ (or pass --data)."
        )
    # The UCI file uses ";" as separator; sep=None lets pandas detect ";" or ","
    return pd.read_csv(path, sep=None, engine="python")


def main(data_path: Path) -> None:
    df = load_data(data_path)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED
    )

    # Fit the scaler on the training split only, then apply it to the test split
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        max_depth=MAX_DEPTH,
        criterion="entropy",
        random_state=SEED,
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(f"accuracy: {accuracy_score(y_test, pred):.4f}")
    print(f"f1_macro: {f1_score(y_test, pred, average='macro'):.4f}")
    print(classification_report(y_test, pred, zero_division=0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a wine quality model")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    main(args.data)
