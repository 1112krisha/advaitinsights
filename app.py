import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import random

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
                    "Darbhanga Medical College", "Katihar Medical College", "Muzaffarpur Medical College",
                    "Patna Medical College Hospital", "Indira Gandhi Institute of Medical Sciences",
                    "Sri Krishna Medical College", "Government Medical College Bettiah"
                ],
                "services": [
                    "Primary Healthcare", "Secondary Healthcare", "Tertiary Healthcare",
                    "Emergency Services", "Diagnostic Services", "Pharmacy Services",
                    "Telemedicine", "Maternal Health", "Child Health", "Mental Health",
                    "Cardiology", "Oncology", "Orthopedics", "Neurology", "Pediatrics"
                ],
                "companies": [
                    "Apollo Hospitals", "Fortis Healthcare", "Max Healthcare",
                    "Medanta", "Narayana Health", "Manipal Hospitals",
                    "Care Hospitals", "Asian Heart Institute", "Kokilaben Hospital",
                    "Jaslok Hospital", "Lilavati Hospital", "P.D. Hinduja Hospital"
                ],
                "funding_sources": [
                    "National Health Mission (NHM)", "Pradhan Mantri Jan Arogya Yojana",
                    "Bihar State Health Society", "World Bank Healthcare Projects",
                    "Asian Development Bank", "Government of Bihar Health Budget",
                    "Private Healthcare Investment", "CSR Healthcare Funding",
                    "UNICEF Health Programs", "WHO Health Initiatives"
                ],
                "government_schemes": [
                    "Ayushman Bharat", "Janani Suraksha Yojana", "Rashtriya Bal Swasthya Karyakram",
                    "National Programme for Healthcare of Elderly", "Mission Indradhanush",
                    "Pradhan Mantri Matru Vandana Yojana", "Rashtriya Swasthya Bima Yojana",
                    "National Rural Health Mission", "Integrated Child Development Services"
                ]
            }
        }
    
    def get_healthcare_info(self, state, category):
        """Get healthcare information for specific state and category"""
        state_lower = state.lower()
        if state_lower in self.healthcare_data:
            return self.healthcare_data[state_lower].get(category, [])
        return []
    
    def fill_column_data(self, df, column_name, data_list, num_rows):
        """Fill column with data from list"""
        if not data_list:
            return ["No data available"] * num_rows
        
        # If we have more rows than data, repeat the data
        filled_data = []
        for i in range(num_rows):
            filled_data.append(data_list[i % len(data_list)])
        
        return filled_data
    
    def process_excel_file(self, uploaded_file, state):
        """Process uploaded Excel file and fill healthcare data"""
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Create a copy to modify
            result_df = df.copy()
            num_rows = len(df)
            
            # Process each column
            for column in df.columns:
                column_lower = column.lower()
                
                if any(keyword in column_lower for keyword in ['hospital', 'medical', 'health center', 'clinic']):
                    hospitals = self.get_healthcare_info(state, 'hospitals')
                    result_df[column] = self.fill_column_data(df, column, hospitals, num_rows)
                
                elif any(keyword in column_lower for keyword in ['service', 'treatment', 'care', 'specialty']):
                    services = self.get_healthcare_info(state, 'services')
                    result_df[column] = self.fill_column_data(df, column, services, num_rows)
                
                elif any(keyword in column_lower for keyword in ['company', 'provider', 'organization']):
                    companies = self.get_healthcare_info(state, 'companies')
                    result_df[column] = self.fill_column_data(df, column, companies, num_rows)
                
                elif any(keyword in column_lower for keyword in ['funding', 'finance', 'budget', 'investment']):
                    funding = self.get_healthcare_info(state, 'funding_sources')
                    result_df[column] = self.fill_column_data(df, column, funding, num_rows)
                
                elif any(keyword in column_lower for keyword in ['scheme', 'program', 'initiative', 'policy']):
                    schemes = self.get_healthcare_info(state, 'government_schemes')
                    result_df[column] = self.fill_column_data(df, column, schemes, num_rows)
            
            return result_df
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None

def create_sample_template():
    """Create sample Excel template"""
    sample_data = {
        'Hospital_Name': [''] * 5,
        'Services_Available': [''] * 5,
        'Healthcare_Company': [''] * 5,
        'Funding_Source': [''] * 5,
        'Government_Scheme': [''] * 5,
        'Location': [''] * 5,
        'Contact_Details': [''] * 5
    }
    return pd.DataFrame(sample_data)

def main():
    st.title("🏥 Healthcare AI Agent")
    st.markdown("Upload Excel files and get healthcare data filled automatically!")
    st.markdown("---")
    
    # Initialize agent
    agent = HealthcareAgent()
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    selected_state = st.sidebar.selectbox(
        "Select State",
        ["Bihar"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("📋 Instructions")
    st.sidebar.markdown("""
    1. Upload Excel file with column headers
    2. Use keywords like: hospital, service, company, funding, scheme
    3. Click 'Process File'
    4. Download filled data
    """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 File Upload & Processing")
        
        uploaded_file = st.file_uploader(
            "Choose Excel file (.xlsx or .xls)",
            type=['xlsx', 'xls'],
            help="Upload Excel file with blank columns that need healthcare data"
        )
        
        if uploaded_file is not None:
            try:
                # Show original file
                original_df = pd.read_excel(uploaded_file)
                st.subheader("📋 Original File Preview")
                st.dataframe(original_df, use_container_width=True)
                
                st.info(f"File has {len(original_df)} rows and {len(original_df.columns)} columns")
                
                # Process button
                if st.button("🚀 Process File", type="primary", use_container_width=True):
                    with st.spinner("Processing healthcare data..."):
                        result_df = agent.process_excel_file(uploaded_file, selected_state.lower())
                        
                        if result_df is not None:
                            st.success("✅ File processed successfully!")
                            
                            # Show processed data
                            st.subheader("📊 Processed Healthcare Data")
                            st.dataframe(result_df, use_container_width=True)
                            
                            # Create download file
                            output = BytesIO()
                            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                result_df.to_excel(writer, index=False, sheet_name='Healthcare_Data')
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Processed File",
                                data=output.getvalue(),
                                file_name=f"healthcare_data_{selected_state.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    with col2:
        st.header("ℹ️ Available Data")
        
        if selected_state == "Bihar":
            # Show data categories
            categories = {
                "🏥 Hospitals": "hospitals",
                "🩺 Services": "services", 
                "🏢 Companies": "companies",
                "💰 Funding": "funding_sources",
                "📋 Schemes": "government_schemes"
            }
            
            for title, key in categories.items():
                with st.expander(title):
                    items = agent.get_healthcare_info("bihar", key)
                    for item in items[:5]:  # Show first 5 items
                        st.write(f"• {item}")
                    if len(items) > 5:
                        st.write(f"... and {len(items) - 5} more")
    
    # Sample template section
    st.markdown("---")
    st.header("📋 Sample Template")
    st.write("Download this template to see how to structure your Excel file:")
    
    sample_df = create_sample_template()
    st.dataframe(sample_df, use_container_width=True)
    
    # Download sample template
    sample_output = BytesIO()
    with pd.ExcelWriter(sample_output, engine='openpyxl') as writer:
        sample_df.to_excel(writer, index=False, sheet_name='Template')
    
    st.download_button(
        label="📥 Download Sample Template",
        data=sample_output.getvalue(),
        file_name="healthcare_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Healthcare AI Agent | Made for Bihar Healthcare Data Processing</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
