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
fragnet_master = pd.DataFrame([
    ["SC","SC-001","Release of mfg drgs/JRM","ENGG DM",5],
    ["SC","SC-002","Issue of Inquiry & Receipt of Offer, bid evaluation","SC",7],
    ["SC","SC-003","Finalisation of Order","SC",8],
    ["BM","BM-001","Release of Tech. Specifications/PR","ENGG DM",5],
    ["BM","BM-002","Issue of Inquiry & Receipt of Offer, bid evaluation","BM",7],
    ["BM","BM-003","Technical Evaluation","ENGG DM",10],
    ["BE","BE-001","Release of Tech. Specifications/PR","ENGG DM",5],
    ["BE","BE-002","Issue of Inquiry & Receipt of Offer, bid evaluation","BE",7],
    ["MA","MA-001","Release of Tech. Specifications/PR","ENGG DM",5],
    ["MA","MA-002","Issue of Inquiry & Receipt of Offer, bid evaluation","MA",7]
],
columns=[
    "WBS Scope",
    "Fragnet ID",
    "Activity Description",
    "S-Curve Scope",
    "Duration"
])

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
                "Duration": fragnet["Duration"],
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
