"""
Unemployment Dataset Loader & Preprocessing Entrypoint
CodeAlpha Task 2 - Data Science Internship

Provides direct access to loaded and cleaned datasets.
"""

from src.data_loader import load_raw_data
from src.preprocessing import preprocess_unemployment_data
from src.analysis import calculate_summary_statistics


def load_dataset(save_cleaned: bool = True):
    """
    Loads raw data and returns cleaned DataFrame.
    """
    raw_df = load_raw_data("unemployment.csv")
    cleaned_df = preprocess_unemployment_data(raw_df, save_cleaned=save_cleaned)
    return cleaned_df


if __name__ == "__main__":
    print("=" * 70)
    print("   LOADING & PREPROCESSING UNEMPLOYMENT DATASET   ")
    print("=" * 70)
    df = load_dataset()
    print("\n--- Cleaned Dataset Sample (First 5 Rows) ---")
    print(df.head())
    print("\n--- Summary Statistics ---")
    print(calculate_summary_statistics(df).to_string())
    print("\nDataset ready for analysis! Run 'python main.py' for full pipeline.")
