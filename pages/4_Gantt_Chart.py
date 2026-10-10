import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Gantt Chart")

if "schedule_df" not in st.session_state:

    st.stop()

df = st.session_state["schedule_df"]

required = [
    "Start Date",
    "Finish Date"
]

if not all(
    c in df.columns
    for c in required
):

    st.warning(
        "Run Schedule Logic Manager first."
    )

    st.stop()

df = df.dropna(
    subset=[
        "Start Date",
        "Finish Date"
    ]
)

fig = px.timeline(

    df,

    x_start="Start Date",

    x_end="Finish Date",

    y="Activity Description",

    color="WBS Scope",

    hover_data=[
        "Activity ID",
        "Fragnet ID",
        "Duration"
    ]

)

fig.update_yaxes(
    autorange="reversed"
)

fig.update_layout(
    height=900
)

st.plotly_chart(
    fig,
    width="stretch"
)
