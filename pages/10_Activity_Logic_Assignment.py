import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Activity Logic Assignment",
    layout="wide"
)

st.title("🔗 Activity Logic Assignment")

if "schedule_df" not in st.session_state:

    st.warning(
        "Generate Schedule First"
    )

    st.stop()

df = st.session_state["schedule_df"]

# Only allow user logic activities

editable_df = df[
    df["Logic Type"] == "USER"
]

if len(editable_df) == 0:

    st.warning(
        "No editable activities found."
    )

    st.stop()

activity_ids = sorted(
    df["Activity ID"]
    .astype(str)
    .tolist()
)

selected_activity = st.selectbox(
    "Select Activity",
    editable_df["Activity ID"]
)

selected_row = editable_df[
    editable_df["Activity ID"]
    == selected_activity
].iloc[0]

st.write(
    f"### {selected_row['Activity Description']}"
)

pred1 = st.selectbox(
    "Predecessor",
    [""] + activity_ids
)

relationship = st.selectbox(
    "Relationship",
    ["FS", "SS", "FF", "SF"]
)

lag = st.number_input(
    "Lag (Days)",
    value=0
)

if st.button("Save Logic"):

    row_index = df[
        df["Activity ID"]
        == selected_activity
    ].index[0]

    df.loc[row_index, "Pred1"] = pred1

    df.loc[row_index, "Relationship"] = relationship

    df.loc[row_index, "Lag"] = lag

    st.session_state["schedule_df"] = df

    st.success(
        "Logic Updated Successfully"
    )

st.divider()

st.subheader(
    "Activities Available For Logic Assignment"
)

st.dataframe(
    editable_df[
        [
            "Activity ID",
            "WBS Name",
            "Fragnet ID",
            "Activity Description"
        ]
    ],
    width="stretch"
)
