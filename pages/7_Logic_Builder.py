import streamlit as st
import pandas as pd

st.title("🔗 Logic Builder")

if "schedule_df" not in st.session_state:

    st.warning(
        "Generate Schedule First"
    )

    st.stop()

df = st.session_state["schedule_df"]

activity_list = df["Activity ID"].tolist()

editable_df = st.data_editor(
    df,
    use_container_width=True,
    height=700
)

st.session_state["schedule_df"] = editable_df

st.success(
    "Activity Logic Updated"
)
