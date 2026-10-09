import streamlit as st
import pandas as pd

st.title("WBS Upload")

uploaded_file = st.file_uploader(
    "Upload WBS Excel File",
    type=["xlsx"]
)

if uploaded_file:

    wbs_df = pd.read_excel(uploaded_file)

    st.session_state["wbs_df"] = wbs_df

    st.success("WBS Uploaded Successfully")

    st.dataframe(
        wbs_df,
        use_container_width=True
    )
