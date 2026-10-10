import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Project Dashboard",
    layout="wide"
)

st.title("📊 Project Dashboard")

if "schedule_df" not in st.session_state:

    st.warning(
        "Generate Schedule First."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

# =====================================================
# BASIC METRICS
# =====================================================

total_activities = len(df)

total_wbs = df[
    "TKIL SAP WBS Code"
].nunique()

total_scopes = df[
    "WBS Scope"
].nunique()

# =====================================================
# PROJECT DURATION
# =====================================================

project_start = None
project_finish = None
project_duration = 0

if (
    "Start Date" in df.columns
    and
    "Finish Date" in df.columns
):

    valid_dates = df.dropna(
        subset=[
            "Start Date",
            "Finish Date"
        ]
    )

    if len(valid_dates) > 0:

        valid_dates["Start Date"] = pd.to_datetime(
            valid_dates["Start Date"]
        )

        valid_dates["Finish Date"] = pd.to_datetime(
            valid_dates["Finish Date"]
        )

        project_start = valid_dates[
            "Start Date"
        ].min()

        project_finish = valid_dates[
            "Finish Date"
        ].max()

        project_duration = (
            project_finish - project_start
        ).days + 1

# =====================================================
# KPI ROW 1
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Activities",
        total_activities
    )

with c2:

    st.metric(
        "Project Duration (Days)",
        project_duration
    )

with c3:

    if project_start is not None:

        st.metric(
            "Project Start",
            project_start.strftime(
                "%d-%b-%Y"
            )
        )

    else:

        st.metric(
            "Project Start",
            "-"
        )

with c4:

    if project_finish is not None:

        st.metric(
            "Project Finish",
            project_finish.strftime(
                "%d-%b-%Y"
            )
        )

    else:

        st.metric(
            "Project Finish",
            "-"
        )

# =====================================================
# KPI ROW 2
# =====================================================

c5, c6, c7, c8 = st.columns(4)

with c5:

    st.metric(
        "WBS Packages",
        total_wbs
    )

with c6:

    st.metric(
        "Scopes",
        total_scopes
    )

with c7:

    if "% Complete" in df.columns:

        avg_progress = round(
            df["% Complete"].mean(),
            1
        )

        st.metric(
            "Average Progress %",
            avg_progress
        )

    else:

        st.metric(
            "Average Progress %",
            0
        )

with c8:

    completed = 0

    if "% Complete" in df.columns:

        completed = len(
            df[
                df["% Complete"] >= 100
            ]
        )

    st.metric(
        "Completed Activities",
        completed
    )

st.divider()

# =====================================================
# SCOPE SUMMARY
# =====================================================

scope_summary = (

    df.groupby("WBS Scope")
    .agg(

        Activities=(
            "Activity ID",
            "count"
        ),

        Duration=(
            "Duration",
            "sum"
        )

    )
    .reset_index()

)

col1, col2 = st.columns(2)

with col1:

    fig1 = px.bar(

        scope_summary,

        x="WBS Scope",

        y="Activities",

        color="WBS Scope",

        title="Activities by Scope"

    )

    st.plotly_chart(
        fig1,
        width="stretch"
    )

with col2:

    fig2 = px.pie(

        scope_summary,

        names="WBS Scope",

        values="Duration",

        title="Duration Distribution by Scope"

    )

    st.plotly_chart(
        fig2,
        width="stretch"
    )

# =====================================================
# SCHEDULE REVIEW
# =====================================================

st.divider()

st.subheader("📋 Schedule Review")

st.dataframe(
    df,
    width="stretch",
    height=500
)
