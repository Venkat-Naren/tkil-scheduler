import streamlit as st
import plotly.graph_objects as go

st.title("📈 Planned vs Actual S-Curve")

if "schedule_df" not in st.session_state:

    st.stop()

df = st.session_state["schedule_df"]

if "% Complete" not in df.columns:

    df["% Complete"] = 0

df["Weight"] = (

    df["Duration"]

    /

    df["Duration"].sum()

) * 100

df["Planned"] = (
    df["Weight"]
    .cumsum()
)

df["Actual"] = (
    (
        df["Weight"]
        *
        df["% Complete"]
        / 100
    )
    .cumsum()
)

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=df.index,

        y=df["Planned"],

        name="Planned"

    )

)

fig.add_trace(

    go.Scatter(

        x=df.index,

        y=df["Actual"],

        name="Actual"

    )

)

st.plotly_chart(
    fig,
    width="stretch"
)
