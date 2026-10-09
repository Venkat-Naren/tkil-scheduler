import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(layout="wide")

st.title("📅 Date Calculator")

if "schedule_df" not in st.session_state:

    st.warning(
        "Please generate schedule first."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

project_start = st.date_input(
    "Project Start Date"
)

activity_dates = {}

for idx, row in df.iterrows():

    preds = []

    for pred_col in ["Pred1", "Pred2", "Pred3"\]:

        pred = str(
            row.get(pred_col, "")
        ).strip()

        if pred != "":
            preds.append(pred)

    duration = int(row["Duration"])

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
                + timedelta(days=1)
            )

        else:

            start_date = pd.Timestamp(
                project_start
            )

    finish_date = (
        start_date
        + timedelta(days=duration-1)
    )

    activity_dates[
        row["Activity ID"]
    ] = {
        "Start": start_date,
        "Finish": finish_date
    }

    df.loc[idx, "Start Date"] = start_date
    df.loc[idx, "Finish Date"] = finish_date

st.session_state["schedule_df"] = df

st.success(
    "Schedule Calculated Successfully"
)

st.dataframe(
    df,
    use_container_width=True,
    height=700
)
