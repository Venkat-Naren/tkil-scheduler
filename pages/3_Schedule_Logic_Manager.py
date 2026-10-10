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
        "Please generate schedule first."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

# ====================================================
# USER LOGIC ACTIVITIES
# ====================================================

editable_df = df[
    df["Logic Type"] == "USER"
].copy()

st.subheader("User Logic Activities")

st.info(
    "Assign predecessors only for the starting activity of each WBS chain."
)

activity_ids = sorted(
    df["Activity ID"].astype(str).tolist()
)

updated_rows = []

for idx, row in editable_df.iterrows():

    st.markdown("---")

    st.write(
        f"### {row['Activity ID']} | {row['Activity Description']}"
    )

    current_pred = (
        str(row["Pred1"])
        if pd.notna(row["Pred1"])
        else ""
    )

    available_preds = [""] + [
        a for a in activity_ids
        if a != row["Activity ID"]
    ]

    pred1 = st.selectbox(
        f"Predecessor - {row['Activity ID']}",
        available_preds,
        index=(
            available_preds.index(current_pred)
            if current_pred in available_preds
            else 0
        ),
        key=f"pred_{row['Activity ID']}"
    )

    relationship = st.selectbox(
        f"Relationship - {row['Activity ID']}",
        ["FS", "SS", "FF", "SF"],
        key=f"rel_{row['Activity ID']}"
    )

    lag = st.number_input(
        f"Lag Days - {row['Activity ID']}",
        value=int(row.get("Lag", 0)),
        key=f"lag_{row['Activity ID']}"
    )

    updated_rows.append(
        (
            row["Activity ID"],
            pred1,
            relationship,
            lag
        )
    )

# ====================================================
# SAVE LOGIC
# ====================================================

if st.button("💾 Save Logic"):

    for activity_id, pred1, relationship, lag in updated_rows:

        idx = df[
            df["Activity ID"] == activity_id
        ].index[0]

        df.loc[idx, "Pred1"] = pred1
        df.loc[idx, "Relationship"] = relationship
        df.loc[idx, "Lag"] = lag

    st.session_state["schedule_df"] = df

    st.success(
        "Logic Saved Successfully"
    )

# ====================================================
# CALCULATE DATES
# ====================================================

st.divider()

st.subheader("📅 Calculate Schedule")

project_start = st.date_input(
    "Project Start Date"
)

if st.button("Calculate Schedule"):

    activity_dates = {}

    schedule_df = st.session_state[
        "schedule_df"
    ].copy()

    if "Start Date" not in schedule_df.columns:
        schedule_df["Start Date"] = None

    if "Finish Date" not in schedule_df.columns:
        schedule_df["Finish Date"] = None

    for idx, row in schedule_df.iterrows():

        pred1 = str(
            row.get("Pred1", "")
        ).strip()

        lag = int(
            row.get("Lag", 0)
        )

        duration = int(
            row["Duration"]
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
                    + timedelta(days=1 + lag)
                )

            else:

                start_date = pd.Timestamp(
                    project_start
                )

        finish_date = (
            start_date
            + timedelta(days=duration - 1)
        )

        activity_dates[
            row["Activity ID"]
        ] = {

            "Start":
                start_date,

            "Finish":
                finish_date

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

# ====================================================
# VALIDATION
# ====================================================

st.divider()

st.subheader("✅ Logic Validation")

issues = []

for _, row in df.iterrows():

    activity_id = str(
        row["Activity ID"]
    )

    pred1 = str(
        row.get("Pred1", "")
    ).strip()

    if pred1 == "":
        continue

    if pred1 == activity_id:

        issues.append(
            f"{activity_id} cannot be its own predecessor."
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
        "No logic issues found."
    )

# ====================================================
# SCHEDULE REVIEW
# ====================================================

st.divider()

st.subheader("📋 Current Schedule")

# ====================================================
# EXPORT SCHEDULE
# ====================================================

st.divider()

st.subheader("📥 Export Schedule")

schedule_export = st.session_state["schedule_df"]

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    schedule_export.to_excel(
        writer,
        sheet_name="Schedule",
        index=False
    )

st.download_button(
    label="📥 Download Schedule Excel",
    data=excel_buffer.getvalue(),
    file_name="TKIL_Schedule.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

csv_data = schedule_export.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Schedule CSV",
    data=csv_data,
    file_name="TKIL_Schedule.csv",
    mime="text/csv"
)

st.dataframe(
    st.session_state["schedule_df"],
    width="stretch",
    height=600
)
