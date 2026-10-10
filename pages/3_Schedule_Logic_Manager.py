import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import timedelta

st.set_page_config(
    page_title="Schedule Logic Manager",
    layout="wide"
)

st.title("🔗 Schedule Logic Manager")

if "schedule_df" not in st.session_state:

    st.warning("Generate Schedule First")

    st.stop()

df = st.session_state["schedule_df"].copy()

# ==================================================
# BULK LOGIC ASSIGNMENT
# ==================================================

st.subheader("Bulk Predecessor Assignment")

user_df = df[
    df["Logic Type"] == "USER"
]

activity_options = [

    f"{row['Activity ID']} | {row['Activity Description']}"

    for _, row in user_df.iterrows()

]

if len(activity_options) > 0:

    col1, col2 = st.columns(2)

    with col1:

        successor = st.selectbox(
            "Successor",
            activity_options
        )

        predecessor = st.selectbox(
            "Predecessor",
            [""] + activity_options
        )

    with col2:

        relationship = st.selectbox(
            "Relationship",
            ["FS", "SS", "FF", "SF"]
        )

        lag = st.number_input(
            "Lag",
            value=0
        )

    if st.button("Assign Logic"):

        successor_id = successor.split("|")[0].strip()

        predecessor_id = ""

        if predecessor != "":

            predecessor_id = (
                predecessor.split("|")[0]
                .strip()
            )

        idx = df[
            df["Activity ID"]
            == successor_id
        ].index[0]

        df.loc[idx, "Pred1"] = predecessor_id

        df.loc[idx, "Relationship"] = relationship

        df.loc[idx, "Lag"] = lag

        st.session_state["schedule_df"] = df

        st.success(
            "Logic Updated"
        )

# ==================================================
# VALIDATION
# ==================================================

st.divider()

st.subheader("Logic Validation")

issues = []

activity_ids = set(
    df["Activity ID"]
    .astype(str)
)

for _, row in df.iterrows():

    activity = str(
        row["Activity ID"]
    )

    for pred_col in [
        "Pred1",
        "Pred2",
        "Pred3"
    \]:

        pred = str(
            row.get(pred_col, "")
        ).strip()

        if pred == "" or pred == "nan":
            continue

        if pred == activity:

            issues.append(
                f"{activity} references itself"
            )

        if pred not in activity_ids:

            issues.append(
                f"{activity} has invalid predecessor {pred}"
            )

if issues:

    st.error(
        f"{len(issues)} issue(s) found"
    )

    for issue in issues:

        st.write(f"❌ {issue}")

else:

    st.success(
        "No Logic Issues Found"
    )

# ==================================================
# DATE CALCULATION
# ==================================================

st.divider()

st.subheader("📅 Calculate Schedule")

project_start = st.date_input(
    "Project Start Date"
)

if st.button("Calculate Schedule"):

    activity_dates = {}

    schedule_df = df.copy()

    for idx, row in schedule_df.iterrows():

        preds = []

        for pred_col in [
            "Pred1",
            "Pred2",
            "Pred3"
        \]:

            pred = str(
                row.get(pred_col, "")
            ).strip()

            if pred and pred != "nan":

                preds.append(pred)

        duration = int(
            row["Duration"]
        )

        lag_val = int(
            row.get("Lag", 0)
        )

        if len(preds) == 0:

            start_date = pd.Timestamp(
                project_start
            )

        else:

            dates = []

            for pred in preds:

                if pred in activity_dates:

                    dates.append(
                        activity_dates[pred]["Finish"]
                    )

            if len(dates) > 0:

                start_date = max(
                    dates
                ) + timedelta(
                    days=1 + lag_val
                )

            else:

                start_date = pd.Timestamp(
                    project_start
                )

        finish_date = (
            start_date +
            timedelta(
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
        "Schedule Calculated"
    )

# ==================================================
# REVIEW
# ==================================================

st.divider()

st.subheader("Schedule Review")

st.dataframe(
    st.session_state["schedule_df"],
    width="stretch",
    height=500
)

# ==========================
