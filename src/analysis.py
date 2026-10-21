"""
Statistical Analysis Module for Unemployment Analysis
CodeAlpha Task 2 - Data Science Internship

Performs statistical analysis, time-trend evaluations, regional comparisons,
COVID-19 impact calculations, and generates key numerical findings.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from .data_loader import get_project_root


def calculate_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes overall statistical metrics (Mean, Median, Std, Min, Max, IQR)
    for numeric indicators.
    """
    numeric_cols = [
        "Estimated_Unemployment_Rate_Pct",
        "Estimated_Employed",
        "Estimated_Labour_Participation_Rate_Pct"
    ]
    present_cols = [col for col in numeric_cols if col in df.columns]

    stats_dict = {}
    for col in present_cols:
        series = df[col].dropna()
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        stats_dict[col] = {
            "Count": len(series),
            "Mean": round(series.mean(), 2),
            "Std_Dev": round(series.std(), 2),
            "Median": round(series.median(), 2),
            "Min": round(series.min(), 2),
            "Q25 (25%)": round(q25, 2),
            "Q75 (75%)": round(q75, 2),
            "IQR": round(q75 - q25, 2),
            "Max": round(series.max(), 2),
        }
    return pd.DataFrame(stats_dict)


def analyze_trends_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates average monthly unemployment rate across India over time.
    """
    trend = (
        df.groupby("Date")
        .agg(
            Avg_Unemployment_Rate=("Estimated_Unemployment_Rate_Pct", "mean"),
            Median_Unemployment_Rate=("Estimated_Unemployment_Rate_Pct", "median"),
            Avg_Participation_Rate=("Estimated_Labour_Participation_Rate_Pct", "mean"),
            Total_Employed_Sample=("Estimated_Employed", "sum")
        )
        .reset_index()
    )
    trend["Date_Label"] = trend["Date"].dt.strftime("%b %Y")
    return trend


def analyze_regional_differences(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Analyzes state-wise unemployment differences.
    Returns:
        (full_state_summary, top_5_highest, top_5_lowest)
    """
    state_summary = (
        df.groupby("Region")["Estimated_Unemployment_Rate_Pct"]
        .agg(["count", "mean", "median", "min", "max", "std"])
        .reset_index()
        .rename(columns={
            "mean": "Mean_Unemployment_Rate",
            "median": "Median_Unemployment_Rate",
            "min": "Min_Rate",
            "max": "Max_Rate",
            "std": "Std_Dev"
        })
        .sort_values(by="Mean_Unemployment_Rate", ascending=False)
    )
    state_summary["Mean_Unemployment_Rate"] = state_summary["Mean_Unemployment_Rate"].round(2)
    state_summary["Median_Unemployment_Rate"] = state_summary["Median_Unemployment_Rate"].round(2)

    top_5_highest = state_summary.head(5).copy()
    top_5_lowest = state_summary.tail(5).copy()
    return state_summary, top_5_highest, top_5_lowest


