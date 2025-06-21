import streamlit as st
from utils.gsheet import get_data_from_sheet

st.set_page_config(page_title="Advait Insights", layout="wide")
st.title("🔍 ADVAIT INSIGHTS - Market Research Dashboard")

df = get_data_from_sheet()

# Filters
with st.sidebar:
    st.header("📂 Filter Insights")
    category = st.multiselect("Category", df["Category"].unique())
    insight_type = st.multiselect("Insight Type", df["Insight Type"].unique())
    priority = st.multiselect("Priority", df["Priority"].unique())

# Apply filters
if category:
    df = df[df["Category"].isin(category)]
if insight_type:
    df = df[df["Insight Type"].isin(insight_type)]
if priority:
    df = df[df["Priority"].isin(priority)]

# Show Insights
st.subheader("📊 Latest Insights")
for _, row in df.iterrows():
    st.markdown(f"### {row['Company Name']} | {row['What Happened']}")
    st.markdown(f"**Date:** {row['Date']}  |  **Category:** {row['Category']}  |  **Priority:** {row['Priority']}")
    st.markdown(f"**Summary:** {row['AI Summary']}")
    st.markdown(f"**Advait Angle:** _{row['Advait Angle']}_")
    st.markdown(f"[🔗 Source]({row['Source Link']})")
    st.markdown("---")
