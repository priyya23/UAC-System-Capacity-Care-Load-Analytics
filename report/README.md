UAC System Capacity & Care Load Analytics
1. Project Overview

This project analyzes system capacity and care load within the Unaccompanied Children (UAC) care pipeline.

The analysis focuses on children moving through the care process from U.S. Customs and Border Protection (CBP) custody to the U.S. Department of Health and Human Services (HHS) care system and eventual discharge.

The project uses historical data to understand:

System-wide care load
Children in CBP custody
Children in HHS care
Transfers from CBP custody
HHS discharges
Daily net intake pressure
Changes in system load over time
Periods of relatively high system demand

The project combines data cleaning, exploratory data analysis, feature engineering, statistical analysis, trend analysis, and an interactive Streamlit dashboard.

The overall goal is to provide a structured analytical view of system demand and care-load patterns that can support capacity monitoring and further analysis.

2. Project Objectives

The main objectives of this project are:

Analyze the overall UAC system load over time.
Compare children in CBP custody with children in HHS care.
Examine transfers from CBP custody into HHS care.
Analyze HHS discharges.
Measure daily net intake pressure.
Identify periods of relatively high system load.
Study changes and trends in system capacity indicators.
Develop analytical metrics that summarize system pressure.
Create an interactive dashboard for exploring the data.
Create a reusable analytical dataset for further analysis.
3. Project Workflow

The project follows the following analytical workflow:

Raw UAC Dataset
       |
       v
Data Loading
       |
       v
Data Cleaning & Validation
       |
       v
Exploratory Data Analysis
       |
       v
Feature Engineering
       |
       v
Statistical & Trend Analysis
       |
       v
High-Load Identification
       |
       v
Monthly & Time-Based Analysis
       |
       v
Final Analytical Dataset
       |
       v
Streamlit Dashboard
       |
       v
Insights & Reporting
4. Dataset

The project uses historical UAC data containing the following primary fields:

Date
Children apprehended and placed in CBP custody*
Children in CBP custody
Children transferred out of CBP custody
Children in HHS Care
Children discharged from HHS Care

The original dataset contains:

720 observations
14 original columns

The final analytical dataset contains the original fields together with calculated metrics, rolling averages, indicators, and time-based features.

5. Data Preparation

The data preparation process included several steps to ensure that the dataset was suitable for analysis.

5.1 Data Loading

The original CSV dataset was loaded into Python using the Pandas library.

The primary analysis notebook is:

analysis/uac_analysis.ipynb
5.2 Column Cleaning

Column names were reviewed and cleaned to make them easier to use during analysis and feature engineering.

5.3 Date Conversion

The Date field was converted into a proper datetime format so that the observations could be sorted chronologically and analyzed over time.

5.4 Numeric Data Cleaning

The relevant numerical fields were checked and converted into appropriate numeric data types.

5.5 Missing-Value Check

The dataset was examined for missing values in the primary analytical fields.

5.6 Duplicate-Date Check

Dates were checked for duplicate observations to ensure that the time-series analysis was not affected by unintended duplicate records.

5.7 Negative-Value Check

The original numeric fields were checked for negative values because the primary count variables represent numbers of children and should not contain negative observations.

5.8 Chronological Sorting

The observations were sorted by date to ensure that calculations such as growth rates, cumulative measures, and rolling averages were performed in chronological order.

6. Time-Series Observation Analysis

The dataset does not contain an observation for every calendar day.

The average gap between observations was approximately:

1.49 days

The largest observed gap was:

10 days

Because of these gaps, the rolling averages used in the project are defined as observation-based rolling averages rather than exact calendar-day averages.

For example:

7-observation rolling average
14-observation rolling average

This distinction is important when interpreting the time-series results.

7. Feature Engineering

Several analytical features were created from the original dataset to provide additional information about system capacity and care load.

The final analytical dataset includes the following major fields:

