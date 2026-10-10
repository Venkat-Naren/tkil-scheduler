import streamlit as st
import pandas as pd
from datetime import timedelta
from io import BytesIO
from collections import defaultdict, deque

st.set_page_config(
    page_title="Schedule Logic Manager",
    layout="wide"
)

st.title("🔗 Schedule Logic Manager")

# =====================================================
# VALIDATIONS
# =====================================================

if "schedule_df" not in st.session_state:

    st.warning(
        "Please Generate Schedule First."
    )

    st.stop()

if "project_start_date" not in st.session_state:

    st.warning(
        "Please set Project Start Date in Project Data page."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

project_start = st.session_state["project_start_date"]

project_name = st.session_state.get(
    "project_name",
    "-"
)

project_number = st.session_state.get(
    "project_number",
    "-"
)

st.info(
    f"""
Project: {project_name}

Project Number: {project_number}

Project Start Date: {project_start.strftime('%d-%b-%Y')}
"""
)

# =====================================================
# TOPOLOGICAL SORT
# =====================================================

def build_schedule_order(df):

    graph = defaultdict(list)

    indegree = {}

    activities = df["Activity ID"].tolist()

    for act in activities:

        indegree[act] = 0

    for _, row in df.iterrows():

        activity = row["Activity ID"]

        predecessors = [

            row.get("Pred1", ""),
            row.get("Pred2", ""),
            row.get("Pred3", "")

        ]

        for pred in predecessors:

            pred = str(pred).strip()

            if pred and pred != "nan":

                graph[pred].append(activity)

                indegree[activity] += 1

    queue = deque()

    for act in activities:

        if indegree[act] == 0:

            queue.append(act)

    ordered = []

    while queue:

        node = queue.popleft()

        ordered.append(node)

        for succ in graph[node]:

            indegree[succ] -= 1

            if indegree[succ] == 0:

                queue.append(succ)

    return ordered

# =====================================================
# WORKING DAY CALENDAR
# =====================================================

def add_working_days(
    start_date,
    duration,
    calendar_type
):

    current_date = start_date

    days_added = 0

    while days_added < duration - 1:

        current_date += timedelta(days=1)

        # 5 Day Calendar
        if calendar_type == "5D":

            if current_date.weekday() < 5:
                days_added += 1

        # 6 Day Calendar
        else:

            if current_date.weekday() < 6:
                days_added += 1

    return current_date

# =====================================================
# BULK LOGIC ASSIGNMENT
# =====================================================

st.subheader("🔗 Bulk Predecessor Assignment")

user_df = df[df["Logic Type"] == "USER"]

if len(user_df) > 0:

    activity_options = [

        f"{row['Activity ID']} | {row['Activity Description']}"

        for _, row in user_df.iterrows()

    ]

    col1, col2 = st.columns(2)

    with col1:

        successor = st. "Successor Activity",
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

st.subheader("📋 Logic Summary")

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
    height=300,
    hide_index=True
)

# =====================================================
# VALIDATION
# =====================================================

st.divider()

st.subheader("✅ Logic Validation")

issues = []

activity_ids = set(
    df["Activity ID"].astype(str)
)

for _, row in df.iterrows():

    activity_id = str(
        row["Activity ID"]
    )

    predecessors = [

        str(row.get("Pred1", "")).strip(),
        str(row.get("Pred2", "")).strip(),
        str(row.get("Pred3", "")).strip()

    ]

    for pred in predecessors:

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

if issues:

    st.error(
        f"{len(issues)} Issue(s) Found"
    )

    for issue in issues:

        st.write(f"❌ {issue}")

else:

    st.success(
        "No Logic Issues Found"
    )

# =====================================================
# CALENDAR RULES
# =====================================================

st.divider()

st.info("""
Calendar Rules

• ENGG DM = 5 Day Calendar (Mon-Fri)

• BM / BE / SC / WS-P / WS-H / MA = 6 Day Calendar (Mon-Sat)
""")

# =====================================================
# CALCULATE SCHEDULE
# =====================================================

st.subheader("📅 Calculate Schedule")

if st.button("Calculate Schedule"):

    schedule_df = st.session_state[
        "schedule_df"
    ].copy()

    schedule_order = build_schedule_order(
        schedule_df
    )

    if len(schedule_order) != len(schedule_df):

        st.error(
            "Circular Logic Detected. Schedule Cannot Be Calculated."
        )

        st.stop()

    activity_dates = {}

    for activity_id in schedule_order:

        row = schedule_df[
            schedule_df["Activity ID"] == activity_id
        ].iloc[0]

        idx = row.name

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
                and pred != "nan"
                and pred in activity_dates
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
                        p["Finish"]
                        for p in predecessor_dates
                    ) + timedelta(days=1 + lag)
                )

            elif relationship == "SS":

                start_date = (
                    max(
                        p["Start"]
                        for p in predecessor_dates
                    ) + timedelta(days=lag)
                )

            elif relationship == "FF":

                finish_ref = (
                    max(
                        p["Finish"]
                        for p in predecessor_dates
                    ) + timedelta(days=lag)
                )

                start_date = (
                    finish_ref -
                    timedelta(days=duration - 1)
                )

            elif relationship == "SF":

                finish_ref = (
                    max(
                        p["Start"]
                        for p in predecessor_dates
                    ) + timedelta(days=lag)
                )

                start_date = (
                    finish_ref -
                    timedelta(days=duration - 1)
                )

            else:

                start_date = pd.Timestamp(
                    project_start
                )

        scope_curve = str(
            row["S-Curve Scope"]
        ).upper()

        if "ENG" in scope_curve:

            calendar_type = "5D"

        else:

            calendar_type = "6D"

        finish_date = add_working_days(
            start_date,
            duration,
            calendar_type
        )

        activity_dates[
            activity_id
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

        schedule_df.loc[
            idx,
            "Calendar"
        ] = calendar_type

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

st.subheader("📊 Current Schedule")

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

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    review_df.to_excel(
        writer,
        sheet_name="Schedule",
        index=False
    )

st.download_button(
    "📥 Download Excel Schedule",
    excel_buffer.getvalue(),
    "TKIL_Schedule.xlsx"
)

csv_data = review_df.to_csv(
    index=False
)

st.download_button(
    "📥 Download CSV Schedule",
    csv_data,
    "TKIL_Schedule.csv"
)
