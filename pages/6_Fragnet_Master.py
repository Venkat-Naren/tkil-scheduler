import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Fragnet Master",
    layout="wide"
)

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

# ------------------------------------------------------------------
# Sample Template
# ------------------------------------------------------------------

sample_fragnet = pd.DataFrame({
    "WBS Scope": [
        "BM",
        "BM",
        "BM",
        "SC",
        "SC",
        "MA"
    ],
    "Fragnet ID": [
        "BM-001",
        "BM-002",
        "BM-003",
        "SC-001",
        "SC-002",
        "MA-001"
    ],
    "Activity Description": [
        "Release of Tech. Specifications/PR",
        "Issue of Inquiry & Receipt of Offer, bid evaluation",
        "Technical Evaluation",
        "Release of mfg drgs/JRM",
        "Issue of Inquiry & Receipt of Offer, bid evaluation",
        "Release of Tech. Specifications/PR"
    ],
    "S-Curve Scope": [
        "ENGG DM",
        "BM",
        "ENGG DM",
        "ENGG DM",
        "SC",
        "ENGG DM"
    ],
    "Duration (Days)": [
        5,
        7,
        10,
        5,
        7,
        5
    ]
})

buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    sample_fragnet.to_excel(
        writer,
        sheet_name="Fragnet Master",
        index=False
    )

st.download_button(
    label="📥 Download Sample Fragnet Template",
    data=buffer.getvalue(),
    file_name="Sample_Fragnet_Master.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ------------------------------------------------------------------
# Upload Section
# ------------------------------------------------------------------

uploaded = st.file_uploader(
    "Upload Fragnet Master",
    type=["xlsx"]
)

if uploaded:

    try:

        fragnet_df = pd.read_excel(uploaded)

        required_columns = [
            "WBS Scope",
            "Fragnet ID",
            "Activity Description",
            "S-Curve Scope",
            "Duration (Days)"
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in fragnet_df.columns
        ]

        if missing_columns:

            st.error(
                f"Missing Columns: {', '.join(missing_columns)}"
            )

        else:

            st.session_state["fragnet_master"] = fragnet_df

            st.success(
                f"{len(fragnet_df)} Fragnet Activities Loaded Successfully"
            )

            st.dataframe(
                fragnet_df,
                use_container_width=True,
                height=500
            )

    except Exception as e:

        st.error(
            f"Error reading file: {str(e)}"
        )

else:

    if "fragnet_master" in st.session_state:

        st.subheader("Current Fragnet Master")

        st.dataframe(
            st.session_state["fragnet_master"],
            use_container_width=True,
            height=500
        )