Date
Children apprehended and placed in CBP custody*
Children in CBP custody
Children transferred out of CBP custody
Children in HHS Care
Children discharged from HHS Care
transfer_gt_cbp_flag
discharge_gt_hhs_flag
Total System Load
Net Intake Pressure
Care Load Growth Rate
Discharge Offset Ratio
7_Observation_Load_Avg
14_Observation_Load_Avg
Month
Week
High_Load_Flag
High_Load_Group
Cumulative Net Intake
7_Observation_Intake_Avg
14_Observation_Intake_Avg
8. Key Analytical Metrics
8.1 Total System Load

Total System Load represents the combined number of children in CBP custody and HHS care.

Formula
Total System Load =
Children in CBP custody + Children in HHS Care

This metric provides an overall view of the number of children represented within the two major stages of the care pipeline.

8.2 Net Intake Pressure

Net Intake Pressure compares the number of children transferred from CBP custody with the number of children discharged from HHS care.

Formula
Net Intake Pressure =
Children transferred out of CBP custody
-
Children discharged from HHS Care

Interpretation:

A positive value indicates that transfers were greater than discharges for that observation.
A negative value indicates that discharges were greater than transfers.
A value of zero indicates that transfers and discharges were equal.

Net Intake Pressure is used as an analytical indicator of short-term movement pressure within the care pipeline.

8.3 Care Load Growth Rate

Care Load Growth Rate measures the percentage change in Total System Load from one observation to the next.

It provides an indication of whether the overall system load is increasing or decreasing between consecutive observations.

8.4 Discharge Offset Ratio

Discharge Offset Ratio compares HHS discharges with transfers from CBP custody.

Formula
Discharge Offset Ratio =
Children discharged from HHS Care
/
Children transferred out of CBP custody

A ratio greater than 1 indicates that discharges exceeded transfers for that observation.

A ratio below 1 indicates that transfers exceeded discharges.

9. Rolling Averages

The project calculates observation-based rolling averages to smooth short-term fluctuations and highlight broader trends.

The following rolling averages were created:

7-observation Total System Load average
14-observation Total System Load average
7-observation Net Intake Pressure average
14-observation Net Intake Pressure average

Because the dataset contains gaps between some dates, these represent the previous seven or fourteen observations rather than exact seven-day or fourteen-day calendar windows.

10. High-Load Analysis

A high-load indicator was created using the 75th percentile of Total System Load.

Observations at or above the calculated threshold were classified as:

High Load

Other observations were classified as:

Normal Load

This classification is a statistical indicator created specifically for analytical purposes.

It should not be interpreted as an official facility capacity threshold or an official operational definition of system overload.

11. Exploratory Data Analysis

Exploratory Data Analysis was performed to understand patterns and relationships within the dataset.

The analysis focused on:

Total System Load trends
CBP custody trends
HHS care trends
Transfers into HHS care
HHS discharge patterns
Net Intake Pressure
Cumulative Net Intake
Rolling averages
High-load observations
Monthly trends

Visualizations were used to identify changes in system load and differences between transfers and discharges.

12. Key Project Findings
12.1 Highest System Load

The highest observed Total System Load occurred on:

Date: December 20, 2023
Total System Load: 11,762

On this date:

Children in CBP custody: 246
Children in HHS Care: 11,516

HHS care therefore represented the majority of the observed system load on this date.

12.2 Lowest System Load

The lowest observed Total System Load occurred on:

Date: August 24, 2025
Total System Load: 2,002

On this date:

Children in CBP custody: 21
Children in HHS Care: 1,981
12.3 Highest Positive Net Intake Pressure

The highest positive Net Intake Pressure occurred on:

Date: February 12, 2024
Net Intake Pressure: 206

The corresponding values were:

Transfers: 440
Discharges: 234

This means that transfers exceeded discharges by 206 children for that observation.

12.4 Most Negative Net Intake Pressure

The most negative Net Intake Pressure occurred on:

Date: January 11, 2024
Net Intake Pressure: -465

The corresponding values were:

Transfers: 11
Discharges: 476

