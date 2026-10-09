import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Logic Builder",
    layout="wide"
)

st.title("🔗 Schedule Logic Builder")

if "schedule_df" not in st.session_state:

    st.warning(
        "Generate Schedule First."
    )

    st.stop()

df = st.session_state["schedule_df"].copy()

st.info(
    "Define activity relationships and predecessors."
)

# Editable grid
edited_df = st.data_editor(
    df,
    use_container_width=True,
    height=700,
    num_rows="fixed"
)

st.session_state["schedule_df"] = edited_df

st.success(
    "Schedule Logic Saved."
)

# Validation Checks

st.divider()

st.subheader("Logic Validation")

activity_list = set(
    edited_df["Activity ID"].astype(str)
)

issues = []

for _, row in edited_df.iterrows():

    activity_id = str(row["Activity ID"])

    for pred_col in ["Pred1", "Pred2", "Pred3"\]:

        pred = str(
            row.get(pred_col, "")
        ).strip()

        if pred == "":
            continue

        if pred not in activity_list:

            issues.append(
                f"{activity_id}: Invalid predecessor {pred}"
            )

        if pred == activity_id:

            issues.append(
                f"{activity_id}: Cannot be predecessor to itself"
            )

if len(issues) > 0:

    st.error(
        f"{len(issues)} Logic Issues Found"
    )

    for issue in issues:

        st.write(
            f"❌ {issue}"
        )

else:

    st.success(
        "No logic issues found."
    )
