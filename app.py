import streamlit as st
import pandas as pd
from constants import state_list
from utils import process_excel

st.set_page_config(
page_title="AdvaitInsight - KOL AI Agent",
page_icon="🧠",
layout="centered"
)

st.title("🤖 AdvaitInsight - Healthcare Research AI Agent")
st.markdown("Autofill institute & personnel data for selected state using AI agent.")

uploaded_file = st.file_uploader(
label="📤 Upload Excel File (.xlsx format only)",
type=["xlsx"]
)

selected_state = st.selectbox("🌍 Select State:", state_list)

if st.button("✨ Autofill State Data"):
if uploaded_file is not None and selected_state:
df = pd.read_excel(uploaded_file, engine="openpyxl")
filled_df = process_excel(df, selected_state)
 st.success("✅ Data filled for selected state.")  
    st.download_button(  
        label="📥 Download Completed Excel File",  
        data=filled_df.to_excel(index=False, engine='openpyxl'),  
        file_name=f"{selected_state}_filled.xlsx",  
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  
    )  
else:  
    st.warning("⚠️ Please upload a file and select a state first.")
