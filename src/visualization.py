"""
Data Visualization Module for Unemployment Analysis
CodeAlpha Task 2 - Data Science Internship

Generates high-resolution statistical visualizations using Matplotlib and Seaborn.
Saves all charts inside 'outputs/plots/' directory.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from .data_loader import get_project_root


# Set global aesthetics
def setup_plotting_style():
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "bold",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 16,
        "figure.titleweight": "bold",
        "figure.autolayout": True
    })


def get_plots_dir() -> Path:
    plots_dir = get_project_root() / "outputs" / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    return plots_dir


def plot_unemployment_trend(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """1. Line Chart: National Unemployment Trend Over Time with COVID-19 Lockdown Marker."""
    setup_plotting_style()
    fig, ax = plt.subplots(figsize=(12, 6))

    # Monthly aggregation
    monthly_trend = df.groupby("Date")["Estimated_Unemployment_Rate_Pct"].mean().reset_index()

    ax.plot(
        monthly_trend["Date"],
        monthly_trend["Estimated_Unemployment_Rate_Pct"],
        marker="o",
        linewidth=2.5,
        color="#1f77b4",
        label="Monthly Mean Unemployment Rate (%)"
    )

    # Shading COVID-19 Lockdown Shock Period (March 2020 onward)
    lockdown_start = pd.Timestamp("2020-03-24")
    ax.axvspan(pd.Timestamp("2020-03-01"), df["Date"].max(), color="#ff7f0e", alpha=0.15, label="COVID-19 Period")

    # Annotate lockdown onset
    ax.axvline(lockdown_start, color="#d62728", linestyle="--", linewidth=1.5, label="Lockdown Imposed (24-Mar-2020)")

    # Annotate peak
    peak_idx = monthly_trend["Estimated_Unemployment_Rate_Pct"].idxmax()
    peak_date = monthly_trend.loc[peak_idx, "Date"]
    peak_val = monthly_trend.loc[peak_idx, "Estimated_Unemployment_Rate_Pct"]
    ax.annotate(
        f"Peak Shock: {peak_val:.1f}%\n({peak_date.strftime('%b %Y')})",
        xy=(peak_date, peak_val),
        xytext=(peak_date - pd.Timedelta(days=70), peak_val + 2),
        arrowprops=dict(facecolor="#d62728", shrink=0.08, width=1.5, headwidth=8),
        fontweight="bold",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="#ffebee", ec="#d62728")
    )

    ax.set_title("National Unemployment Rate Trend in India (2019 - 2020)")
    ax.set_xlabel("Timeline (Month - Year)")
    ax.set_ylabel("Unemployment Rate (%)")
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", frameon=True)

    if save:
        path = get_plots_dir() / "1_unemployment_trend_over_time.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"[PLOT] Saved: {path.name}")
    return fig


def plot_regional_comparison(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """2. Bar Chart: Average Unemployment Rates Across Indian States."""
    setup_plotting_style()
    state_avg = (
        df.groupby("Region")["Estimated_Unemployment_Rate_Pct"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 11))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(state_avg)))

    bars = ax.barh(state_avg["Region"], state_avg["Estimated_Unemployment_Rate_Pct"], color=colors, edgecolor="black", alpha=0.85)

    # Add data values on top of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.3,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.1f}%",
            va="center",
            ha="left",
            fontsize=8.5,
            fontweight="bold"
        )

    # National average dashed line
    national_mean = df["Estimated_Unemployment_Rate_Pct"].mean()
    ax.axvline(national_mean, color="#d62728", linestyle="--", linewidth=1.8, label=f"National Average ({national_mean:.1f}%)")

    ax.set_title("Average Unemployment Rate by State / Union Territory in India")
    ax.set_xlabel("Average Estimated Unemployment Rate (%)")
    ax.set_ylabel("State / Region")
    ax.set_xlim(0, state_avg["Estimated_Unemployment_Rate_Pct"].max() + 5)
    ax.legend(loc="lower right", frameon=True)

    if save:
        path = get_plots_dir() / "2_statewise_unemployment_rate.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"[PLOT] Saved: {path.name}")
    return fig


def plot_distribution(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """3. Histogram and KDE: Distribution of Unemployment Rates."""
    setup_plotting_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    rates = df["Estimated_Unemployment_Rate_Pct"].dropna()
    mean_val = rates.mean()
    median_val = rates.median()

    sns.histplot(rates, kde=True, bins=30, color="#2b5c8f", ax=ax, edgecolor="white", alpha=0.6)

    ax.axvline(mean_val, color="#d62728", linestyle="--", linewidth=2, label=f"Mean: {mean_val:.2f}%")
    ax.axvline(median_val, color="#2ca02c", linestyle="-.", linewidth=2, label=f"Median: {median_val:.2f}%")

    ax.set_title("Distribution of Estimated Unemployment Rates in India")
    ax.set_xlabel("Estimated Unemployment Rate (%)")
    ax.set_ylabel("Frequency (Count)")
    ax.legend(frameon=True)

    if save:
        path = get_plots_dir() / "3_unemployment_rate_distribution.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"[PLOT] Saved: {path.name}")
    return fig


def plot_area_boxplot(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """4. Box Plot: Spread of Unemployment Rates by Area (Rural vs Urban)."""
    setup_plotting_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    if "Area" in df.columns:
        sns.boxplot(
            data=df,
            x="Area",
            y="Estimated_Unemployment_Rate_Pct",
            hue="Area",
            legend=False,
            palette=["#4e79a7", "#e15759"],
            ax=ax,
            width=0.45,
            boxprops=dict(alpha=0.85)
        )
        sns.stripplot(
            data=df,
            x="Area",
            y="Estimated_Unemployment_Rate_Pct",
            color="black",
            alpha=0.25,
            jitter=0.2,
            size=4,
            ax=ax
        )
        ax.set_title("Spread and Disparity of Unemployment Rate: Rural vs Urban")
        ax.set_xlabel("Area Category")
        ax.set_ylabel("Estimated Unemployment Rate (%)")
    else:
        sns.boxplot(
            data=df,
            y="Estimated_Unemployment_Rate_Pct",
            color="#4e79a7",
            ax=ax
        )
        ax.set_title("Overall Spread of Unemployment Rates")
        ax.set_ylabel("Estimated Unemployment Rate (%)")

    if save:
        path = get_plots_dir() / "4_area_wise_boxplot.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"[PLOT] Saved: {path.name}")
    return fig


def plot_covid_comparison(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """5. COVID-Period Comparison Chart: Pre-COVID vs COVID-19 Period Rates."""
    setup_plotting_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Overall comparison bar chart
    covid_agg = df.groupby("COVID_Period")["Estimated_Unemployment_Rate_Pct"].agg(["mean", "median"]).reset_index()
    palette = {"Pre-COVID": "#2ca02c", "COVID-19 Period": "#d62728"}

    bars = ax1.bar(covid_agg["COVID_Period"], covid_agg["mean"], color=[palette[p] for p in covid_agg["COVID_Period"]], width=0.45, edgecolor="black")
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.3, f"{h:.2f}%", ha="center", va="bottom", fontweight="bold", fontsize=11)

    abs_diff = covid_agg.loc[covid_agg["COVID_Period"] == "COVID-19 Period", "mean"].values[0] - covid_agg.loc[covid_agg["COVID_Period"] == "Pre-COVID", "mean"].values[0]
    pct_rise = (abs_diff / covid_agg.loc[covid_agg["COVID_Period"] == "Pre-COVID", "mean"].values[0]) * 100
    ax1.set_title(f"Average Rate Comparison\n(+{abs_diff:.2f} percentage points / +{pct_rise:.1f}%)")
    ax1.set_ylabel("Mean Unemployment Rate (%)")
    ax1.set_ylim(0, max(covid_agg["mean"]) + 5)

    # Sub-breakdown by Area (Rural vs Urban) across periods
    if "Area" in df.columns:
        sns.barplot(
            data=df,
            x="Area",
            y="Estimated_Unemployment_Rate_Pct",
            hue="COVID_Period",
            palette=palette,
            ax=ax2,
            edgecolor="black"
        )
        ax2.set_title("Impact by Demographic Sector: Rural vs Urban")
        ax2.set_ylabel("Mean Unemployment Rate (%)")
        ax2.legend(title="Period", frameon=True)
    else:
        sns.violinplot(
            data=df,
            x="COVID_Period",
            y="Estimated_Unemployment_Rate_Pct",
            palette=palette,
            ax=ax2
        )
        ax2.set_title("Rate Distribution Shift")

    if save:
        path = get_plots_dir() / "5_covid_impact_comparison.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"[PLOT] Saved: {path.name}")
    return fig


def plot_monthly_heatmap(df: pd.DataFrame, save: bool = True) -> plt.Figure:
    """6. Heatmap: State vs Month Unemployment Rate Patterns."""
    setup_plotting_style()
    fig, ax = plt.subplots(figsize=(14, 12))

    # Format Date as Month-Year chronological string
    df_temp = df.copy()
    df_temp["Month_Year"] = df_temp["Date"].dt.strftime("%Y-%m")

    # Pivot table: Index=Region, Columns=Month_Year, Values=Estimated_Unemployment_Rate_Pct
    pivot_data = df_temp.pivot_table(
        index="Region",
        columns="Month_Year",
        values="Estimated_Unemployment_Rate_Pct",
        aggfunc="mean"
    )

    sns.heatmap(
        pivot_data,
        cmap="YlOrRd",
        linewidths=0.5,
        linecolor="#efefef",
        cbar_kws={"label": "Unemployment Rate (%)"},
        ax=ax
    )

    ax.set_title("Heatmap: Monthly Unemployment Rate Across Indian States (2019 - 2020)")
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("State / Region")
    plt.xticks(rotation=45, ha="right")

    if save:
        path = get_plots_dir() / "6_monthly_unemployment_heatmap.png"
        fig.savefig(path, dpi=300, bbox_inches="tight")
        print(f"[PLOT] Saved: {path.name}")
    return fig


def generate_all_visualizations(df: pd.DataFrame) -> None:
    """Generates and saves all 6 standard project visualizations."""
    print("\n--- Generating Project Visualizations ---")
    plot_unemployment_trend(df)
    plot_regional_comparison(df)
    plot_distribution(df)
    plot_area_boxplot(df)
    plot_covid_comparison(df)
    plot_monthly_heatmap(df)
    print("[INFO] All visualizations successfully generated and saved to 'outputs/plots/'.")
