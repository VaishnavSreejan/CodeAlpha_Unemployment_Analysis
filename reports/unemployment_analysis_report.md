# Comprehensive Research Report: Unemployment Analysis in India (2019–2020)

**Project Name:** Unemployment Analysis with Python  
**Internship Organization:** CodeAlpha (Virtual Internship - Task 2)  
**Author:** Data Science Intern  
**Repository:** `CodeAlpha_Unemployment_Analysis`  
**Date:** October 2026  

---

## 1. Executive Summary

This study conducts a rigorous exploratory data analysis (EDA) of monthly unemployment trends in India between **May 2019 and June 2020**, with particular emphasis on the socioeconomic shock induced by the COVID-19 pandemic and subsequent national lockdowns. Utilizing empirical survey datasets covering 28 Indian States and Union Territories across both Rural and Urban divisions, we uncover significant temporal spikes, sectoral vulnerabilities, and marked inter-state disparities.

### Key Highlights
- **Overall Baseline:** The nationwide average estimated unemployment rate stood at **11.79%** (median: **8.35%**) over the full 14-month observation window.
- **Lockdown Peak:** The national monthly average reached an unprecedented peak of **24.88% in May 2020**, with the highest single observation of **76.74%** recorded in Puducherry (Urban) during April 2020.
- **COVID-19 Shift:** The average unemployment rate surged from **9.51%** in the Pre-COVID period (May 2019 – Feb 2020) to **17.77%** during the COVID-19 lockdown period (Mar 2020 – Jun 2020), representing an absolute increase of **+8.26 percentage points** and an **+86.91% relative surge**.
- **Sectoral Impact:** Urban unemployment averaged **13.17%** compared to **10.32%** in rural economies, reflecting sharper service-sector disruption in metropolitan centers.

---

## 2. Dataset Overview & Data Cleaning Methodology

### 2.1 Dataset Provenance & Characteristics
The primary dataset (`unemployment.csv` / `Unemployment in India.csv`) comprises monthly labor market metrics released through survey observations across Indian states.

| Metric / Dimension | Specification |
| :--- | :--- |
| **Observation Window** | 31-May-2019 to 30-June-2020 (14 months) |
| **Raw Records** | 768 rows, 7 columns |
| **Geographic Coverage** | 28 States / Union Territories |
| **Area Disaggregation** | Rural and Urban segments |
| **Target Variables** | Estimated Unemployment Rate (%), Estimated Employed, Estimated Labour Participation Rate (%) |

### 2.2 Data Cleaning & Integrity Safeguards
Raw labor survey data typically suffer from survey padding and format irregularities. The following steps were executed in `src/preprocessing.py`:

1. **Header Sanitization:** Leading/trailing whitespaces in column names (e.g., `' Date'` $\rightarrow$ `'Date'`, `' Estimated Unemployment Rate (%)'` $\rightarrow$ `'Estimated_Unemployment_Rate_Pct'`) were systematically stripped and standardized.
2. **Blank Record Pruning:** 28 completely blank trailing records (`NaN` across all columns) were identified and dropped, yielding a clean corpus of **740 valid observations**.
3. **Categorical Normalization:** Text variables (`Region`, `Area`, `Frequency`) were trimmed of whitespace.
4. **Temporal Transformation:** The `Date` field was converted into standard `datetime64[ns]` format. Features for `Year`, `Month`, `Month_Name`, and `COVID_Period` were engineered.
5. **Boundary Validation:** Assertions confirmed all unemployment rates remained within valid positive boundaries ($[0\%, 100\%]$) and participation rates did not exceed physical limits.
6. **Persistence:** The clean DataFrame was exported to `outputs/cleaned_unemployment_data.csv`.

---

## 3. Summary Statistics

The quantitative distribution of labor market indicators across all 740 observations:

| Metric | Estimated Unemployment Rate (%) | Estimated Employed | Estimated Labour Participation Rate (%) |
| :--- | :---: | :---: | :---: |
| **Count** | 740 | 740 | 740 |
| **Mean** | **11.79%** | 7,204,460 | 42.63% |
| **Standard Deviation** | 10.72% | 8,087,988 | 8.11% |
| **Median** | **8.35%** | 4,744,178 | 41.16% |
| **Min** | 0.00% | 49,420 | 13.33% |
| **25th Percentile (Q1)** | 4.66% | 1,190,404 | 38.06% |
| **75th Percentile (Q3)** | 15.89% | 11,275,490 | 45.50% |
| **Interquartile Range (IQR)** | 11.23% | 10,085,085 | 7.44% |
| **Max** | **76.74%** | 45,777,509 | 72.57% |

*Interpretation:* The mean (11.79%) exceeds the median (8.35%) substantially, indicating a pronounced right-skewed distribution driven by extreme unemployment spikes during April and May 2020.

---

## 4. Empirical Findings & Detailed Analysis

### 4.1 Temporal Evolution and the COVID-19 Lockdown Shock
The monthly trajectory displays baseline stability throughout 2019 (fluctuating between 8.87% and 11.10%), followed by an unprecedented disruption in the spring of 2020:

- **Pre-Shock Low:** Lowest average monthly unemployment occurred in **May 2019 (8.87%)**.
- **The Shock (March 2020):** Jumped to **10.70%** as initial preventative restrictions were introduced.
- **The Acute Crisis (April–May 2020):** National average surged to **22.99% in April 2020** and peaked at **24.88% in May 2020**.
- **Gradual Reopening (June 2020):** Subsided to **11.90%** as lockdown measures began phased easing ("Unlock 1.0").

![Unemployment Trend Over Time](../outputs/plots/1_unemployment_trend_over_time.png)

---

