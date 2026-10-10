import streamlit as st

def apply_theme(dark_mode):

    if dark_mode:

        st.markdown(
            """
            <style>

            .stApp {
                background:#0E1117;
                color:white;
            }

            </style>
            """,
            unsafe_allow_html=True
        )
