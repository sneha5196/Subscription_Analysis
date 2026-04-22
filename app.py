import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Subscription Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("multi_company_data.csv")

    df['Start_Date'] = pd.to_datetime(df['Start_Date'])
    df['Churn'] = df['End_Date'].notnull().astype(int)
    df['Month'] = df['Start_Date'].dt.to_period('M').astype(str)
    df['Quarter'] = df['Start_Date'].dt.to_period('Q').astype(str)

    return df

df = load_data()

# ✅ STORE IN SESSION STATE (for other pages like insights.py)
if 'df' not in st.session_state:
    st.session_state['df'] = df

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filters")

company = st.sidebar.multiselect(
    "🏢 Company",
    df['Company'].unique(),
    df['Company'].unique()
)

plan = st.sidebar.multiselect(
    "📊 Plan",
    df['Plan'].unique(),
    df['Plan'].unique()
)

country = st.sidebar.multiselect(
    "🌍 Country",
    df['Country'].unique(),
    df['Country'].unique()
)

# ---------------- FILTER ----------------
filtered_df = df[
    (df['Company'].isin(company)) &
    (df['Plan'].isin(plan)) &
    (df['Country'].isin(country))
]

# ---------------- HEADER ----------------
st.title("📊 Subscription Revenue Analysis Dashboard")

# ---------------- KPI ----------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"₹{filtered_df['Monthly_Fee'].sum():,}")
col2.metric("👥 Users", filtered_df['User_ID'].nunique())
col3.metric("📉 Churn Rate", f"{round(filtered_df['Churn'].mean()*100,2)}%")

# ---------------- MONTHLY TREND ----------------
st.subheader("📈 Monthly Revenue Trend")
monthly = filtered_df.groupby('Month')['Monthly_Fee'].sum()
st.line_chart(monthly)

# ---------------- 2 MONTH COMPARISON ----------------
if len(monthly) >= 2:
    st.subheader("⚡ Last 2 Months Comparison")
    last_2 = monthly.tail(2)

    col4, col5 = st.columns(2)

    col4.metric(last_2.index[0], f"₹{last_2.iloc[0]:,}")
    col5.metric(
        last_2.index[1],
        f"₹{last_2.iloc[1]:,}",
        delta=f"{last_2.iloc[1] - last_2.iloc[0]:,}"
    )

# ---------------- COMPANY LOGIC ----------------
st.subheader("🏢 Company Analysis")

if len(company) == 1:

    st.success(f"Showing detailed analysis for {company[0]}")

    col6, col7 = st.columns(2)

    with col6:
        st.subheader("📊 Revenue by Plan")
        st.bar_chart(filtered_df.groupby('Plan')['Monthly_Fee'].sum())

    with col7:
        st.subheader("🌍 Revenue by Country")
        st.bar_chart(filtered_df.groupby('Country')['Monthly_Fee'].sum())

else:
    st.subheader("📊 Company Comparison")
    st.bar_chart(filtered_df.groupby('Company')['Monthly_Fee'].sum())

# ---------------- QUARTERLY TABLE ----------------
st.subheader("📊 Quarterly Revenue Table")
quarter = filtered_df.groupby('Quarter')['Monthly_Fee'].sum().reset_index()
st.dataframe(quarter, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("🧠 Insights")

if len(filtered_df) > 0:
    top_plan = filtered_df.groupby('Plan')['Monthly_Fee'].sum().idxmax()
    top_country = filtered_df.groupby('Country')['Monthly_Fee'].sum().idxmax()

    st.info(f"💡 Top Plan: {top_plan}")
    st.info(f"🌍 Top Country: {top_country}")
else:
    st.warning("No data available for selected filters")

# ---------------- FOOTER ----------------