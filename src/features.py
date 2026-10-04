"""Feature generation and reusable data-cleaning functions."""

from pathlib import Path

from loguru import logger
import numpy as np
import pandas as pd
from tqdm import tqdm
import typer

from src.config import PROCESSED_DATA_DIR

app = typer.Typer()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of df (the input is not modified).

    - Column names: stripped, lower-case, spaces/hyphens -> underscores
    - String cells: whitespace stripped; empty strings -> NaN
    - Exact duplicate rows dropped
    """
    out = df.copy()
    out.columns = out.columns.str.strip().str.lower().str.replace(r"[\s\-]+", "_", regex=True)
    str_cols = out.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        out[col] = out[col].map(lambda v: v.strip() if isinstance(v, str) else v)
        out[col] = out[col].replace("", np.nan)
    return out.drop_duplicates().reset_index(drop=True)


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating features from dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Features generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