This means that discharges exceeded transfers by 465 children for that observation.

12.5 Net Intake Pressure Distribution

Across the observations:

Positive observations: 238
Zero observations: 7
Negative observations: 475

This indicates that negative Net Intake Pressure observations were more frequent than positive observations in the analyzed dataset.

12.6 Average Care Load

The average values across the analyzed observations were:

Average CBP custody: 171.49
Average HHS care: 6,061.28
Average Total System Load: 6,232.77

The average HHS care load was substantially larger than the average CBP custody count in the dataset.

12.7 Overall Transfers and Discharges

The total number of recorded transfers was:

92,641

The total number of recorded discharges was:

124,853

The overall discharge-to-transfer ratio was:

1.348

This ratio is calculated across the full set of observations and should be interpreted as an aggregate dataset-level measure rather than a daily capacity measure.

12.8 High-Load Observations

Using the 75th percentile classification described earlier:

High-load observations: 180
Share of observations: 25.0%

The classification identifies approximately one-quarter of the observations as relatively high-load observations based on the selected statistical threshold.

12.9 Highest HHS Care Observation

The highest observed HHS care value was:

Date: December 20, 2023
HHS care: 11,516
12.10 Highest CBP Custody Observation

The highest observed CBP custody value was:

Date: February 4, 2024
CBP custody: 531
13. CBP and HHS System Share

The analysis also examined the relative contribution of CBP custody and HHS care to the overall system load.

The calculated average system shares were:

CBP Share: 2.75%
HHS Share: 97.25%

This shows that, within the analyzed system-load measure, the majority of the observed load was associated with children in HHS care.

These percentages describe the analyzed dataset and should not be interpreted as an official allocation of organizational responsibility or capacity.

14. Dashboard Development

The project includes an interactive dashboard developed using Streamlit.

The dashboard application is located at:

dashboard/app.py

The dashboard was designed to provide an accessible interface for exploring the analytical dataset without requiring users to directly work with the Python analysis notebook.

15. Dashboard Features

The dashboard provides the following analytical sections:

System Load Overview
CBP vs HHS Care Load Comparison
Net Intake and Backlog Trends
Cumulative Net Intake
Transfers vs Discharges
Selected Metric Analysis
Analytical Summary
High Load Periods
Monthly Summary
Dataset Explorer
Filtered CSV Download
16. Dashboard Controls
16.1 Date Range

Users can select a specific date range to examine a particular period of the dataset.

This allows users to focus the analysis on selected periods rather than viewing the complete historical dataset.

16.2 Metric Selection

Users can select different metrics for analysis, including:

Total System Load
Children in CBP custody
Children in HHS Care
Net Intake Pressure
Children transferred out of CBP custody
Children discharged from HHS Care

The selected metric can then be examined over the selected date range.

17. Analytical Dataset

The final analytical dataset was created after completing the data preparation and feature engineering process.

The final dataset includes:

Original UAC measurements
Derived system-load metrics
Intake and discharge metrics
Rolling averages
Cumulative measures
High-load indicators
Time-based features

The final analytical dataset is stored as:

data/uac_final_analysis.csv
18. Monthly Summary

A monthly summary dataset was also created to support higher-level trend analysis.

The monthly summary is stored as:

data/uac_monthly_summary.csv

Monthly aggregation provides an additional way of examining changes in system load and care activity over time.

19. Technologies Used

The project uses the following technologies:

Python

Used for data processing, feature engineering, statistical calculations, and analysis.

Pandas

Used for:

Data loading
Data cleaning
Data transformation
Feature engineering
Aggregation
Exporting analytical datasets
Matplotlib

Used for data visualization and exploratory analysis.

Streamlit

Used to develop the interactive analytical dashboard.

Jupyter Notebook

Used as the primary environment for exploratory analysis and development.

Visual Studio Code

Used for project development, notebook execution, dashboard development, and project file management.

20. Project Structure

The project is organized as follows:

