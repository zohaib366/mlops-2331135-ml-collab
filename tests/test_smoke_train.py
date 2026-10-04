import json

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.common import RAW, TARGET, load_dataset, load_params


def test_smoke_train():
    """Train and evaluate a small sample to verify the ML pipeline works."""
    df = load_dataset(RAW)

    # Keep CI fast while still exercising the complete training flow.
    df = df.sample(n=300, random_state=42)

    train, test = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df[TARGET],
    )

    X_train = train.drop(columns=[TARGET])
    y_train = train[TARGET]
    X_test = test.drop(columns=[TARGET])
    y_test = test[TARGET]

    p = load_params()
    t = p["train"]

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
                    random_state=p["seed"],
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    assert len(predictions) == len(y_test)

    accuracy = accuracy_score(y_test, predictions)
    f1_macro = f1_score(y_test, predictions, average="macro")

    metrics = {
        "accuracy": round(float(accuracy), 4),
        "f1_macro": round(float(f1_macro), 4),
    }

    with open("ci-metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        f.write("\n")
