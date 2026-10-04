from pathlib import Path
import subprocess

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]  # repo root, no absolute paths
RAW = ROOT / "data" / "raw" / "WineQT.csv"
PROCESSED = ROOT / "data" / "processed"
MODEL_PATH = ROOT / "models" / "model.joblib"
METRICS_PATH = ROOT / "metrics.json"
TARGET = "quality"
ID_COLUMN = "Id"


def load_params(path: Path = ROOT / "params.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_dataset(path: Path) -> pd.DataFrame:
    """Read a wine CSV (";" or ",") and drop the uninformative Id column."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}. Run `dvc pull` first.")
    df = pd.read_csv(path, sep=None, engine="python")
    return df.drop(columns=[ID_COLUMN], errors="ignore")


def git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"
