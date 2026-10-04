from sklearn.model_selection import train_test_split

from src.common import PROCESSED, RAW, TARGET, load_dataset, load_params


def main() -> None:
    p = load_params()
    df = load_dataset(RAW)
    train, test = train_test_split(
        df,
        test_size=p["split"]["test_size"],
        random_state=p["seed"],
        stratify=df[TARGET],  # keeps rare classes (quality 3 and 8) in both splits
    )
    PROCESSED.mkdir(parents=True, exist_ok=True)
    train.to_csv(PROCESSED / "train.csv", index=False)
    test.to_csv(PROCESSED / "test.csv", index=False)
    print(f"train: {len(train)} rows, test: {len(test)} rows")


if __name__ == "__main__":
    main()
