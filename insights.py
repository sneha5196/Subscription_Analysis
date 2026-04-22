import streamlit as st
import pandas as pd

df = st.session_state['df']

st.title("🧠 Advanced Insights")

# -------- Quarterly Table --------
st.subheader("📊 Quarterly Revenue")

quarter = df.groupby('Quarter')['Monthly_Fee'].sum().reset_index()
st.dataframe(quarter)

# -------- Top Plan --------
top_plan = df.groupby('Plan')['Monthly_Fee'].sum().idxmax()
top_country = df.groupby('Country')['Monthly_Fee'].sum().idxmax()

st.success(f"Top Plan: {top_plan}")
st.success(f"Top Country: {top_country}")

# -------- Churn Analysis --------
st.subheader("📉 Churn Analysis")

churn_dist = df['Churn'].value_counts()
st.bar_chart(churn_dist)

# -------- Insight --------
if df['Churn'].mean() > 0.4:
    st.error("High churn rate detected!")
else:
    st.success("Churn rate is under control")