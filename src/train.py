"""Train the wine quality model.

Starter code adapted from the Kaggle notebook "wine-quality".
Source: <paste Kaggle notebook link and author here>
"""

import random

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.common import MODEL_PATH, PROCESSED, TARGET, load_params


def main() -> None:
    p = load_params()
    seed, t = p["seed"], p["train"]
    random.seed(seed)
    np.random.seed(seed)

    if t["model"] != "random_forest":
        raise ValueError(f"Unsupported model: {t['model']}")

    train = pd.read_csv(PROCESSED / "train.csv")
    X, y = train.drop(columns=[TARGET]), train[TARGET]

    # The scaler lives inside the Pipeline, so it is fit on the training split only
    model = Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=t["n_estimators"],
                    max_depth=t["max_depth"],
                    min_samples_leaf=t["min_samples_leaf"],
                    criterion=t["criterion"],
                    random_state=seed,
                ),
            ),
        ]
    )
    model.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)


if __name__ == "__main__":
    main()
