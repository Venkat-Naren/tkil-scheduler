import streamlit as st

def init_theme():

    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False


def theme_toggle():

    st.sidebar.markdown("---")

    st.session_state["dark_mode"] = st.sidebar.toggle(
        "🌙 Dark Mode",
        value=st.session_state["dark_mode"]
    )


def apply_theme():

    dark_mode = st.session_state.get(
        "dark_mode",
        False
    )

    if dark_mode:

        css = """
        <style>

        .stApp{
            background-color:#0E1117;
            color:white;
        }

        section[data-testid="stSidebar"]{
            background-color:#161B22;
        }

        div[data-testid="metric-container"]{
            background-color:#1F2937;
            border:1px solid #374151;
            border-radius:10px;
            padding:15px;
        }

        thead tr th{
            background-color:#1F2937 !important;
            color:white !important;
        }

        tbody tr td{
            background-color:#111827 !important;
            color:white !important;
        }

        tbody tr:nth-child(even) td{
            background-color:#1F2937 !important;
        }

        </style>
        """

    else:

        css = """
        <style>

        div[data-testid="metric-container"]{
            border:1px solid #D1D5DB;
            border-radius:10px;
            padding:15px;
        }

        </style>
        """

    st.markdown(
        css,
        unsafe_allow_html=True
    )
