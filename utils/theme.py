import streamlit as st

def apply_theme():

    dark_mode = st.session_state.get(
        "dark_mode",
        False
    )

    if dark_mode:

        st.markdown(
            """
            <style>
            .stApp{
                background-color:#0E1117;
                color:white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
