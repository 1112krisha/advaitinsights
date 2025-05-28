import streamlit as st
import pandas as pd
import requests
import json
from io import BytesIO
import time
from typing import Dict, List, Any
import openai
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Healthcare AI Agent",
    page_icon="🏥",
    layout="wide"
)

class HealthcareAgent:
    def __init__(self):
        self.healthcare_data = {
            "bihar": {
                "hospitals": [
                    "AIIMS Patna", "Patna Medical College", "Nalanda Medical College",
                    "Darbhanga Medical College", "Katihar Medical College"
                ],
                "services": [
                    "Primary Healthcare", "Secondary Healthcare", "Tertiary Healthcare",
                    "Emergency Services", "Diagnostic Services", "Pharmacy Services",
                    "Telemedicine", "Maternal Health", "Child Health", "Mental Health"
                ],
                "companies": [
                    "Apollo Hospitals", "Fortis Healthcare", "Max Healthcare",
                    "Medanta", "Narayana Health", "Manipal Hospitals"
                ],
                "funding_sources": [
                    "National Health Mission (NHM)", "Pradhan Mantri Jan Arogya Yojana",
                    "Bihar State Health Society", "World Bank Healthcare Projects",
                    "Asian Development Bank", "Government of Bihar Health Budget",
                    "Private Healthcare Investment", "CSR Healthcare Funding"
                ],
                "government_schemes": [
                    "Ayushman Bharat", "Janani Suraksha Yojana", "Rashtriya Bal Swasthya Karyakram",
                    "National Programme for Healthcare of Elderly", "Mission Indradhanush"
                ]
            }
        }
    
    def get_healthcare_info(self, state: str, category: str) -> List[str]:
        """Get healthcare information for specific state and category"""
        state_lower = state.lower()
        if state_lower in self.healthcare_data:
            return self.healthcare_data[state_lower].get(category, [])
        return []
    
    def process_excel_file(self, uploaded_file, state: str) -> pd.DataFrame:
        """Process uploaded Excel file and fill healthcare data"""
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Create a copy to modify
            result_df = df.copy()
            
            # Fill data based on column names
            for column in df.columns:
                column_lower = column.lower()
                
                if any(keyword in column_lower for keyword in ['hospital', 'medical', 'health center']):
                    hospitals = self.get_healthcare_info(state, 'hospitals')
                    result_df[column] = hospitals[:len(df)] if hospitals else ['No data available'] * len(df)
                
                elif any(keyword in column_lower for keyword in ['service', 'treatment']):
                    services = self.get_healthcare_info(state, 'services')
                    result_df[column] = services[:len(df)] if services else ['No data available'] * len(df)
                
                elif any(keyword in column_lower for keyword in ['company', 'provider']):
                    companies = self.get_healthcare_info(state, 'companies')
                    result_df[column] = companies[:len(df)] if companies else ['No data available'] * len(df)
                
                elif any(keyword in column_lower for keyword in ['funding', 'finance', 'budget']):
                    funding = self.get_healthcare_info(state, 'funding_sources')
                    result_df[column] = funding[:len(df)] if funding else ['No data available'] * len(df)
                
                elif any(keyword in column_lower for keyword in ['scheme', 'program', 'initiative']):
                    schemes = self.get_healthcare_info(state, 'government_schemes')
                    result_df[column] = schemes[:len(df)] if schemes else ['No data available'] * len(df)
            
            return result_df
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None

def main():
    st.title("🏥 Healthcare AI Agent")
    st.markdown("---")
    
    # Initialize agent
    agent = HealthcareAgent()
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    selected_state = st.sidebar.selectbox(
        "Select State",
        ["Bihar", "Other States (Coming Soon)"],
        index=0
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload Excel File")
        uploaded_file = st.file_uploader(
            "Choose an Excel file with blank columns",
            type=['xlsx', 'xls'],
            help="Upload an Excel file with column headers. The agent will fill data based on column names."
        )
        
        if uploaded_file:
            st.success("File uploaded successfully!")
            
            # Preview original file
            try:
                preview_df = pd.read_excel(uploaded_file)
                st.subheader("📋 Original File Preview")
                st.dataframe(preview_df)
                
                # Process button
                if st.button("🚀 Process File", type="primary"):
                    with st.spinner("Processing healthcare data..."):
                        result_df = agent.process_excel_file(uploaded_file, selected_state.lower())
                        
                        if result_df is not None:
                            st.success("✅ File processed successfully!")
                            
                            # Display processed data
                            st.subheader("📊 Processed Healthcare Data")
                            st.dataframe(result_df)
                            
                            # Download processed file
                            output = BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                result_df.to_excel(writer, index=False, sheet_name='Healthcare_Data')
                            
                            st.download_button(
                                label="📥 Download Processed File",
                                data=output.getvalue(),
                                file_name=f"healthcare_data_{selected_state.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    with col2:
        st.header("ℹ️ Healthcare Information")
        
        if selected_state == "Bihar":
            st.subheader("🏥 Available Data Categories")
            
            # Display available information
            info_categories = {
                "🏥 Hospitals": agent.get_healthcare_info("bihar", "hospitals"),
                "🩺 Services": agent.get_healthcare_info("bihar", "services"),
                "🏢 Companies": agent.get_healthcare_info("bihar", "companies"),
                "💰 Funding Sources": agent.get_healthcare_info("bihar", "funding_sources"),
                "📋 Government Schemes": agent.get_healthcare_info("bihar", "government_schemes")
            }
            
            for category, items in info_categories.items():
                with st.expander(category):
                    for item in items:
                        st.write(f"• {item}")
    
    # Instructions
    st.markdown("---")
    st.header("📝 How to Use")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1️⃣ Prepare Excel File")
        st.write("""
        - Create Excel file with column headers
        - Use keywords like: hospital, service, company, funding, scheme
        - Leave data rows blank or with placeholder text
        """)
    
    with col2:
        st.subheader("2️⃣ Upload & Process")
        st.write("""
        - Select your state (currently Bihar)
        - Upload the Excel file
        - Click 'Process File' button
        """)
    
    with col3:
        st.subheader("3️⃣ Download Results")
        st.write("""
        - Review processed data
        - Download filled Excel file
        - Use for your healthcare analysis
        """)
    
    # Sample Excel template
    st.markdown("---")
    st.header("📋 Sample Template")
    
    sample_data = pd.DataFrame({
        'Hospital_Name': [''] * 5,
        'Services_Available': [''] * 5,
        'Healthcare_Company': [''] * 5,
        'Funding_Source': [''] * 5,
        'Government_Scheme': [''] * 5
    })
    
    st.dataframe(sample_data)
    
    # Download sample template
    sample_output = BytesIO()
    with pd.ExcelWriter(sample_output, engine='openpyxl') as writer:
        sample_data.to_excel(writer, index=False, sheet_name='Template')
    
    st.download_button(
        label="📥 Download Sample Template",
        data=sample_output.getvalue(),
        file_name="healthcare_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()
