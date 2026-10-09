import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Activity Logic Assignment",
    layout="wide"
)

st.title("🔗 Activity Logic Assignment")

if "schedule_df" not in st.session_state:

    st.warning(
        "Generate Schedule First."
    )

    st.stop()

df = st.session_state["schedule_df"]

activity_list = sorted(
    df["Activity ID"].astype(str).unique()
)

st.subheader("Assign Logic")

selected_activity = st.selectbox(
    "Select Activity",
    activity_list
)

activity_row = df[
    df["Activity ID"] == selected_activity
].iloc[0]

st.write(
    f"**Activity:** {activity_row['Activity Description']}"
)

pred1 = st.selectbox(
    "Predecessor 1",
    [""] + activity_list,
    index=0
)

pred2 = st.selectbox(
    "Predecessor 2",
    [""] + activity_list,
    index=0
)

pred3 = st.selectbox(
    "Predecessor 3",
    [""] + activity_list,
    index=0
)

relationship = st.selectbox(
    "Relationship",
    [
        "FS",
        "SS",
        "FF",
        "SF"
    ]
)

lag_days = st.number_input(
    "Lag Days",
    value=0,
    step=1
)

if st.button("Save Logic"):

    row_index = df[
        df["Activity ID"] == selected_activity
    ].index[0]

    df.loc[row_index, "Pred1"] = pred1
    df.loc[row_index, "Pred2"] = pred2
    df.loc[row_index, "Pred3"] = pred3

    df.loc[row_index, "Relationship"] = relationship

    df.loc[row_index, "Lag"] = lag_days

    st.session_state["schedule_df"] = df

    st.success(
        f"Logic saved for {selected_activity}"
    )

st.divider()

st.subheader("Current Logic")

logic_cols = [
    "Activity ID",
    "Activity Description",
    "Pred1",
    "Pred2",
    "Pred3",
    "Relationship"
]

if "Lag" in df.columns:
    logic_cols.append("Lag")

st.dataframe(
    df[logic_cols],
    use_container_width=True,
    height=500
)

st.divider()

st.subheader("Logic Validation")

issues = []

for _, row in df.iterrows():

    activity = str(row["Activity ID"])

    for pred_col in [
        "Pred1",
        "Pred2",
        "Pred3"
    ]:

        pred = str(
            row.get(pred_col, "")
        ).strip()

        if pred == "":
            continue

        if pred == activity:

            issues.append(
                f"{activity} cannot be its own predecessor"
            )

if issues:

    st.error(
        f"{len(issues)} issue(s) found"
    )

    for issue in issues:

        st.write(
            f"❌ {issue}"
        )

else:

    st.success(
        "No logic issues found"
    )
