# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
# ---

# %% [markdown]
# # 01 - Exploratory Data Analysis
# Data is versioned with DVC: run `dvc pull` before opening this notebook.

# %%
import matplotlib.pyplot as plt
import pandas as pd

# `src` is installed by `uv sync`, so paths resolve from the package itself
# rather than from the kernel's working directory.
from src.config import RAW_DATA_DIR
from src.features import clean_data

DATA_PATH = RAW_DATA_DIR / "WineQT.csv"
TARGET = "quality"  # lower_snake_case after clean_data

# %%
raw = pd.read_csv(DATA_PATH)
df = clean_data(raw)
print(f"raw: {raw.shape} | cleaned: {df.shape} | duplicates removed: {len(raw) - len(df)}")
df.head()

# %% [markdown]
# ## Types and missing values

# %%
df.dtypes

# %%
df.isna().sum().sort_values(ascending=False)

# %% [markdown]
# ## Summary statistics

# %%
df.describe(include="all").T

# %% [markdown]
# ## Target balance

# %%
df[TARGET].value_counts(normalize=True)

# %% [markdown]
# ## Numeric distributions

# %%
df.select_dtypes("number").hist(figsize=(12, 8), bins=30)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Correlations

# %%
df.select_dtypes("number").corr().round(2)
