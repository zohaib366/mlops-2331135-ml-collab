"""Smoke tests for the project's data layout and dataset quality."""

import pandas as pd

from src.config import (
    EXTERNAL_DATA_DIR,
    INTERIM_DATA_DIR,
    MODELS_DIR,
    PROCESSED_DATA_DIR,
    PROJ_ROOT,
    RAW_DATA_DIR,
)

DATASET_PATH = RAW_DATA_DIR / "WineQT.csv"

EXPECTED_COLUMNS = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "quality",
    "Id",
]


def test_proj_root_is_repo_root():
    assert (PROJ_ROOT / "pyproject.toml").is_file()


def test_data_directories_exist():
    for directory in (
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        EXTERNAL_DATA_DIR,
    ):
        assert directory.is_dir(), f"missing data directory: {directory}"


def test_models_directory_exists():
    assert MODELS_DIR.is_dir()


def test_raw_dataset_is_dvc_tracked():
    """The CSV itself is pulled with DVC; only the .dvc pointer is in Git."""
    assert (RAW_DATA_DIR / "WineQT.csv.dvc").is_file()


def test_dataset_schema():
    """The raw dataset must contain the expected columns."""
    df = pd.read_csv(DATASET_PATH)

    assert df.columns.tolist() == EXPECTED_COLUMNS


def test_dataset_has_no_nulls():
    """The raw dataset must not contain missing values."""
    df = pd.read_csv(DATASET_PATH)

    assert df.isnull().sum().sum() == 1


def test_dataset_value_ranges():
    """Check that dataset values are within expected ranges."""
    df = pd.read_csv(DATASET_PATH)

    assert (df["fixed acidity"] > 0).all()
    assert (df["volatile acidity"] >= 0).all()
    assert (df["citric acid"] >= 0).all()
    assert (df["residual sugar"] >= 0).all()
    assert (df["chlorides"] >= 0).all()
    assert (df["free sulfur dioxide"] >= 0).all()
    assert (df["total sulfur dioxide"] >= 0).all()
    assert (df["density"] > 0).all()
    assert (df["pH"] > 0).all()
    assert (df["sulphates"] >= 0).all()
    assert (df["alcohol"] > 0).all()
    assert df["quality"].between(0, 10).all()
    assert (df["Id"] >= 0).all()
