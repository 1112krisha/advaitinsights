import streamlit as st
import pandas as pd
from utils import get_institutes_by_state, extract_personnel_from_website
from io import BytesIO

# List of Indian states
states = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
    "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana",
    "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Mumbai", "Nagaland", "Odisha",
    "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
    "Uttarakhand", "West Bengal"
]

st.set_page_config(page_title="Advait Healthcare Excel Auto-Filler", layout="wide")
st.title("🔬 Advait Healthcare Excel Auto-Filler")

uploaded_file = st.file_uploader("📤 Upload your blank Excel file", type=["xlsx"])
selected_state = st.selectbox("📍 Select a State to Fetch Data From", states)

if uploaded_file and selected_state:
    df = pd.read_excel(uploaded_file)
    st.success(f"✅ File uploaded successfully. State selected: {selected_state}")

    if st.button("🔍 Start Auto-Fill"):
        st.info("⏳ Fetching institute and personnel data... please wait.")
        institute_websites = get_institutes_by_state(selected_state)

        if not institute_websites:
            st.error("❌ No institutes found. Try a different state.")
        else:
            filled_data = []

            for url in institute_websites:
                institute_name = url.split("//")[-1].split("/")[0]
                personnel_list = extract_personnel_from_website(url)

                if not personnel_list:
                    filled_data.append({
                        "Location": selected_state,
                        "Institute Name": institute_name,
                        "Institute Website": url,
                        "Department Name": "",
                        "Lab/Unit Name": "",
                        "Personnel Information": "",
                        "Designation": "",
                        "Email Address": "",
                        "Contact Number": "",
                        "Profile Link(s)": "",
                        "Primary Focus Area": "",
                        "Ongoing Projects": "",
                        "Funding Agencies": "",
                        "Recent Publications": "",
                        "Matched Advait Solution(s)": "",
                        "Match Category": ""
                    })
                else:
                    for person in personnel_list:
                        filled_data.append({
                            "Location": selected_state,
                            "Institute Name": institute_name,
                            "Institute Website": url,
                            "Department Name": "",
                            "Lab/Unit Name": "",
                            "Personnel Information": person['name'],
                            "Designation": person['designation'],
                            "Email Address": person['email'],
                            "Contact Number": "",
                            "Profile Link(s)": person['profile_link'],
                            "Primary Focus Area": "",
                            "Ongoing Projects": "",
                            "Funding Agencies": "",
                            "Recent Publications": "",
                            "Matched Advait Solution(s)": "",
                            "Match Category": ""
                        })

            filled_df = pd.DataFrame(filled_data)
            st.success("✅ Data auto-filled successfully.")
            st.dataframe(filled_df)

            # Download
            output = BytesIO()
            filled_df.to_excel(output, index=False, engine='openpyxl')
            st.download_button(
                label="📥 Download Filled Excel",
                data=output.getvalue(),
                file_name="filled_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
