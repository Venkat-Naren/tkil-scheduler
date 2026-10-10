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
        "Generate Schedule First."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

# =====================================================
# USER ACTIVITIES
# =====================================================

user_df = df[
    df["Logic Type"] == "USER"
].copy()

st.subheader("Bulk Logic Assignment")

if len(user_df) > 0:

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

        pred1 = st.selectbox(
            "Pred1",
            [""] + activity_options
        )

        pred2 = st.selectbox(
            "Pred2",
            [""] + activity_options
        )

        pred3 = st.selectbox(
            "Pred3",
            [""] + activity_options
        )

    with col2:

        relationship = st.selectbox(
            "Relationship",
            ["FS", "SS", "FF", "SF"]
        )

        lag = st.number_input(
            "Lag Days",
            value=0
        )

    if st.button("Assign Logic"):

        successor_id = successor.split("|")[0].strip()

        idx = df[
            df["Activity ID"] == successor_id
        ].index[0]

        df.loc[idx, "Pred1"] = (
            pred1.split("|")[0].strip()
            if pred1 else ""
        )

        df.loc[idx, "Pred2"] = (
            pred2.split("|")[0].strip()
            if pred2 else ""
        )

        df.loc[idx, "Pred3"] = (
            pred3.split("|")[0].strip()
            if pred3 else ""
        )

        df.loc[idx, "Relationship"] = relationship

        df.loc[idx, "Lag"] = lag

        st.session_state["schedule_df"] = df

        st.success(
            f"Logic Updated For {successor_id}"
        )

# =====================================================
# LOGIC SUMMARY
# =====================================================

st.divider()

st.subheader("Logic Summary")

logic_cols = [

    "Activity ID",
    "Activity Description",
    "Pred1",
    "Pred2",
    "Pred3",
    "Relationship",
    "Lag"

]

available_cols = [
    c for c in logic_cols
    if c in df.columns
]

st.dataframe(
    df[available_cols],
    width="stretch",
    height=250,
    hide_index=True
)

# =====================================================
# VALIDATION
# =====================================================

st.divider()

st.subheader("Logic Validation")

issues = []

activity_ids = set(
    df["Activity ID"].astype(str)
)

for _, row in df.iterrows():

    activity_id = str(
        row["Activity ID"]
    )

    preds = [

        str(row.get("Pred1", "")).strip(),
        str(row.get("Pred2", "")).strip(),
        str(row.get("Pred3", "")).strip()

    ]

    for pred in preds:

        if pred == "" or pred == "nan":
            continue

        if pred == activity_id:

            issues.append(
                f"{activity_id} references itself"
            )

        if pred not in activity_ids:

            issues.append(
                f"{activity_id} has invalid predecessor {pred}"
            )

# Basic circular logic check

for _, row in df.iterrows():

    activity = str(row["Activity ID"])

    for pred_col in ["Pred1", "Pred2", "Pred3"]:

        pred = str(
            row.get(pred_col, "")
        ).strip()

        if pred == "" or pred == "nan":
            continue

        pred_rows = df[
            df["Activity ID"] == pred
        ]

        if len(pred_rows) > 0:

            p1 = str(
                pred_rows.iloc[0].get(
                    "Pred1",
                    ""
                )
            ).strip()

            if p1 == activity:

                issues.append(
                   f"Circular Logic: {activity} ↔ {pred}"
                )

if issues:

    st.error(
        f"{len(issues)} Issue(s) Found"
    )

    for issue in issues:

        st.write(
            f"❌ {issue}"
        )

else:

    st.success(
        "✅ No Logic Issues Found"
    )

# =====================================================
# DATE CALCULATOR
# =====================================================

st.divider()

st.subheader("📅 Schedule Calculation")

project_start = st.date_input(
    "Project Start Date"
)

if st.button("Calculate Schedule"):

    schedule_df = df.copy()

    activity_dates = {}

    if "Start Date" not in schedule_df.columns:
        schedule_df["Start Date"] = None

    if "Finish Date" not in schedule_df.columns:
        schedule_df["Finish Date"] = None

    for idx, row in schedule_df.iterrows():

        duration = int(
            row["Duration"]
        )

        lag = int(
            row.get("Lag", 0)
        )

        relationship = str(
            row.get(
                "Relationship",
                "FS"
            )
        )

        predecessor_dates = []

        for pred_col in [
            "Pred1",
            "Pred2",
            "Pred3"
        ]:

            pred = str(
                row.get(pred_col, "")
            ).strip()

            if (
                pred != ""
                and
                pred != "nan"
                and
                pred in activity_dates
            ):

                predecessor_dates.append(
                    activity_dates[pred]
                )

        if len(predecessor_dates) == 0:

            start_date = pd.Timestamp(
                project_start
            )

        else:

            if relationship == "FS":

                start_date = (
                    max(
                        x["Finish"]
                        for x in predecessor_dates
                    )
                    + timedelta(
                        days=1 + lag
                    )
                )

            elif relationship == "SS":

                start_date = (
                    max(
                        x["Start"]
                        for x in predecessor_dates
                    )
                    + timedelta(days=lag)
                )

            elif relationship == "FF":

                finish_date = (
                    max(
                        x["Finish"]
                        for x in predecessor_dates
                    )
                    + timedelta(days=lag)
                )

                start_date = (
                    finish_date
                    - timedelta(
                        days=duration - 1
                    )
                )

            elif relationship == "SF":

                finish_date = (
                    max(
                        x["Start"]
                        for x in predecessor_dates
                    )
                    + timedelta(days=lag)
                )

                start_date = (
                    finish_date
                    - timedelta(
                        days=duration - 1
                    )
                )

            else:

                start_date = pd.Timestamp(
                    project_start
                )

        finish_date = (
            start_date
            + timedelta(
                days=duration - 1
            )
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
        "✅ Schedule Calculated Successfully"
    )

# =====================================================
# REVIEW
# =====================================================

st.divider()

st.subheader("Current Schedule")

review_df = st.session_state["schedule_df"]

st.dataframe(
    review_df,
    width="stretch",
    height=500,
    hide_index=True
)

# =====================================================
# EXPORT
# =====================================================

st.divider()

st.subheader("📥 Export Schedule")

buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    review_df.to_excel(
        writer,
        index=False,
        sheet_name="Schedule"
    )

st.download_button(
    label="📥 Download Excel",
    data=buffer.getvalue(),
    file_name="TKIL_Schedule.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

csv_data = review_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name="TKIL_Schedule.csv",
    mime="text/csv"
)
