"""
Helper entry point for the Bank Marketing EDA project.

Open Bank_Marketing_EDA.ipynb for the full graded notebook (Part 2).
Run the dashboard with:  streamlit run app.py
"""

from pathlib import Path

import pandas as pd

DATA_PATH = Path("data") / "bank.csv"


def load_bank_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the campaign CSV with a relative path."""
    return pd.read_csv(path)


if __name__ == "__main__":
    df = load_bank_data()
    print(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns from {DATA_PATH}")
    print(df.head())
