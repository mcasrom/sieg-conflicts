import streamlit as st
import pandas as pd

st.title("🌍 Radar Conflictos")

try:
    df=pd.read_csv("../data/processed/history.csv")
except:
    st.warning("No data")
    st.stop()

latest=df.sort_values("timestamp").groupby("pais").tail(1)

st.dataframe(latest.sort_values("score",ascending=False))
st.line_chart(df.pivot_table(index="timestamp",columns="pais",values="score"))
