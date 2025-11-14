import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page title
st.title("Cloud Cost Dashboard")
st.set_page_config(page_title="Cloud Cost Dashboard", layout="wide")

# Load data
data = pd.read_csv("cloud_costs.csv")

# Show the table
st.subheader("Cloud Cost Data")
st.dataframe(data)

# Total cost summary
st.subheader("Total Cost by Provider")
total_cost = data.groupby("provider")["cost"].sum()
st.bar_chart(total_cost)

# Cost over time
st.subheader("Daily Cloud Cost Trend")
daily_cost = data.groupby(["date", "provider"])["cost"].sum().unstack()
st.line_chart(daily_cost)

# Pie chart
st.subheader("Cost Distribution by Provider")
fig, ax = plt.subplots()
ax.pie(total_cost, labels=total_cost.index, autopct="%1.1f%%")
st.pyplot(fig)


# Sidebar filters
st.sidebar.header("🔍 Filters")

# Provider filter
provider_list = ["All"] + list(data["provider"].unique())
selected_provider = st.sidebar.selectbox("Select Cloud Provider", provider_list)

# Date filter
date_list = ["All"] + list(data["date"].unique())
selected_date = st.sidebar.selectbox("Select Date", date_list)

# Apply filters
filtered_data = data.copy()

if selected_provider != "All":
    filtered_data = filtered_data[filtered_data["provider"] == selected_provider]

if selected_date != "All":
    filtered_data = filtered_data[filtered_data["date"] == selected_date]

# ---- Summary Cards ----
st.subheader("Summary")

total_cost = filtered_data["cost"].sum()
avg_cost = filtered_data["cost"].mean()
provider_count = filtered_data["provider"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Cost", f"${total_cost:,.2f}")
col2.metric("Average Cost", f"${avg_cost:,.2f}")
col3.metric("Providers", provider_count)

# ---- Charts ----
st.divider()
st.subheader("Filtered Cloud Cost Data")
st.dataframe(filtered_data)

st.subheader("Total Cost by Provider")
total_cost_chart = filtered_data.groupby("provider")["cost"].sum()
st.bar_chart(total_cost_chart)

st.subheader("Daily Cost Trend")
daily_cost = filtered_data.groupby(["date", "provider"])["cost"].sum().unstack()
st.line_chart(daily_cost)

st.subheader("Cost Distribution by Provider")
fig, ax = plt.subplots()
ax.pie(total_cost_chart, labels=total_cost_chart.index, autopct="%1.1f%%")
st.pyplot(fig)
