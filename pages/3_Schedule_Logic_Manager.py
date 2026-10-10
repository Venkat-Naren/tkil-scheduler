import streamlit as st
import pandas as pd
from datetime import timedelta
from collections import defaultdict, deque
from io import BytesIO

st.set_page_config(
    page_title="Schedule Logic Manager",
    layout="wide"
)

st.title("🔗 Schedule Logic Manager")

# =====================================================
# VALIDATION
# =====================================================

if "schedule_df" not in st.session_state:

    st.warning(
        "Please Generate Schedule First."
    )

    st.stop()

if "project_start_date" not in st.session_state:

    st.warning(
        "Please Set Project Start Date In Project Data Page."
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

# =====================================================
# PROJECT INFO
# =====================================================

st.info(
    f"""
Project: {project_name}

Project Number: {project_number}

Project Start Date: {project_start.strftime('%d-%b-%Y')}
"""
)

# =====================================================
# SCHEDULE HEALTH
# =====================================================

st.subheader("📊 Schedule Health")

total_activities = len(df)

user_logic = len(
    df[df["Logic Type"] == "USER"]
)

missing_logic = len(
    df[
        (df["Logic Type"] == "USER")
        &
        (
            df["Pred1"].fillna("")
            == ""
        )
    ]
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Activities",
    total_activities
)

c2.metric(
    "User Logic Activities",
    user_logic
)

c3.metric(
    "Missing Logic",
    missing_logic
)

# =====================================================
# FILTERS
# =====================================================

st.divider()

st.subheader("🔍 Filters")

col1, col2 = st.columns(2)

with col1:

    search_text = st.text_input(
        "Search Activity"
    )

with col2:

    selected_scope = st.multiselect(
        "Filter WBS Scope",
        sorted(
            df["WBS Scope"].unique()
        ),
        default=sorted(
            df["WBS Scope"].unique()
        )
    )

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["WBS Scope"]
    .isin(selected_scope)
]

if search_text:

    filtered_df = filtered_df[
        filtered_df[
            "Activity Description"
        ].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# =====================================================
# EDITABLE USER LOGIC GRID
# =====================================================

st.divider()

st.subheader("🔗 User Logic Activities")

editable_logic_df = filtered_df[
    filtered_df["Logic Type"] == "USER"
][[
    "Activity ID",
    "Activity Description",
    "Pred1",
    "Pred2",
    "Pred3",
    "Relationship",
    "Lag"
]]

edited_logic = st.data_editor(
    editable_logic_df,
    width="stretch",
    height=400,
    hide_index=True
)

if st.button("💾 Save Logic Grid"):

    for _, edit_row in edited_logic.iterrows():

        act_id = edit_row["Activity ID"]

        idx = df[
            df["Activity ID"] == act_id
        ].index[0]

        df.loc[idx, "Pred1"] = edit_row["Pred1"]

        df.loc[idx, "Pred2"] = edit_row["Pred2"]

        df.loc[idx, "Pred3"] = edit_row["Pred3"]

        df.loc[idx, "Relationship"] = (
            edit_row["Relationship"]
        )

        df.loc[idx, "Lag"] = edit_row["Lag"]

    st.session_state[
        "schedule_df"
    ] = df

    st.success(
        "Logic Grid Saved"
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

        if pred in ["", "nan"]:
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

        st.write(
            f"❌ {issue}"
        )

else:

    st.success(
        "No Logic Issues Found"
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

# =================================CALENDAR FUNCTION
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

        if calendar_type == "5D":

            if current_date.weekday() < 5:
                days_added += 1

        else:

            if current_date.weekday() < 6:
                days_added += 1

    return current_date

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

    schedule_df = df.copy()

    schedule_order = build_schedule_order(
        schedule_df
    )

    if len(schedule_order) != len(schedule_df):

        st.error(
            "Circular Logic Detected"
        )

        st.stop()

    activity_dates = {}

    for activity_id in schedule_order:

        row = schedule_df[
            schedule_df["Activity ID"]
            == activity_id
        ].iloc[0]

        idx = row.name

        duration = int(
            row["Duration"]
        )

        lag = int(
            row.get("Lag", 0)
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
                pred
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

            start_date = (
                max(
                    p["Finish"]
                    for p in predecessor_dates
                )
                + timedelta(days=1 + lag)
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
# SCHEDULE REVIEW
# =====================================================

st.divider()

st.subheader("📋 Schedule Review")

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
    label="📥 Download Excel Schedule",
    data=excel_buffer.getvalue(),
    file_name="TKIL_Schedule.xlsx"
)

csv_data = review_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download CSV Schedule",
    data=csv_data,
    file_name="TKIL_Schedule.csv"
)
