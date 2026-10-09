import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📚 Fragnet Master")

st.markdown("""
Upload the Fragnet Master Excel file.

Required Columns:

- WBS Scope
- Fragnet ID
- Activity Description
- S-Curve Scope
- Duration (Days)
""")

uploaded = st.file_uploader(
    "Upload Fragnet Master",
    type=["xlsx"]
)

if uploaded:

    fragnet_df = pd.read_excel(uploaded)

    st.session_state["fragnet_master"] = fragnet_df

    st.success(
        f"{len(fragnet_df)} Fragnets Loaded Successfully"
    )

    st.dataframe(
        fragnet_df,
        use_container_width=True,
        height=500
    )

else:

    st.info(
        "Upload your Fragnet Master Excel file."
    )

    if "fragnet_master" in st.session_state:

        st.subheader("Current Fragnet Master")

        st.dataframe(
            st.session_state["fragnet_master"],
            use_container_width=True
        )
