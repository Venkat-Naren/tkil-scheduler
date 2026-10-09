import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("⚙️ Schedule Generator")

if "wbs_df" not in st.session_state:
    st.warning("Please upload a WBS file first.")
    st.stop()

wbs_df = st.session_state["wbs_df"]

st.subheader("Uploaded WBS Data")
st.dataframe(wbs_df, use_container_width=True)

# Temporary Fragnet Library
if "fragnet_master" not in st.session_state:

    st.warning(
        "Please upload Fragnet Master first."
    )

    st.stop()

fragnet_master = st.session_state["fragnet_master"]
if st.button("Generate Schedule"):

    schedule = []
    activity_counter = 1

    for _, wbs in wbs_df.iterrows():

        matching_fragnets = fragnet_master[
            fragnet_master["WBS Scope"] == wbs["WBS Scope"]
        ]

        for _, fragnet in matching_fragnets.iterrows():

           schedule.append({
    "Activity ID": f"A{activity_counter:04d}",
    "TKIL SAP WBS Code": wbs["TKIL SAP WBS Code"],
    "WBS Name": wbs["WBS Name"],
    "WBS Scope": wbs["WBS Scope"],
    "Fragnet ID": fragnet["Fragnet ID"],
    "Activity Description":
        f"{wbs['WBS Name']} - {fragnet['Activity Description']}",
    "S-Curve Scope": fragnet["S-Curve Scope"],
    "Duration": fragnet["Duration (Days)"],
    "Pred1": "",
    "Pred2": "",
    "Pred3": "",
    "Relationship": "FS",
    "% Complete": 0
})

            activity_counter += 1

    schedule_df = pd.DataFrame(schedule)

    st.session_state["schedule_df"] = schedule_df

    st.success(
        f"Schedule Generated: {len(schedule_df)} Activities"
    )

    st.dataframe(
        schedule_df,
        use_container_width=True,
        height=600
    )

    csv = schedule_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Schedule",
        data=csv,
        file_name="generated_schedule.csv",
        mime="text/csv"
    )
