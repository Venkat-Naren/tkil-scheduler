import streamlit as st
import pandas as pd
from datetime import timedelta
from io import BytesIO

st.set_page_config(
    page_title="Schedule Logic Manager",
    layout="wide"
)

st.title("🔗 Schedule Logic Manager")

if "schedule_df" not in st.session_state:

    st.warning(
        "Please Generate Schedule First."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

# =====================================================
# USER ACTIVITIES
# =====================================================

user_df = df[
    df["Logic Type"] == "USER"
].copy()

st.subheader("🔗 Bulk Predecessor Assignment")

if len(user_df) == 0:

    st.warning(
        "No USER Activities Found."
    )

else:

    activity_options = [

        f"{row['Activity ID']} | {row['Activity Description']}"

        for _, row in user_df.iterrows()

    ]

    col1, col2 = st.columns(2)

    with col1:

        successor = st.selectbox(
            "Successor Activity",
            activity_options
        )

        predecessor = st.selectbox(
            "Predecessor Activity",
            [""] + activity_options
        )

    with col2:

        relationship = st.selectbox(
            "Relationship",
            ["FS", "SS", "FF", "SF"]
        )

        lag = st.number_input(
            "Lag (Days)",
            value=0
        )

    if st.button("Assign Logic"):

        successor_id = successor.split("|")[0].strip()

        predecessor_id = ""

        if predecessor != "":

            predecessor_id = (
                predecessor.split("|")[0].strip()
            )

        row_idx = df[
            df["Activity ID"] == successor_id
        ].index[0]

        df.loc[row_idx, "Pred1"] = predecessor_id

        df.loc[row_idx, "Relationship"] = relationship

        df.loc[row_idx, "Lag"] = lag

        st.session_state["schedule_df"] = df

        st.success(
            f"Logic Assigned To {successor_id}"
        )

# =====================================================
# LOGIC SUMMARY
# =====================================================

st.divider()

st.subheader("📋 Logic Summary")

logic_view = df[
    df["Logic Type"] == "USER"
][[
    "Activity ID",
    "Activity Description",
    "Pred1",
    "Relationship",
    "Lag"
]]

st.dataframe(
    logic_view,
    width="stretch",
    height=300
)

# =====================================================
# DATE CALCULATION
# =====================================================

st.divider()

st.subheader("📅 Calculate Schedule")

project_start = st.date_input(
    "Project Start Date"
)

if st.button("Calculate Schedule"):

    schedule_df = st.session_state[
        "schedule_df"
    ].copy()

    activity_dates = {}

    if "Start Date" not in schedule_df.columns:
        schedule_df["Start Date"] = None

    if "Finish Date" not in schedule_df.columns:
        schedule_df["Finish Date"] = None

    for idx, row in schedule_df.iterrows():

        pred1 = str(
            row.get("Pred1", "")
        ).strip()

        duration = int(
            row["Duration"]
        )

        lag = int(
            row.get("Lag", 0)
        )

        # No predecessor

        if pred1 == "" or pred1 == "nan":

            start_date = pd.Timestamp(
                project_start
            )

        else:

            if pred1 in activity_dates:

                start_date = (

                    activity_dates[pred1]["Finish"]

                    +

                    timedelta(days=1 + lag)

                )

            else:

                start_date = pd.Timestamp(
                    project_start
                )

        finish_date = (

            start_date

            +

            timedelta(days=duration - 1)

        )

        activity_dates[
            row["Activity ID"]
        ] = {

            "Start": start_date,

            "Finish": finish_date

        }

        schedule_df.loc[
            idx,
            "Start Date"
        ] = start_date

        schedule_df.loc[
            idx,
            "Finish Date"
        ] = finish_date

    st.session_state[
        "schedule_df"
    ] = schedule_df

    st.success(
        "Schedule Calculated Successfully"
    )

# =====================================================
# VALIDATION
# =====================================================

st.divider()

st.subheader("✅ Logic Validation")

issues = []

for _, row in df.iterrows():

    activity = str(
        row["Activity ID"]
    ).strip()

    pred = str(
        row.get("Pred1", "")
    ).strip()

    if pred == "":
        continue

    if pred == activity:

        issues.append(

            f"{activity} cannot be its own predecessor"

        )

if issues:

    st.error(
        f"{len(issues)} Issues Found"
    )

    for issue in issues:

        st.write(
            f"❌ {issue}"
        )

else:

    st.success(
        "No Logic Issues Found"
    )

# =====================================================
# SCHEDULE REVIEW
# =====================================================

st.divider()

st.subheader("📊 Current Schedule")

schedule_export = st.session_state[
    "schedule_df"
]

st.dataframe(
    schedule_export,
    width="stretch",
    height=500
)

# =====================================================
# EXPORT
# =====================================================

st.divider()

st.subheader("📥 Export Schedule")

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    schedule_export.to_excel(
        writer,
        index=False,
        sheet_name="Schedule"
    )

st.download_button(
    "📥 Download Excel Schedule",
    excel_buffer.getvalue(),
    file_name="TKIL_Schedule.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

csv_data = schedule_export.to_csv(
    index=False
)

st.download_button(
    "📥 Download CSV Schedule",
    csv_data,
    file_name="TKIL_Schedule.csv",
    mime="text/csv"
)
