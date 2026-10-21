"""
Data Loader Module for Unemployment Analysis
CodeAlpha Task 2 - Data Science Internship

Responsible for loading the raw dataset from the local 'data/' directory.
"""

import os
from pathlib import Path
import pandas as pd


def get_project_root() -> Path:
    """Returns the root directory path of the project."""
    return Path(__file__).resolve().parent.parent


def load_raw_data(filename: str = "unemployment.csv") -> pd.DataFrame:
    """
    Loads raw unemployment data from the project's data directory.

    Args:
        filename (str): Name of the CSV file inside 'data/'. Defaults to 'unemployment.csv'.

    Returns:
        pd.DataFrame: Raw loaded pandas DataFrame.

    Raises:
        FileNotFoundError: If the specified file does not exist in the data folder.
    """
    project_root = get_project_root()
    filepath = project_root / "data" / filename

    if not filepath.exists():
        # Fallback check for 'Unemployment in India.csv'
        fallback_path = project_root / "data" / "Unemployment in India.csv"
        if fallback_path.exists():
            filepath = fallback_path
        else:
            raise FileNotFoundError(
                f"\n[ERROR] Dataset not found at: {filepath}\n"
                f"Please ensure '{filename}' or 'Unemployment in India.csv' is placed inside '{project_root / 'data'}'."
            )

    print(f"[INFO] Loading raw dataset from: {filepath.name}")
    df = pd.read_csv(filepath)
    print(f"[INFO] Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
    return df


if __name__ == "__main__":
    raw_df = load_raw_data()
    print("\n--- First 5 Rows ---")
    print(raw_df.head())
    print("\n--- Column Info ---")
    print(raw_df.info())