C:\UAC_Project
│
├── README.md
│
├── data
│   ├── uac_data.csv
│   ├── uac_final_analysis.csv
│   └── uac_monthly_summary.csv
│
├── analysis
│   └── uac_analysis.ipynb
│
├── dashboard
│   └── app.py
│
└── report
    └── UAC_System_Capacity_Report.docx
21. Limitations

Several limitations should be considered when interpreting the analysis.

21.1 Historical Data

The analysis is based on historical observations and therefore describes patterns in the available dataset.

21.2 Observation Gaps

The dataset does not contain an observation for every calendar day. The average gap between observations was approximately 1.49 days, with a maximum gap of 10 days.

Therefore, rolling calculations were defined based on observations rather than exact calendar-day periods.

21.3 Statistical High-Load Threshold

The High Load classification is based on the 75th percentile of Total System Load.

It is an analytical classification and does not represent an official operational capacity threshold.

21.4 Aggregate-Level Analysis

The analysis focuses on aggregate system-level measures available in the dataset.

It does not provide facility-level capacity, staffing-level capacity, geographic-level capacity, or individual case-level analysis.

21.5 Interpretation of Net Intake Pressure

Net Intake Pressure is an analytical indicator based on transfers and discharges.

It should not be interpreted as a complete measure of actual physical capacity or available beds.

22. Future Enhancements

The project can be expanded in several ways.

22.1 Forecasting

Time-series forecasting models could be added to estimate future system load and intake pressure.

22.2 Automated Alerts

The dashboard could include automated alerts when system load or intake pressure exceeds predefined analytical thresholds.

22.3 Facility-Level Analysis

If facility-level data becomes available, the analysis could be extended to compare capacity and workload across individual facilities.

22.4 Geographic Analysis

Geographic information could be incorporated to examine regional differences in care demand and system capacity.

22.5 Real-Time Data Integration

The dashboard could be connected to regularly updated data sources to provide more current monitoring.

22.6 Advanced Predictive Analytics

Machine learning and statistical forecasting techniques could be explored to identify factors associated with changes in system load.

23. Conclusion

The UAC System Capacity & Care Load Analytics project provides a structured analytical approach for examining system load and movement patterns within the UAC care pipeline.

The project combines data preparation, exploratory analysis, feature engineering, statistical indicators, rolling averages, high-load classification, and interactive visualization.

The analysis demonstrates how historical system-level data can be transformed into meaningful indicators such as Total System Load, Net Intake Pressure, Care Load Growth Rate, Discharge Offset Ratio, cumulative intake, and rolling averages.

The results provide a quantitative view of changes in CBP custody, HHS care, transfers, and discharges over time.

The Streamlit dashboard further improves accessibility by allowing users to interactively examine different metrics and time periods.

Overall, the project establishes a reusable analytical framework that can be extended with forecasting, automated alerts, more detailed capacity information, and additional data sources.

24. Main Deliverables

The project produces the following deliverables:

Analytical Notebook
analysis/uac_analysis.ipynb

Contains the data preparation, exploratory analysis, feature engineering, and analytical calculations.

Original Dataset
data/uac_data.csv

Contains the original UAC data used for the analysis.

Final Analytical Dataset
data/uac_final_analysis.csv

Contains the original data together with derived analytical metrics and indicators.

Monthly Summary Dataset
data/uac_monthly_summary.csv

Contains monthly-level aggregated information.

Interactive Dashboard
dashboard/app.py

Contains the Streamlit dashboard application.

Project Report
report/UAC_System_Capacity_Report.docx

Contains the formal documentation of the project, methodology, analysis, findings, dashboard, limitations, and future enhancements.

25. Summary

The project demonstrates an end-to-end data analytics workflow:

Data Collection
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Statistical Analysis
      ↓
Trend Analysis
      ↓
High-Load Identification
      ↓
Dashboard Development
      ↓
Analytical Insights

The resulting analytical framework provides a foundation for monitoring UAC system load, understanding transfer and discharge patterns, identifying relatively high-load periods, and supporting further capacity-oriented analysis.