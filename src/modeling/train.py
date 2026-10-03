"""Train a baseline model on the red wine quality dataset (WineQT.csv).

Starter code adapted from the Kaggle notebook "wine-quality" (EDA + model
comparison with LogisticRegression, DecisionTree, SVC and KNN on WineQT.csv).
Source: <paste Kaggle notebook link and author here>
Dataset: UCI Wine Quality (red), Kaggle "Wine Quality Dataset" version WineQT.csv

Run (from the repo root):
    python src/modeling/train.py
    python src/modeling/train.py --model svc
    python src/modeling/train.py --drop-duplicates
    python src/modeling/train.py --data path/to/other.csv
"""

import argparse
from pathlib import Path
import random

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# This file lives in <repo>/src/modeling/, so the repo root is two levels up
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data" / "raw" / "WineQT.csv"

SEED = 42
TEST_SIZE = 0.2
TARGET = "quality"
ID_COLUMN = "Id"  # row index column in WineQT.csv, carries no information

# Hyperparameters (will move to params.yaml in the DVC pipeline phase)
N_ESTIMATORS = 100
MAX_DEPTH = 6


MODEL_CHOICES = ["random_forest", "svc", "logreg", "tree", "knn"]


def build_estimator(name: str):
    """Return the classifier for `name`; the notebook's models plus a Random Forest."""
    if name == "random_forest":
        return RandomForestClassifier(
            n_estimators=N_ESTIMATORS,
            max_depth=MAX_DEPTH,
            criterion="entropy",
            random_state=SEED,
        )
    if name == "svc":
        return SVC(C=50, kernel="rbf")
    if name == "logreg":
        return LogisticRegression(max_iter=1000, random_state=SEED)
    if name == "tree":
        return DecisionTreeClassifier(max_depth=10, random_state=SEED)
    if name == "knn":
        return KNeighborsClassifier(n_neighbors=5)
    raise ValueError(f"Unknown model: {name}")


def load_data(path: Path, drop_duplicates: bool = False) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Place WineQT.csv in data/raw/ (or pass --data)."
        )
    # sep=None lets pandas detect ";" (UCI original) or "," (WineQT.csv)
    df = pd.read_csv(path, sep=None, engine="python")

    # Drop the Id column first: it makes every row unique, which would hide
    # duplicates (WineQT.csv has 125 duplicate rows once Id is removed).
    df = df.drop(columns=[ID_COLUMN], errors="ignore")

    if TARGET not in df.columns:
        raise ValueError(f"Target column '{TARGET}' not found. Columns: {list(df.columns)}")

    if drop_duplicates:
        before = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Dropped {before - len(df)} duplicate rows ({before} -> {len(df)})")
    return df


def main(data_path: Path, model_name: str, drop_duplicates: bool) -> None:
    random.seed(SEED)
    np.random.seed(SEED)

    df = load_data(data_path, drop_duplicates)
    print(f"Loaded {data_path.name}: {df.shape[0]} rows, {df.shape[1]} columns")

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    # Stratify so the rare classes (quality 3 and 8) appear in both splits
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y
    )

    # The scaler lives inside the Pipeline, so it is fit on the training split only
    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("clf", build_estimator(model_name)),
        ]
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(f"model:    {model_name}")
    print(f"accuracy: {accuracy_score(y_test, pred):.4f}")
    print(f"f1_macro: {f1_score(y_test, pred, average='macro'):.4f}")
    print(classification_report(y_test, pred, zero_division=0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a wine quality model")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--model", choices=MODEL_CHOICES, default="random_forest")
    parser.add_argument(
        "--drop-duplicates",
        action="store_true",
        help="remove duplicate rows (ignoring Id) before splitting",
    )
    args = parser.parse_args()
    main(args.data, args.model, args.drop_duplicates)
