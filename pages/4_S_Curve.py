import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 S-Curve")

if "schedule_df" not in st.session_state:
    st.warning("Generate schedule first.")
    st.stop()

df = st.session_state["schedule_df"].copy()

total_duration = df["Duration"].sum()

df["Weight"] = (
    df["Duration"] / total_duration
) * 100

df["Cumulative"] = df["Weight"].cumsum()

fig = px.line(
    df,
    x=df.index + 1,
    y="Cumulative",
    markers=True,
    title="Planned S-Curve"
)

fig.update_layout(
    xaxis_title="Activity Sequence",
    yaxis_title="Cumulative Progress %"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    df[
        [
            "Activity ID",
            "Activity Description",
            "Weight",
            "Cumulative"
        ]
    ],
    use_container_width=True
)
