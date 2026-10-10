import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Project Data",
    layout="wide"
)

st.title("📂 Project Data Setup")

col1, col2 = st.columns(2)

# =====================================================
# FRAGNET MASTER
# =====================================================

with col1:

    st.header("📚 Fragnet Master")

    sample_fragnet = pd.DataFrame({
        "WBS Scope":["BM"],
        "Fragnet ID":["BM-001"],
        "Activity Description":
            ["Release of Tech. Specifications/PR"],
        "S-Curve Scope":["ENGG DM"],
        "Duration (Days)":[5]
    })

    fragnet_buffer = BytesIO()

    with pd.ExcelWriter(
        fragnet_buffer,
        engine="openpyxl"
    ) as writer:

        sample_fragnet.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "Download Sample Fragnet Template",
        fragnet_buffer.getvalue(),
        "Sample_Fragnet.xlsx"
    )

    fragnet_file = st.file_uploader(
        "Upload Fragnet Master",
        type=["xlsx"],
        key="fragnet"
    )

    if fragnet_file:

        fragnet_df = pd.read_excel(
            fragnet_file
        )

        st.session_state[
            "fragnet_master"
        ] = fragnet_df

        st.success(
            f"{len(fragnet_df)} Fragnets Loaded"
        )

# =====================================================
# WBS UPLOAD
# =====================================================

with col2:

    st.header("📂 WBS Upload")

    sample_wbs = pd.DataFrame({

        "TKIL SAP WBS Code":[
            "1000-01"
        ],

        "WBS Name":[
            "Bag Filter"
        ],

        "WBS Scope":[
            "BM"
        ]
    })

    wbs_buffer = BytesIO()

    with pd.ExcelWriter(
        wbs_buffer,
        engine="openpyxl"
    ) as writer:

        sample_wbs.to_excel(
            writer,
            index=False
        )

    st.download_button(
        "Download Sample WBS Template",
        wbs_buffer.getvalue(),
        "Sample_WBS.xlsx"
    )

    uploaded_wbs = st.file_uploader(
        "Upload WBS",
        type=["xlsx"],
        key="wbs"
    )

    if uploaded_wbs:

        wbs_df = pd.read_excel(
            uploaded_wbs
        )

        st.session_state[
            "wbs_df"
        ] = wbs_df

        st.success(
            f"{len(wbs_df)} WBS Loaded"
        )

# =====================================================
# SUMMARY
# =====================================================

st.divider()

st.subheader("Project Summary")

if (
    "wbs_df" in st.session_state
    and
    "fragnet_master"
    in st.session_state
):

    wbs_df = st.session_state["wbs_df"]

    fragnet_df = st.session_state[
        "fragnet_master"
    ]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "WBS Count",
        len(wbs_df)
    )

    c2.metric(
        "Scopes",
        wbs_df["WBS Scope"]
        .nunique()
    )

    c3.metric(
        "Fragnets",
        len(fragnet_df)
    )

    st.success(
        "✅ Project Data Ready"
    )

else:

    st.warning(
        "Upload both Fragnet Master and WBS Upload."
    )
