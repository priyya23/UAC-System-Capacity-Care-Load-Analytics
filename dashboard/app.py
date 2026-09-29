import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UAC Care Load Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/uac_final_analysis.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_data()


# ============================================================
# TITLE AND INTRODUCTION
# ============================================================

st.title("📊 UAC System Capacity & Care Load Analytics")

st.markdown(
    """
    This dashboard provides an overview of system load, CBP custody,
    HHS care, transfers, discharges, and net intake pressure across
    the UAC care pipeline.
    """
)

st.markdown("---")


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.header("Dashboard Controls")


# Date range

minimum_date = df["Date"].min().date()
maximum_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)


# Metric selection

selected_metric = st.sidebar.selectbox(
    "Metric",
    [
        "Total System Load",
        "Children in CBP custody",
        "Children in HHS Care",
        "Net Intake Pressure",
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ]
)


# ============================================================
# FILTER DATA
# ============================================================

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = df[
        (df["Date"] >= start_date)
        & (df["Date"] <= end_date)
    ].copy()

else:

    filtered_df = df.copy()


if filtered_df.empty:

    st.warning(
        "No data is available for the selected date range."
    )

    st.stop()


# ============================================================
# LATEST OBSERVATION
# ============================================================

latest = (
    filtered_df
    .sort_values("Date")
    .iloc[-1]
)

latest_date = latest["Date"].strftime(
    "%B %d, %Y"
)

total_system_load = latest["Total System Load"]

cbp_load = latest["Children in CBP custody"]

hhs_load = latest["Children in HHS Care"]

net_intake = latest["Net Intake Pressure"]


# ============================================================
# SUMMARY CALCULATIONS
# ============================================================

average_system_load = (
    filtered_df["Total System Load"].mean()
)

maximum_system_load = (
    filtered_df["Total System Load"].max()
)

minimum_system_load = (
    filtered_df["Total System Load"].min()
)

load_volatility = (
    filtered_df["Total System Load"].std()
)

total_transfers = (
    filtered_df[
        "Children transferred out of CBP custody"
    ].sum()
)

total_discharges = (
    filtered_df[
        "Children discharged from HHS Care"
    ].sum()
)

positive_intake_days = (
    filtered_df["Net Intake Pressure"] > 0
).sum()

number_of_observations = len(filtered_df)

backlog_rate = (
    positive_intake_days /
    number_of_observations *
    100
    if number_of_observations > 0
    else 0
)


# ============================================================
# SUMMARY STATISTICS
# ============================================================

st.header("📌 Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Average System Load",
        f"{average_system_load:,.0f}"
    )

with col2:

    st.metric(
        "Maximum System Load",
        f"{maximum_system_load:,.0f}"
    )

with col3:

    st.metric(
        "Minimum System Load",
        f"{minimum_system_load:,.0f}"
    )


# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

st.header("Key Performance Indicators")

st.caption(
    f"Latest observation in selected period: {latest_date}"
)


# First KPI row

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total System Load",
        f"{total_system_load:,.0f}"
    )


with col2:

    st.metric(
        "CBP Custody",
        f"{cbp_load:,.0f}"
    )


with col3:

    st.metric(
        "HHS Care",
        f"{hhs_load:,.0f}"
    )


with col4:

    st.metric(
        "Net Intake Pressure",
        f"{net_intake:,.0f}"
    )


# Second KPI row

col5, col6, col7, col8 = st.columns(4)


with col5:

    st.metric(
        "Average System Load",
        f"{average_system_load:,.0f}"
    )


with col6:

    st.metric(
        "Load Volatility",
        f"{load_volatility:,.0f}"
    )


with col7:

    st.metric(
        "Total Transfers",
        f"{total_transfers:,.0f}"
    )


with col8:

    st.metric(
        "Total Discharges",
        f"{total_discharges:,.0f}"
    )


# ============================================================
# HIGH-LOAD ALERT
# ============================================================

st.markdown("---")

st.header("⚠️ High-Load Alert")

high_load_count = filtered_df["High_Load_Flag"].sum()

if high_load_count > 0:

    st.warning(
        f"High-load conditions were observed on "
        f"{high_load_count} observation(s) in the selected period."
    )

else:

    st.success(
        "No high-load observations in the selected period."
    )


# ============================================================
# SYSTEM LOAD OVERVIEW
# ============================================================

st.header("1. System Load Overview")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df["Date"],
    filtered_df["Total System Load"],
    label="Total System Load"
)

ax.plot(
    filtered_df["Date"],
    filtered_df["7_Observation_Load_Avg"],
    label="7-Observation Average"
)

ax.plot(
    filtered_df["Date"],
    filtered_df["14_Observation_Load_Avg"],
    label="14-Observation Average"
)

ax.set_title(
    "Total System Load Over Time"
)

