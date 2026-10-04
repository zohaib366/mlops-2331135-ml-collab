import json

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, f1_score

from src.common import METRICS_PATH, MODEL_PATH, PROCESSED, TARGET, git_sha


def main() -> None:
    model = joblib.load(MODEL_PATH)
    test = pd.read_csv(PROCESSED / "test.csv")
    X, y = test.drop(columns=[TARGET]), test[TARGET]

    pred = model.predict(X)  # the scaler (fit on train) is applied inside the pipeline
    print(classification_report(y, pred, zero_division=0))

    metrics = {
        "accuracy": round(float(accuracy_score(y, pred)), 4),
        "f1_macro": round(float(f1_score(y, pred, average="macro")), 4),
        "git_sha": git_sha(),
    }
    # trailing newline matters: pre-commit's end-of-file-fixer would otherwise edit this
    # file after DVC hashed it, and dvc.lock would no longer match
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n")


if __name__ == "__main__":
    main()
