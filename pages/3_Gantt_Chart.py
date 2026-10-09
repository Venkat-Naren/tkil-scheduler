import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Gantt Chart",
    layout="wide"
)

st.title("📊 Project Gantt Chart")

# Check schedule exists
if "schedule_df" not in st.session_state:

    st.warning(
        "Please generate the schedule first."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

# Check dates are calculated
required_cols = ["Start Date", "Finish Date"]

missing_cols = [
    col for col in required_cols
    if col not in df.columns
]

if missing_cols:

    st.warning(
        "Please run Date Calculator first."
    )

    st.stop()

# Remove rows without dates
df = df.dropna(
    subset=["Start Date", "Finish Date"]
)

if len(df) == 0:

    st.warning(
        "No schedule dates available."
    )

    st.stop()

# Ensure datetime format
df["Start Date"] = pd.to_datetime(
    df["Start Date"]
)

df["Finish Date"] = pd.to_datetime(
    df["Finish Date"]
)

# KPI Section
col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Activities",
        len(df)
    )

with col2:

    project_start = df["Start Date"].min()

    st.metric(
        "Project Start",
        project_start.strftime("%d-%b-%Y")
    )

with col3:

    project_finish = df["Finish Date"].max()

    st.metric(
        "Project Finish",
        project_finish.strftime("%d-%b-%Y")
    )

st.divider()

# Optional Filters
scope_filter = st.multiselect(
    "Filter WBS Scope",
    options=sorted(df["WBS Scope"].unique()),
    default=sorted(df["WBS Scope"].unique())
)

filtered_df = df[
    df["WBS Scope"].isin(scope_filter)
]

# Gantt Chart
fig = px.timeline(
    filtered_df,
    x_start="Start Date",
    x_end="Finish Date",
    y="Activity Description",
    color="WBS Scope",
    text="Activity ID",
    hover_data=[
        "Activity ID",
        "Fragnet ID",
        "Duration",
        "TKIL SAP WBS Code",
        "WBS Name"
    ]
)

fig.update_yaxes(
    autorange="reversed"
)

fig.update_layout(
    title="Project Schedule",
    height=900,
    xaxis_title="Date",
    yaxis_title="Activities",
    legend_title="WBS Scope"
)

fig.update_traces(
    textposition="inside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Schedule Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

# Download option
csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Gantt Data",
    data=csv,
    file_name="gantt_schedule.csv",
    mime="text/csv"
)
