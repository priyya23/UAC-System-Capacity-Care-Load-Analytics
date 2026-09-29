# UAC System Capacity & Care Load Analytics

## Project Report

**Project Title:** System Capacity & Care Load Analytics for Unaccompanied Children  
**Project Type:** Data Analytics & Dashboard Project  
**Dataset Size:** 720 observations  
**Original Dataset Columns:** 14  
**Tools:** Python, Pandas, Matplotlib, Streamlit, Jupyter Notebook, VS Code

---

## 1. Executive Summary

The **UAC System Capacity & Care Load Analytics** project analyzes the movement and care load of Unaccompanied Children (UAC) through the U.S. care pipeline.

The analysis focuses on two major stages:

1. Children in CBP custody
2. Children receiving care through HHS

Historical time-series data was used to understand system load, intake pressure, transfers, discharges, and periods of unusually high system demand.

Additional analytical features were created, including:

- Total System Load
- Net Intake Pressure
- Care Load Growth Rate
- Discharge Offset Ratio
- 7-observation rolling average
- 14-observation rolling average
- High Load Flag
- Cumulative Net Intake

A Streamlit dashboard provides an interactive view of the analytical results.

---

## 2. Project Overview

The UAC care system can be viewed as a dynamic pipeline:

**CBP Custody → HHS Care → Discharge / Sponsor Placement**

Children move through several stages, and the number entering, remaining within, and leaving the system changes over time.

Understanding these changes provides visibility into:

- System workload
- Care demand
- Intake pressure
- Discharge activity
- High-load periods
- Changes in CBP and HHS populations

---

## 3. Problem Statement

The UAC system may experience changes in the number of children requiring custody and care. A sudden increase in arrivals or transfers can increase operational pressure, while changes in discharge activity can change the number of children remaining in the system.

This project transforms historical UAC data into analytical measures that describe system capacity and care load over time.

---

## 4. Project Objectives

The main objectives are:

- Analyze UAC system activity over time.
- Compare children in CBP custody with children in HHS care.
- Calculate Total System Load.
- Calculate Net Intake Pressure.
- Analyze care-load growth and discharge activity.
- Identify high-load periods.
- Calculate rolling averages and cumulative measures.
- Create visualizations for major system indicators.
- Develop an interactive Streamlit dashboard.
- Produce a reusable analytical dataset.

---

## 5. Dataset Description

The original dataset contains:

- **720 observations**
- **14 original columns**

The dataset includes observations related to children in CBP custody, transfers out of CBP custody, children in HHS care, and HHS discharges.

### Important Variables

| Variable | Description |
|---|---|
| `Date` | Observation date |
| `Children apprehended and placed in CBP custody*` | Number of children entering CBP custody |
| `Children in CBP custody` | Children currently in CBP custody |
| `Children transferred out of CBP custody` | Children transferred from CBP |
| `Children in HHS Care` | Children currently receiving HHS care |
| `Children discharged from HHS Care` | Children leaving HHS care |

---

## 6. Data Preparation

The following data preparation steps were performed:

1. Loaded the dataset using Pandas.
2. Converted the `Date` column to datetime format.
3. Checked numerical columns for invalid values.
4. Checked for missing values.
5. Checked for duplicate observations.
6. Checked for unexpected negative values.
7. Sorted the dataset chronologically.
8. Created analytical features.
9. Saved the final analytical dataset.

---

## 7. Time-Series Observation Analysis

The dataset does not contain an observation for every calendar day.

The average gap between observations was:

**1.49 days**

The largest observed gap was:

**10 days**

Because observations are not perfectly evenly spaced, rolling averages were calculated using observation counts rather than assuming that every observation represents exactly one calendar day.

---

## 8. Feature Engineering

Several analytical features were created from the original dataset.

### 8.1 Total System Load

Total System Load represents the combined number of children in CBP custody and HHS care.

**Formula:**

```text
Total System Load =
Children in CBP custody + Children in HHS Care