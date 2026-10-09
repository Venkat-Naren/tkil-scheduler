import streamlit as st

st.set_page_config(
    page_title="TKIL Automated Scheduler",
    page_icon="📅",
    layout="wide"
)

st.title("📅 TKIL Automated Scheduler")

st.markdown("""
### Welcome

This application will help Project Managers:

✅ Upload WBS Data

✅ Generate Schedules from Fragnet Templates

✅ Create Activity IDs Automatically

✅ Assign Predecessors

✅ Generate Gantt Charts

✅ Generate S-Curves

✅ Track Progress

✅ Export Schedules

---

### Navigation

Use the left sidebar to access:

- WBS Upload
- Schedule Generator
- Gantt Chart
- S-Curve
- Dashboard
""")

st.info(
    "Upload your WBS file from the WBS Upload page to get started."
)
