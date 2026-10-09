import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Excel Export",
    layout="wide"
)

st.title("📥 Export Schedule")

if "schedule_df" not in st.session_state:

    st.warning(
        "Please generate the schedule first."
    )

    st.stop()

df = st.session_state["schedule_df"]

st.subheader("Schedule Preview")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

output = BytesIO()

with pd.ExcelWriter(
    output,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False,
        sheet_name="Schedule"
    )

st.download_button(
    label="📥 Download Schedule Excel",
    data=output.getvalue(),
    file_name="TKIL_Schedule.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Schedule CSV",
    data=csv,
    file_name="TKIL_Schedule.csv",
    mime="text/csv"
)
