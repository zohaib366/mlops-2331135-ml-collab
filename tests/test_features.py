import numpy as np
import pandas as pd

from src.features import clean_data


def make_df():
    return pd.DataFrame(
        {
            " Customer ID": ["a", "b", "b", "c"],
            "Total-Charges": ["10.5", " 20 ", " 20 ", " "],
            "age": [30, 40, 40, np.nan],
        }
    )


def test_column_names_normalised():
    assert list(clean_data(make_df()).columns) == ["customer_id", "total_charges", "age"]


def test_duplicates_dropped():
    assert len(clean_data(make_df())) == 3


def test_whitespace_stripped_and_blank_becomes_nan():
    out = clean_data(make_df())
    assert out.loc[1, "total_charges"] == "20"
    assert pd.isna(out.loc[2, "total_charges"])


def test_existing_nulls_preserved():
    assert pd.isna(clean_data(make_df()).loc[2, "age"])


def test_input_not_mutated():
    df = make_df()
    before = df.copy()
    clean_data(df)
    pd.testing.assert_frame_equal(df, before)
