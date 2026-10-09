import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📈 Project Dashboard")

if "schedule_df" not in st.session_state:
    st.warning("Generate the schedule first.")
    st.stop()

df = st.session_state["schedule_df"]

# KPI Section

total_activities = len(df)
total_duration = df["Duration"].sum()

total_wbs = df["TKIL SAP WBS Code"].nunique()

total_scopes = df["WBS Scope"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Activities",
    total_activities
)

c2.metric(
    "Duration (Days)",
    int(total_duration)
)

c3.metric(
    "WBS Count",
    total_wbs
)

c4.metric(
    "Scopes",
    total_scopes
)

st.divider()

# Scope Distribution

scope_summary = (
    df.groupby("WBS Scope")
    .agg(
        Activities=("Activity ID", "count"),
        Duration=("Duration", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig1 = px.bar(
        scope_summary,
        x="WBS Scope",
        y="Activities",
        title="Activities by Scope",
        color="WBS Scope"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fig2 = px.pie(
        scope_summary,
        names="WBS Scope",
        values="Duration",
        title="Duration Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

st.subheader("Generated Schedule")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)
