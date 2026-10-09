import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Schedule Generator",
    layout="wide"
)

st.title("⚙️ Schedule Generator")

# Check WBS Upload

if "wbs_df" not in st.session_state:

    st.warning(
        "Please upload WBS data first."
    )

    st.stop()

# Check Fragnet Master

if "fragnet_master" not in st.session_state:

    st.warning(
        "Please upload Fragnet Master first."
    )

    st.stop()

wbs_df = st.session_state["wbs_df"]

fragnet_master = st.session_state["fragnet_master"]

st.subheader("Uploaded WBS Data")

st.dataframe(
    wbs_df,
    width="stretch"
)

if st.button("Generate Schedule"):

    schedule = []

    activity_counter = 1

    for _, wbs in wbs_df.iterrows():

        scope = str(
            wbs["WBS Scope"]
        ).strip()

        matching_fragnets = fragnet_master[
            fragnet_master["WBS Scope"]
            .astype(str)
            .str.strip()
            == scope
        ]

        if len(matching_fragnets) == 0:

            st.warning(
                f"No Fragnets Found For Scope: {scope}"
            )

            continue

        for _, fragnet in matching_fragnets.iterrows():

            schedule.append({

                "Activity ID":
                    f"A{activity_counter:04d}",

                "TKIL SAP WBS Code":
                    wbs["TKIL SAP WBS Code"],

                "WBS Name":
                    wbs["WBS Name"],

                "WBS Scope":
                    scope,

                "Fragnet ID":
                    fragnet["Fragnet ID"],

                "Activity Description":
                    f"{wbs['WBS Name']} - "
                    f"{fragnet['Activity Description']}",

                "S-Curve Scope":
                    fragnet["S-Curve Scope"],

                "Duration":
                    fragnet["Duration (Days)"],

                "Pred1": "",

                "Pred2": "",

                "Pred3": "",

                "Relationship": "FS",

                "Lag": 0,

                "Start Date": None,

                "Finish Date": None,

                "% Complete": 0

            })

            activity_counter += 1

    schedule_df = pd.DataFrame(schedule)

    st.session_state["schedule_df"] = schedule_df

    st.success(
        f"Schedule Generated Successfully "
        f"({len(schedule_df)} Activities)"
    )

    st.subheader("Generated Schedule")

    st.dataframe(
        schedule_df,
        width="stretch",
        height=600
    )

    csv = schedule_df.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Schedule CSV",
        data=csv,
        file_name="generated_schedule.csv",
        mime="text/csv"
    )
