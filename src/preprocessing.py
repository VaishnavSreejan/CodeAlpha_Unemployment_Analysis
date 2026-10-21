"""
Preprocessing Module for Unemployment Analysis
CodeAlpha Task 2 - Data Science Internship

Responsible for cleaning, handling missing/duplicate records, formatting dates,
creating temporal features, and saving the cleaned dataset.
"""

from pathlib import Path
import pandas as pd
from .data_loader import get_project_root


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Strips whitespace and standardizes column names."""
    clean_cols = {}
    for col in df.columns:
        stripped = col.strip()
        # Standardize known column names for easy access
        if "Unemployment Rate" in stripped:
            clean_cols[col] = "Estimated_Unemployment_Rate_Pct"
        elif "Labour Participation" in stripped:
            clean_cols[col] = "Estimated_Labour_Participation_Rate_Pct"
        elif "Employed" in stripped:
            clean_cols[col] = "Estimated_Employed"
        elif stripped == "Region.1":
            clean_cols[col] = "Zone"
        else:
            clean_cols[col] = stripped
    return df.rename(columns=clean_cols)


def preprocess_unemployment_data(
    df: pd.DataFrame, 
    save_cleaned: bool = True,
    output_filename: str = "cleaned_unemployment_data.csv"
) -> pd.DataFrame:
    """
    Cleans and preprocesses the raw unemployment dataset.

    Steps:
    1. Inspects raw missing values and duplicates.
    2. Drops entirely blank rows (common at the tail of raw survey CSVs).
    3. Trims whitespace from string headers and categorical values.
    4. Converts 'Date' column to datetime.
    5. Engineers time features: Year, Month, Month_Name, and COVID_Period.
    6. Validates data integrity (no negative rates, valid percentages).
    7. Optionally exports cleaned data to 'outputs/cleaned_unemployment_data.csv'.

    Args:
        df (pd.DataFrame): Raw DataFrame.
        save_cleaned (bool): Whether to save the output CSV. Defaults to True.
        output_filename (str): Name of cleaned CSV.

    Returns:
        pd.DataFrame: Cleaned, structured DataFrame.
    """
    print("\n--- Starting Data Preprocessing ---")
    data = df.copy()

    # Step 1: Clean column names
    data = clean_column_names(data)
    print(f"[INFO] Cleaned columns: {list(data.columns)}")

    # Step 2: Identify and handle missing values
    initial_rows = len(data)
    null_counts = data.isnull().sum()
    print(f"[INFO] Missing values before cleaning:\n{null_counts[null_counts > 0]}")

    # Drop entirely blank rows
    data.dropna(how="all", inplace=True)
    rows_dropped = initial_rows - len(data)
    print(f"[INFO] Dropped {rows_dropped} completely empty rows.")

    # Any remaining nulls in critical columns
    data.dropna(subset=["Estimated_Unemployment_Rate_Pct", "Date", "Region"], inplace=True)

    # Step 3: Check and handle duplicates
    dup_count = data.duplicated().sum()
    if dup_count > 0:
        print(f"[INFO] Found {dup_count} duplicate rows; removing duplicates.")
        data.drop_duplicates(inplace=True)
    else:
        print("[INFO] No duplicate rows detected.")

    # Step 4: Strip string columns
    for col in data.select_dtypes(include="object").columns:
        data[col] = data[col].astype(str).str.strip()

    # Step 5: Convert Date to datetime format (dayfirst=True for DD-MM-YYYY format)
    data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)
    print(f"[INFO] Date range: {data['Date'].min().strftime('%Y-%m-%d')} to {data['Date'].max().strftime('%Y-%m-%d')}")

    # Step 6: Feature Engineering (Temporal and COVID-19 categorization)
    data["Year"] = data["Date"].dt.year
    data["Month"] = data["Date"].dt.month
    data["Month_Name"] = data["Date"].dt.strftime("%b")

    # Define analytical COVID periods:
    # Pre-COVID: 2019 (May 2019 - Dec 2019) and early 2020 prior to national lockdown (Jan-Feb 2020)
    # COVID Period: March 2020 onward (National lockdown announced late March 2020)
    def assign_covid_period(date):
        if date < pd.Timestamp("2020-03-01"):
            return "Pre-COVID"
        else:
            return "COVID-19 Period"

    data["COVID_Period"] = data["Date"].apply(assign_covid_period)

    # Step 7: Validation check
    assert (data["Estimated_Unemployment_Rate_Pct"] >= 0).all(), "Negative unemployment rate found!"
    assert (data["Estimated_Labour_Participation_Rate_Pct"] <= 100).all(), "Invalid participation rate > 100%!"

    # Sort sequentially
    data.sort_values(by=["Date", "Region"], inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Step 8: Save cleaned dataset
    if save_cleaned:
        project_root = get_project_root()
        output_dir = project_root / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename
        data.to_csv(output_path, index=False)
        print(f"[INFO] Cleaned dataset saved to: {output_path}")

    print(f"[INFO] Preprocessing complete. Final shape: {data.shape}")
    return data


if __name__ == "__main__":
    from .data_loader import load_raw_data
    raw = load_raw_data()
    cleaned = preprocess_unemployment_data(raw)
    print(cleaned.head())
