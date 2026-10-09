import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("📊 Gantt Chart")

if "schedule_df" not in st.session_state:
    st.warning("Please generate the schedule first.")
    st.stop()

schedule_df = st.session_state["schedule_df"].copy()

project_start = st.date_input(
    "Project Start Date",
    value=datetime.today()
)

# Simple sequential dates for now
current_date = pd.to_datetime(project_start)

start_dates = []
finish_dates = []

for _, row in schedule_df.iterrows():

    start_dates.append(current_date)

    finish = current_date + timedelta(
        days=int(row["Duration"])
    )

    finish_dates.append(finish)

    current_date = finish + timedelta(days=1)

schedule
