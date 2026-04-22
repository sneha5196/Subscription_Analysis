import streamlit as st
import pandas as pd

df = st.session_state['df']

st.title("📊 Overview Dashboard")

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"₹{df['Monthly_Fee'].sum():,}")
col2.metric("Users", df['User_ID'].nunique())
col3.metric("Churn", f"{round(df['Churn'].mean()*100,2)}%")

# Monthly trend
st.subheader("📈 Monthly Trend")
monthly = df.groupby('Month')['Monthly_Fee'].sum()
st.line_chart(monthly)