### 4.2 Regional & Inter-State Disparities
Significant structural divergence exists across Indian states. The top 5 highest and lowest average unemployment states:

#### Top 5 States with Highest Average Unemployment Rates:
1. **Tripura:** 28.35% (Peak: 43.64%)
2. **Haryana:** 26.28% (Peak: 46.89%)
3. **Jharkhand:** 20.58% (Peak: 70.17%)
4. **Bihar:** 18.92% (Peak: 58.77%)
5. **Himachal Pradesh:** 18.54% (Peak: 50.00%)

#### Top 5 States with Lowest Average Unemployment Rates:
1. **Meghalaya:** 4.80% (Min: 0.24%)
2. **Odisha:** 5.66% (Min: 1.78%)
3. **Assam:** 6.43% (Min: 0.00%)
4. **Uttarakhand:** 6.58% (Min: 1.63%)
5. **Gujarat:** 6.66% (Min: 1.41%)

![Statewise Unemployment Rate](../outputs/plots/2_statewise_unemployment_rate.png)

---

### 4.3 Sectoral Comparison: Rural vs. Urban Economies

The dataset reveals distinct dynamics between rural and urban sectors:
- **Urban Unemployment:** Mean of **13.17%** (Median: 9.92%, Std: 11.19%)
- **Rural Unemployment:** Mean of **10.32%** (Median: 7.39%, Std: 10.04%)

![Area Wise Boxplot](../outputs/plots/4_area_wise_boxplot.png)

*Analytical Insight:* Urban employment in India is heavily reliant on informal services, daily wage labor, hospitality, construction, and manufacturing. These sectors experienced sudden stoppages during mobility lockdowns. Rural labor markets, anchored by agricultural cycles and local employment safety nets (e.g., MGNREGA), demonstrated higher resilience.

---

### 4.4 COVID-19 Period Analysis (Pre-COVID vs. COVID Period)

To isolate the structural disruption, we divided the timeline into two analytical windows:
- **Pre-COVID Window:** May 2019 – February 2020 (10 months)
- **COVID-19 Window:** March 2020 – June 2020 (4 months)

| Demographic Segment | Pre-COVID Mean (%) | COVID-19 Period Mean (%) | Absolute Increase (pts) | Relative Increase (%) |
| :--- | :---: | :---: | :---: | :---: |
| **All India Overall** | **9.51%** | **17.77%** | **+8.26%** | **+86.91%** |
| **Rural India** | 8.09% | 16.18% | +8.09% | +99.90% |
| **Urban India** | 10.84% | 19.28% | +8.43% | +77.79% |

![COVID Impact Comparison](../outputs/plots/5_covid_impact_comparison.png)

*Important Analytical Caveat:* Observed changes do not automatically prove that COVID-19 was the sole driver of all labor shifts. Broader macroeconomic conditions, pre-existing credit slowdowns, and seasonal agricultural cycles also influenced these figures simultaneously.

---

### 4.5 Heatmap Analysis: Monthly Regional Heatmap

The matrix of States across calendar months demonstrates how the lockdown created a synchronized nationwide shock across almost every state during April and May 2020, with northern and eastern industrial states experiencing the steepest heat signatures.

![Monthly Heatmap](../outputs/plots/6_monthly_unemployment_heatmap.png)

---

## 5. Concrete Numerical Key Findings

1. **National Mean:** Over the 14-month survey, India's average unemployment rate was **11.79%**, with a right-skewed median of **8.35%**.
2. **Single Observation Extremes:** The maximum observed rate was **76.74% in Puducherry (Urban)** in April 2020; the minimum was **0.00% in Puducherry** in May 2019.
3. **National Peak Shock:** Monthly nationwide average unemployment peaked at **24.88% in May 2020**, up from **8.87% in May 2019**.
4. **COVID-19 Surge:** Average unemployment rose from **9.51%** Pre-COVID to **17.77%** during the COVID-19 window (+8.26 percentage points, +86.91% surge).
5. **Urban Vulnerability:** Urban unemployment (**13.17%**) consistently outpaced rural unemployment (**10.32%**).
6. **Inter-State Variance:** Average state unemployment ranged from a high of **28.35% in Tripura** to a low of **4.80% in Meghalaya**.

---

## 6. Economic & Social Policy Suggestions

The empirical insights suggest the following policy directions:

1. **Urban Social Safety Nets:** While rural India benefits from employment guarantee programs like MGNREGA, urban centers lack an equivalent institutional buffer. Establishing a dedicated Urban Employment Guarantee Scheme would mitigate acute distress for daily wage earners.
2. **Emergency Direct Benefit Transfers (DBTs):** The sharp contraction in informal sector employment highlights the necessity for rapid digital cash transfers to maintain consumption floors during systemic shocks.
3. **MSME Credit Liquidity:** Small businesses and local enterprises experienced cash flow cessations. Targeted working capital relief is critical to prevent permanent business closures.
4. **Regional Industrial Development:** The sustained high unemployment in states like Haryana, Jharkhand, and Bihar calls for long-term regional industrial policy and skill development initiatives.

---

## 7. Limitations & Recommendations for Future Research

- **Temporal Coverage:** The primary dataset terminates in June 2020. Incorporating subsequent years (2021–2023) would enable evaluation of medium-term economic scarring and post-lockdown labor force recovery.
- **Sample Representation:** Survey estimates reflect high-frequency sample panels; cross-validation with Periodic Labour Force Survey (PLFS) official statistics provides further ground-truthing.
- **Informality Disaggregation:** The data does not separate formal salaried positions from informal gig work; capturing sector-specific employment shifts remains an important avenue for future research.

---
*Report generated for CodeAlpha Task 2 Data Science Virtual Internship.*