def analyze_area_differences(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes unemployment rate differences between Rural and Urban areas (if 'Area' column exists).
    """
    if "Area" not in df.columns:
        return pd.DataFrame()

    area_summary = (
        df.groupby("Area")["Estimated_Unemployment_Rate_Pct"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .reset_index()
        .rename(columns={
            "mean": "Mean_Unemployment_Rate",
            "median": "Median_Unemployment_Rate",
            "std": "Std_Dev",
            "min": "Min_Rate",
            "max": "Max_Rate"
        })
    )
    area_summary["Mean_Unemployment_Rate"] = area_summary["Mean_Unemployment_Rate"].round(2)
    area_summary["Median_Unemployment_Rate"] = area_summary["Median_Unemployment_Rate"].round(2)
    return area_summary


def analyze_covid_impact(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates the statistical difference in unemployment between Pre-COVID and COVID periods.
    """
    pre_covid = df[df["COVID_Period"] == "Pre-COVID"]["Estimated_Unemployment_Rate_Pct"]
    covid_period = df[df["COVID_Period"] == "COVID-19 Period"]["Estimated_Unemployment_Rate_Pct"]

    pre_mean = pre_covid.mean()
    covid_mean = covid_period.mean()
    abs_diff = covid_mean - pre_mean
    pct_change = (abs_diff / pre_mean) * 100 if pre_mean != 0 else 0

    # Monthly breakdown for COVID lockdown impact (April & May 2020 peak shock)
    monthly_trend = df.groupby(["Year", "Month_Name"])["Estimated_Unemployment_Rate_Pct"].mean()

    # Breakdown by Area if present
    area_covid_impact = {}
    if "Area" in df.columns:
        area_group = df.groupby(["Area", "COVID_Period"])["Estimated_Unemployment_Rate_Pct"].mean().unstack()
        if "Pre-COVID" in area_group.columns and "COVID-19 Period" in area_group.columns:
            area_group["Abs_Increase"] = area_group["COVID-19 Period"] - area_group["Pre-COVID"]
            area_group["Pct_Increase"] = (area_group["Abs_Increase"] / area_group["Pre-COVID"]) * 100
            area_covid_impact = area_group.round(2).to_dict(orient="index")

    return {
        "Pre_COVID_Mean": round(pre_mean, 2),
        "Pre_COVID_Median": round(pre_covid.median(), 2),
        "COVID_Period_Mean": round(covid_mean, 2),
        "COVID_Period_Median": round(covid_period.median(), 2),
        "Absolute_Difference": round(abs_diff, 2),
        "Percentage_Change": round(pct_change, 2),
        "Area_Breakdown": area_covid_impact,
    }


def generate_key_findings(df: pd.DataFrame, save_findings: bool = True) -> str:
    """
    Calculates and compiles 5 to 8 evidence-based numerical findings directly from data.
    Saves to 'outputs/key_findings.txt'.
    """
    # 1. Overall Metrics
    overall_mean = df["Estimated_Unemployment_Rate_Pct"].mean()
    overall_median = df["Estimated_Unemployment_Rate_Pct"].median()
    overall_max = df["Estimated_Unemployment_Rate_Pct"].max()
    max_row = df.loc[df["Estimated_Unemployment_Rate_Pct"].idxmax()]
    overall_min = df["Estimated_Unemployment_Rate_Pct"].min()
    min_row = df.loc[df["Estimated_Unemployment_Rate_Pct"].idxmin()]

    # 2. Time Trend Extremes
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Estimated_Unemployment_Rate_Pct"].mean()
    peak_month = monthly.idxmax().strftime("%B %Y")
    peak_month_rate = monthly.max()
    trough_month = monthly.idxmin().strftime("%B %Y")
    trough_month_rate = monthly.min()

    # 3. Regional Extremes
    state_means = df.groupby("Region")["Estimated_Unemployment_Rate_Pct"].mean()
    top_state = state_means.idxmax()
    top_state_rate = state_means.max()
    lowest_state = state_means.idxmin()
    lowest_state_rate = state_means.min()

    # 4. COVID Impact
    covid_res = analyze_covid_impact(df)

    # 5. Rural vs Urban
    area_summary = analyze_area_differences(df)
    urban_mean = area_summary.loc[area_summary["Area"] == "Urban", "Mean_Unemployment_Rate"].values[0] if not area_summary.empty else 0
    rural_mean = area_summary.loc[area_summary["Area"] == "Rural", "Mean_Unemployment_Rate"].values[0] if not area_summary.empty else 0

    findings_text = (
        "================================================================================\n"
        "CODEALPHA TASK 2: UNEMPLOYMENT ANALYSIS - KEY FINDINGS & INSIGHTS\n"
        "================================================================================\n\n"
        f"1. OVERALL NATIONAL UNEMPLOYMENT RATE:\n"
        f"   Across all observations from {df['Date'].min().strftime('%B %Y')} to {df['Date'].max().strftime('%B %Y')}, "
        f"the national average unemployment rate stood at {overall_mean:.2f}%, with a median of {overall_median:.2f}%.\n\n"
        f"2. HIGHEST AND LOWEST RECORDED SINGLE RATES:\n"
        f"   - Peak single observation: {overall_max:.2f}% in {max_row['Region']} ({max_row.get('Area', 'N/A')}) during {max_row['Date'].strftime('%B %Y')}.\n"
        f"   - Minimum single observation: {overall_min:.2f}% in {min_row['Region']} during {min_row['Date'].strftime('%B %Y')}.\n\n"
        f"3. PEAK MONTHLY NATIONAL SHOCK (COVID-19 LOCKDOWN):\n"
        f"   - The national average unemployment rate spiked to its highest monthly level in {peak_month} at {peak_month_rate:.2f}%.\n"
        f"   - In contrast, the lowest monthly national average was recorded in {trough_month} at {trough_month_rate:.2f}%.\n\n"
        f"4. COVID-19 IMPACT (PRE-COVID VS COVID-19 PERIOD):\n"
        f"   - Pre-COVID Average (May 2019 - Feb 2020): {covid_res['Pre_COVID_Mean']}%\n"
        f"   - COVID-19 Period Average (Mar 2020 - Jun 2020): {covid_res['COVID_Period_Mean']}%\n"
        f"   - Absolute Increase: +{covid_res['Absolute_Difference']} percentage points\n"
        f"   - Relative Surge: +{covid_res['Percentage_Change']}% increase in average unemployment rate.\n\n"
        f"5. URBAN VS RURAL DISPARITY:\n"
        f"   - Urban areas suffered higher average unemployment at {urban_mean:.2f}%, compared to {rural_mean:.2f}% in Rural areas.\n"
        f"   - Urban economies experienced sharper lockdown vulnerability due to service-sector closures and dense labor markets.\n\n"
        f"6. REGIONAL AND STATE-LEVEL DISPARITIES:\n"
        f"   - Highest average unemployment rate by state: {top_state} with an average of {top_state_rate:.2f}%.\n"
        f"   - Lowest average unemployment rate by state: {lowest_state} with an average of {lowest_state_rate:.2f}%.\n"
        f"   - Demonstrates marked regional inequality in labor market resilience.\n\n"
        f"7. POLICY IMPLICATIONS & OBSERVATIONAL LIMITATIONS:\n"
        f"   - Urban labor markets require targeted emergency social safety nets and wage subsidy schemes during macroeconomic disruptions.\n"
        f"   - Rural agricultural activity provided partial absorption capacity during lockdowns, but requires continuous formalization.\n"
        f"   - Limitation: These observational data reflect sample survey estimates; changes during 2020 coincide with COVID-19\n"
        f"     containment measures but do not isolate other simultaneous supply-chain and global macroeconomic shifts.\n"
        "================================================================================\n"
    )

    if save_findings:
        project_root = get_project_root()
        findings_path = project_root / "outputs" / "key_findings.txt"
        findings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(findings_path, "w", encoding="utf-8") as f:
            f.write(findings_text)
        print(f"[INFO] Key findings successfully saved to: {findings_path}")

    return findings_text
