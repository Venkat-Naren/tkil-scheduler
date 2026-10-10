import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Schedule Generator",
    layout="wide"
)

st.title("⚙️ Schedule Generator")

# --------------------------------------------------
# Check Data
# --------------------------------------------------

if "wbs_df" not in st.session_state:

    st.warning(
        "Please upload WBS data first."
    )

    st.stop()

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

# --------------------------------------------------
# Generate Schedule
# --------------------------------------------------

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

        if matching_fragnets.empty:

            st.warning(
                f"No Fragnets Found For Scope: {scope}"
            )

            continue

        previous_activity = ""

        for _, fragnet in matching_fragnets.iterrows():

            activity_id = f"A{activity_counter:04d}"

            fragnet_desc = str(
                fragnet["Activity Description"]
            )

            activity_name = (
                f"{wbs['WBS Name']} - "
                f"{fragnet_desc}"
            )

            # ----------------------------------------
            # USER DEFINES ONLY FIRST FRAGNET
            # ----------------------------------------

            if (
                "Release of Tech. Specifications/PR"
                in fragnet_desc
                or
                "Release of mfg drgs/JRM"
                in fragnet_desc
            ):

                logic_type = "USER"

                pred1 = ""

            else:

                logic_type = "AUTO FS"

                pred1 = previous_activity

            schedule.append({

                "Activity ID":
                    activity_id,

                "TKIL SAP WBS Code":
                    wbs["TKIL SAP WBS Code"],

                "WBS Name":
                    wbs["WBS Name"],

                "WBS Scope":
                    scope,

                "Fragnet ID":
                    fragnet["Fragnet ID"],

                "Activity Description":
                    activity_name,

                "S-Curve Scope":
                    fragnet["S-Curve Scope"],

                "Duration":
                    fragnet["Duration (Days)"],

                "Logic Type":
                    logic_type,

                "Pred1":
                    pred1,

                "Pred2":
                    "",

                "Pred3":
                    "",

                "Relationship":
                    "FS",

                "Lag":
                    0,

                "Start Date":
                    None,

                "Finish Date":
                    None,

                "% Complete":
                    0

            })

            previous_activity = activity_id

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
