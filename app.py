import streamlit as st
import pandas as pd
from utils import get_institutes_by_state, extract_personnel_from_website
import os

st.set_page_config(page_title="AI Agent for Healthcare Research", layout="centered")

st.title("🔬 AI Agent: Healthcare Research Institute Finder")

state = st.selectbox("📍 Select a State:", [
    "Andhra Pradesh", "Bihar", "Delhi", "Gujarat", "Karnataka", "Kerala", "Maharashtra", 
    "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal"
])

uploaded_file = st.file_uploader("📤 Upload Blank Excel Template", type=["xlsx"])

if st.button("🔍 Find Institutes and Auto-fill"):
    if uploaded_file is None:
        st.warning("Please upload the Excel template file first.")
    else:
        with st.spinner("Fetching data... Please wait."):

            # Read blank Excel file
            df_template = pd.read_excel(uploaded_file)

            # Get institute URLs
            urls = get_institutes_by_state(state)

            all_rows = []
            for url in urls:
                personnel_list = extract_personnel_from_website(url)
                for person in personnel_list:
                    row = {
                        "Location": state,
                        "Institute Name": url.split("//")[-1].split("/")[0],
                        "Institute Website": url,
                        "Department Name": "",
                        "Lab/Unit Name": "",
                        "Personnel Information": person["name"],
                        "Designation": person["designation"],
                        "Email Address": person["email"],
                        "Contact Number": "",
                        "Profile Link(s)": person["profile_link"],
                        "Primary Focus Area": "",
                        "Ongoing Projects": "",
                        "Funding Agencies": "",
                        "Recent Publications": "",
                        "Matched Advait Solution(s)": "",
                        "Match Category": ""
                    }
                    all_rows.append(row)

            df_filled = pd.DataFrame(all_rows)

            output_path = "output/filled_data.xlsx"
            os.makedirs("output", exist_ok=True)
            df_filled.to_excel(output_path, index=False)

            st.success("✅ Data gathered successfully!")
            with open(output_path, "rb") as f:
                st.download_button("📥 Download Filled Excel File", f, file_name="filled_data.xlsx")
