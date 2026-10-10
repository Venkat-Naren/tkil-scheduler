import streamlit as st
import pandas as pd

st.title("🔥 Critical Path")

if "schedule_df" not in st.session_state:

    st.stop()

df = st.session_state["schedule_df"]

if "Finish Date" not in df.columns:

    st.warning(
        "Run Schedule Calculation First"
    )

    st.stop()

project_finish = pd.to_datetime(
    df["Finish Date"]
).max()

df["Float"] = (

    project_finish

    -

    pd.to_datetime(
        df["Finish Date"]
    )

).dt.days

df["Critical"] = (
    df["Float"] == 0
)

critical_df = df[
    df["Critical"]
]

st.metric(
    "Critical Activities",
    len(critical_df)
)

st.dataframe(
    critical_df[
        [
            "Activity ID",
            "Activity Description",
            "Start Date",
            "Finish Date",
            "Float"
        ]
    ],
    width="stretch"
)
