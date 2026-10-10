import streamlit as st

st.set_page_config(
    page_title="TKIL Scheduler",
    page_icon="📅",
    layout="wide"
)

# Dark Mode Toggle
dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=False
)

if dark_mode:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0E1117;
            color: white;
        }

        section[data-testid="stSidebar"] {
            background-color: #161B22;
        }

        .stMetric {
            background-color: #1E2530;
            padding: 10px;
            border-radius: 10px;
        }

        div[data-testid="stDataFrame"] {
            background-color: #161B22;
        }

        </style>
        """,
        unsafe_allow_html=True
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
