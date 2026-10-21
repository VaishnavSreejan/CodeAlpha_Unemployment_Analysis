"""
CodeAlpha Task 2: Unemployment Analysis with Python
Source package initialization.
"""

from .data_loader import load_raw_data
from .preprocessing import preprocess_unemployment_data
from .analysis import (
    calculate_summary_statistics,
    analyze_trends_over_time,
    analyze_regional_differences,
    analyze_area_differences,
    analyze_covid_impact,
    generate_key_findings
)
from .visualization import (
    plot_unemployment_trend,
    plot_regional_comparison,
    plot_distribution,
    plot_area_boxplot,
    plot_covid_comparison,
    plot_monthly_heatmap,
    generate_all_visualizations
)

__all__ = [
    "load_raw_data",
    "preprocess_unemployment_data",
    "calculate_summary_statistics",
    "analyze_trends_over_time",
    "analyze_regional_differences",
    "analyze_area_differences",
    "analyze_covid_impact",
    "generate_key_findings",
    "plot_unemployment_trend",
    "plot_regional_comparison",
    "plot_distribution",
    "plot_area_boxplot",
    "plot_covid_comparison",
    "plot_monthly_heatmap",
    "generate_all_visualizations",
]