ax.set_xlabel("Date")

ax.set_ylabel("Children")

ax.legend()

ax.grid(
    True,
    alpha=0.3
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# CBP VS HHS LOAD
# ============================================================

st.header("2. CBP vs HHS Care Load")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df["Date"],
    filtered_df["Children in CBP custody"],
    label="CBP Custody"
)

ax.plot(
    filtered_df["Date"],
    filtered_df["Children in HHS Care"],
    label="HHS Care"
)

ax.set_title(
    "Children in CBP Custody and HHS Care"
)

ax.set_xlabel("Date")

ax.set_ylabel("Children")

ax.legend()

ax.grid(
    True,
    alpha=0.3
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# NET INTAKE AND BACKLOG
# ============================================================

st.header("3. Net Intake and Backlog Trends")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df["Date"],
    filtered_df["Net Intake Pressure"],
    label="Net Intake Pressure"
)

ax.plot(
    filtered_df["Date"],
    filtered_df["7_Observation_Intake_Avg"],
    label="7-Observation Average"
)

ax.axhline(
    0,
    linestyle="--",
    label="Zero Balance"
)

ax.set_title(
    "Net Intake Pressure Over Time"
)

ax.set_xlabel("Date")

ax.set_ylabel("Children")

ax.legend()

ax.grid(
    True,
    alpha=0.3
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# CUMULATIVE NET INTAKE
# ============================================================

st.header("4. Cumulative Net Intake")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df["Date"],
    filtered_df["Cumulative Net Intake"]
)

ax.set_title(
    "Cumulative Net Intake Over Time"
)

ax.set_xlabel("Date")

ax.set_ylabel(
    "Cumulative Net Intake"
)

ax.grid(
    True,
    alpha=0.3
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# TRANSFERS VS DISCHARGES
# ============================================================

st.header("5. Transfers vs Discharges")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df["Date"],
    filtered_df[
        "Children transferred out of CBP custody"
    ],
    label="Transfers"
)

ax.plot(
    filtered_df["Date"],
    filtered_df[
        "Children discharged from HHS Care"
    ],
    label="Discharges"
)

ax.set_title(
    "Transfers into HHS and HHS Discharges"
)

ax.set_xlabel("Date")

ax.set_ylabel("Children")

ax.legend()

ax.grid(
    True,
    alpha=0.3
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# SELECTED METRIC
# ============================================================

st.header("6. Selected Metric")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    filtered_df["Date"],
    filtered_df[selected_metric]
)

ax.set_title(
    f"{selected_metric} Over Time"
)

ax.set_xlabel("Date")

ax.set_ylabel("Children")

ax.grid(
    True,
    alpha=0.3
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ============================================================
# ANALYTICAL SUMMARY
# ============================================================

st.header("7. Analytical Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.metric(
        "Load Volatility",
        f"{load_volatility:,.0f}"
    )


with summary_col2:

    st.metric(
        "Positive Intake Observations",
        f"{positive_intake_days:,}"
    )


with summary_col3:

    st.metric(
        "Positive Intake Share",
        f"{backlog_rate:.1f}%"
    )


# ============================================================
# HIGH LOAD PERIODS
# ============================================================

st.header("8. High Load Periods")

high_load = (
    filtered_df[
        filtered_df["High_Load_Flag"] == True
    ][
        [
            "Date",
            "Total System Load",
            "Children in CBP custody",
            "Children in HHS Care",
            "Net Intake Pressure"
        ]
    ]
    .sort_values(
        "Total System Load",
        ascending=False
    )
)

if high_load.empty:

    st.info(
        "No high-load observations are present "
        "for the selected period."
    )

else:

    st.dataframe(
        high_load,
        use_container_width=True
    )


# ============================================================
# MONTHLY SUMMARY
# ============================================================

st.header("9. Monthly Summary")

monthly_summary = (
    filtered_df
    .groupby("Month")
    .agg(
        Average_System_Load=(
            "Total System Load",
            "mean"
        ),

        Maximum_System_Load=(
            "Total System Load",
            "max"
        ),

        Average_Net_Intake=(
            "Net Intake Pressure",
            "mean"
        ),

        Total_Transfers=(
            "Children transferred out of CBP custody",
            "sum"
        ),

        Total_Discharges=(
            "Children discharged from HHS Care",
            "sum"
        )
    )
    .reset_index()
)

st.dataframe(
    monthly_summary,
    use_container_width=True
)


# ============================================================
# DATASET EXPLORER
# ============================================================

st.header("10. Dataset Explorer")

with st.expander(
    "View Filtered Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.header("11. Download Analysis Data")

csv_data = (
    filtered_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv_data,
    file_name="uac_filtered_analysis.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "UAC System Capacity & Care Load Analytics | "
    "Data Analysis Dashboard"
)