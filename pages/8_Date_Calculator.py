import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(
    page_title="Date Calculator",
    layout="wide"
)

st.title("📅 Date Calculator")

if "schedule_df" not in st.session_state:

    st.warning(
        "Please generate the schedule first."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

project_start = st.date_input(
    "Project Start Date"
)

activity_dates = {}

# Ensure columns exist

if "Start Date" not in df.columns:
    df["Start Date"] = pd.NaT

if "Finish Date" not in df.columns:
    df["Finish Date"] = pd.NaT

if "Lag" not in df.columns:
    df["Lag"] = 0

# Calculate Dates

for idx, row in df.iterrows():

    preds = []

    for pred_col in ["Pred1", "Pred2", "Pred3"\]:

        pred = str(
            row.get(pred_col, "")
        ).strip()

        if pred and pred.lower() != "nan":
            preds.append(pred)

    duration = int(row["Duration"])

    lag = int(
        row.get("Lag", 0)
    )

    # No predecessors

    if len(preds) == 0:

        start_date = pd.Timestamp(
            project_start
        )

    else:

        pred_finish_dates = []

        for pred in preds:

            if pred in activity_dates:

                pred_finish_dates.append(
                    activity_dates[pred]["Finish"]
                )

        if len(pred_finish_dates) > 0:

            start_date = (
                max(pred_finish_dates)
                + timedelta(days=1 + lag)
            )

        else:

            start_date = pd.Timestamp(
                project_start
            )

    finish_date = (
        start_date
        + timedelta(days=duration - 1)
    )

    activity_dates[
        row["Activity ID"]
    ] = {
        "Start": start_date,
        "Finish": finish_date
    }

    df.loc[idx, "Start Date"] = start_date
    df.loc[idx, "Finish Date"] = finish_date

# Save back to session

st.session_state["schedule_df"] = df

# KPIs

st.subheader("Schedule Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Activities",
        len(df)
    )

with col2:
    st.metric(
        "Project Start",
        df["Start Date"].min().strftime("%d-%b-%Y")
    )

with col3:
    st.metric(
        "Project Finish",
        df["Finish Date"].max().strftime("%d-%b-%Y")
    )

st.divider()

st.success(
    "Schedule Calculated Successfully"
)

st.dataframe(
    df,
    use_container_width=True,
    height=700
)

# Download updated schedule

csv = df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Updated Schedule",
    data=csv,
    file_name="Calculated_Schedule.csv",
    mime="text/csv"
)
