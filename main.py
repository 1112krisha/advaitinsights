import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.getcwd())
from excel_generator import create_excel_for_state
from constants import STATES

st.set_page_config(page_title="AdvaitInsight - KOL AI Agent", layout="wide")

st.title("🧠 AdvaitInsight - KOL AI Agent")
st.markdown("Generate Excel sheets with realistic institute and personnel data for your selected Indian state.")

# Step 1: Select State
selected_state = st.selectbox("Select a State", STATES)

# Step 2: Generate Data & Excel
if st.button("🔄 Generate Excel for Selected State"):
    with st.spinner("Generating data..."):
        file_path, df = create_excel_for_state(selected_state)
        st.success("Excel file generated successfully!")
        
        # Step 3: Show preview
        st.subheader("🔍 Preview of Generated Data")
        st.dataframe(df)

        # Step 4: Download
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download Excel File",
                data=f,
                file_name="advait_kol_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
