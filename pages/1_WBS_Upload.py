import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="WBS Upload",
    layout="wide"
)

st.title("📂 WBS Upload")

st.markdown("""
Upload the WBS Excel file containing:

- TKIL SAP WBS Code
- WBS Name
- WBS Scope
""")

# Sample Template

sample_df = pd.DataFrame({
    "TKIL SAP WBS Code": [
        "1000-01",
        "1000-02",
        "1000-03"
    ],
    "WBS Name": [
        "Bag Filter",
        "ESP",
        "Screw Conveyor"
    ],
    "WBS Scope": [
        "BM",
        "BE",
        "SC"
    ]
})

buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    sample_df.to_excel(
        writer,
        sheet_name="WBS Upload",
        index=False
    )

st.download_button(
    label="📥 Download Sample WBS Template",
    data=buffer.getvalue(),
    file_name="Sample_WBS_Template.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload WBS Excel File",
    type=["xlsx"]
)

if uploaded_file:

    try:

        wbs_df = pd.read_excel(
            uploaded_file
        )

        required_columns = [
            "TKIL SAP WBS Code",
            "WBS Name",
            "WBS Scope"
        ]

        missing = [
            col
            for col in required_columns
            if col not in wbs_df.columns
        ]

        if missing:

            st.error(
                f"Missing columns: {', '.join(missing)}"
            )

        else:

            st.session_state["wbs_df"] = wbs_df

            st.success(
                f"{len(wbs_df)} WBS records uploaded successfully."
            )

            st.dataframe(
                wbs_df,
                use_container_width=True,
                height=400
            )

    except Exception 
