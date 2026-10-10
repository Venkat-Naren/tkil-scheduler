import streamlit as st

def apply_theme(dark_mode):

   if dark_mode:

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }

        section[data-testid="stSidebar"] {
            background-color: #161B22;
        }

        /* DataFrame */

        div[data-testid="stDataFrame"] {

            border: 1px solid #30363D;
            border-radius: 8px;
        }

        /* Table Header */

        thead tr th {

            background-color: #1F2937 !important;
            color: #FFFFFF !important;
            font-weight: bold !important;
        }

        /* Table Cells */

        tbody tr td {

            background-color: #111827 !important;
            color: #F9FAFB !important;
            border-color: #374151 !important;
        }

        /* Alternate Row Shading */

        tbody tr:nth-child(even) td {

            background-color: #1F2937 !important;
        }

        /* Hover */

        tbody tr:hover td {

            background-color: #2563EB !important;
            color: white !important;
        }

        /* Metric Cards */

        div[data-testid="metric-container"] {

            background-color: #1F2937;
            border: 1px solid #374151;
            padding: 15px;
            border-radius: 10px;
        }

        /* Buttons */

        .stButton button {

            background-color: #2563EB;
            color: white;
            border-radius: 8px;
            border: none;
        }

        /* Select Boxes */

        div[data-baseweb="select"] {

            background-color: #1F2937;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
