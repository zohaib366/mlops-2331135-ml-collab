"""Smoke tests for the project's data layout and config constants."""

from src.config import (
    EXTERNAL_DATA_DIR,
    INTERIM_DATA_DIR,
    MODELS_DIR,
    PROCESSED_DATA_DIR,
    PROJ_ROOT,
    RAW_DATA_DIR,
)


def test_proj_root_is_repo_root():
    assert (PROJ_ROOT / "pyproject.toml").is_file()


def test_data_directories_exist():
    for directory in (RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR):
        assert directory.is_dir(), f"missing data directory: {directory}"


def test_models_directory_exists():
    assert MODELS_DIR.is_dir()


def test_raw_dataset_is_dvc_tracked():
    """The CSV itself is pulled with DVC; only the .dvc pointer is in Git."""
    assert (RAW_DATA_DIR / "WineQT.csv.dvc").is_file()
