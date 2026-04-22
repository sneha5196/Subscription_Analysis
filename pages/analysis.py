import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

df = st.session_state['df']

st.title("📊 Detailed Analysis")

# -------- Plotly Chart --------
st.subheader("📊 Revenue by Company (Plotly)")
fig = px.bar(df.groupby('Company')['Monthly_Fee'].sum().reset_index(),
             x='Company', y='Monthly_Fee')
st.plotly_chart(fig)

# -------- Matplotlib --------
st.subheader("📈 Monthly Revenue (Matplotlib)")

monthly = df.groupby('Month')['Monthly_Fee'].sum()

plt.figure()
plt.plot(monthly.index, monthly.values)
plt.xticks(rotation=45)
plt.title("Monthly Revenue Trend")
st.pyplot(plt)

# -------- Country --------
st.subheader("🌍 Revenue by Country")
fig2 = px.pie(df, names='Country', values='Monthly_Fee')
st.plotly_chart(fig2)
