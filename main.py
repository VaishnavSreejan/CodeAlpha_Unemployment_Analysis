"""
Main Program: Unemployment Analysis with Python
CodeAlpha Task 2 - Data Science Internship

Author: CodeAlpha Intern
Project Name: Unemployment Analysis with Python
Repository: CodeAlpha_Unemployment_Analysis

Executes the end-to-end data science pipeline:
1. Load raw dataset
2. Clean and preprocess data
3. Perform exploratory data analysis and statistical computation
4. Generate and save professional visualizations
5. Export cleaned dataset and key findings report
"""

import sys
from pathlib import Path

# Add project root to path for direct invocation
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data_loader import load_raw_data
from src.preprocessing import preprocess_unemployment_data
from src.analysis import (
    calculate_summary_statistics,
    analyze_trends_over_time,
    analyze_regional_differences,
    analyze_area_differences,
    analyze_covid_impact,
    generate_key_findings
)
from src.visualization import generate_all_visualizations


def main():
    print("=" * 80)
    print("       CODEALPHA INTERNSHIP TASK 2: UNEMPLOYMENT ANALYSIS WITH PYTHON       ")
    print("=" * 80)

    # 1. Load Raw Data
    try:
        raw_df = load_raw_data("unemployment.csv")
    except Exception as e:
        print(f"[FATAL] Failed to load data: {e}")
        sys.exit(1)

    # 2. Preprocess & Clean Data
    cleaned_df = preprocess_unemployment_data(raw_df, save_cleaned=True)

    # 3. Exploratory Data Analysis & Statistics
    print("\n--- Summary Statistics ---")
    summary_stats = calculate_summary_statistics(cleaned_df)
    print(summary_stats.to_string())

    print("\n--- COVID-19 Period Impact Analysis ---")
    covid_impact = analyze_covid_impact(cleaned_df)
    print(f"Pre-COVID Average Unemployment Rate:    {covid_impact['Pre_COVID_Mean']}%")
    print(f"COVID-19 Period Average Rate:           {covid_impact['COVID_Period_Mean']}%")
    print(f"Absolute Rate Surge:                    +{covid_impact['Absolute_Difference']} percentage points")
    print(f"Relative Percentage Spike:              +{covid_impact['Percentage_Change']}%")

    if covid_impact["Area_Breakdown"]:
        print("\nArea-wise COVID Impact Breakdown:")
        for area, vals in covid_impact["Area_Breakdown"].items():
            print(f"  - {area:6s}: Pre={vals.get('Pre-COVID')}% -> COVID={vals.get('COVID-19 Period')}% (Shift: +{vals.get('Abs_Increase')} pts, +{vals.get('Pct_Increase')}%)")

    # State-level extremes
    state_summary, top_5, low_5 = analyze_regional_differences(cleaned_df)
    print("\n--- Top 5 States with Highest Average Unemployment ---")
    print(top_5[["Region", "Mean_Unemployment_Rate", "Max_Rate"]].to_string(index=False))

    print("\n--- Top 5 States with Lowest Average Unemployment ---")
    print(low_5[["Region", "Mean_Unemployment_Rate", "Min_Rate"]].to_string(index=False))

    # 4. Generate Visualizations
    generate_all_visualizations(cleaned_df)

    # 5. Generate and Save Key Findings
    findings = generate_key_findings(cleaned_df, save_findings=True)
    print("\n" + findings)

    # 6. Summary of Output Locations
    print("=" * 80)
    print(" PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
    print(" Outputs Generated:")
    print(f"  1. Cleaned Dataset:  outputs/cleaned_unemployment_data.csv")
    print(f"  2. Key Findings:     outputs/key_findings.txt")
    print(f"  3. Visualizations:   outputs/plots/ (6 PNG files at 300 DPI)")
    print(f"  4. Research Report:  reports/unemployment_analysis_report.md")
    print(f"  5. Jupyter Notebook: notebooks/unemployment_analysis.ipynb")
    print("=" * 80)


if __name__ == "__main__":
    main()
