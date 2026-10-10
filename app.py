import streamlit as st

from utils.theme import apply_theme

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = False

st.session_state["dark_mode"] = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state["dark_mode"],
    key="global_dark_mode"
)

apply_theme()

st.set_page_config(
    page_title="Scheduler Engine",
    page_icon="📅",
    layout="wide"
)

st.title("📅 TKIL Procurement Automated Scheduler")

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
