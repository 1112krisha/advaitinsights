import streamlit as st
import pandas as pd
from utils import get_institutes_by_state, extract_personnel_and_info

# List of states as per your list
STATES = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
    "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka",
    "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Mumbai", "Nagaland", "Odisha", "Puducherry", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

COLUMNS = [
    "Location", "Institute Name", "Institute Website", "Department Name", "Lab/Unit Name",
    "Personnel Information", "Designation", "Email Address", "Contact Number", "Profile Link(s)",
    "Primary Focus Area", "Ongoing Projects", "Funding Agencies", "Recent Publications",
    "Matched Advait Solution(s)", "Match Category"
]

st.title("Healthcare Research Institutes Data Extractor")

# Step 1: Upload blank Excel file with columns or just use default
uploaded_file = st.file_uploader("Upload your blank Excel file with required columns (optional)", type=["xlsx"])

if uploaded_file:
    try:
        df_template = pd.read_excel(uploaded_file)
        st.success("Template loaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        df_template = pd.DataFrame(columns=COLUMNS)
else:
    df_template = pd.DataFrame(columns=COLUMNS)

# Step 2: Select State dropdown
state = st.selectbox("Select State", STATES)

if st.button("Fetch and Fill Data"):
    with st.spinner("Fetching institutes and extracting data..."):
        urls = get_institutes_by_state(state)

        all_rows = []
        for url in urls:
            personnel_list = extract_personnel_and_info(url)
            for person in personnel_list:
                row = {
                    "Location": state,
                    "Institute Name": url.split("//")[-1].split("/")[0],
                    "Institute Website": url,
                    "Department Name": "",
                    "Lab/Unit Name": "",
                    "Personnel Information": person.get("name", ""),
                    "Designation": person.get("designation", ""),
                    "Email Address": person.get("email", ""),
                    "Contact Number": "",
                    "Profile Link(s)": person.get("profile_link", ""),
                    "Primary Focus Area": ", ".join(person.get("services", [])),
                    "Ongoing Projects": "",
                    "Funding Agencies": ", ".join(person.get("funding", [])),
                    "Recent Publications": "",
                    "Matched Advait Solution(s)": ", ".join(person.get("services", [])),
                    "Match Category": "Verified"
                }
                all_rows.append(row)

        if all_rows:
            df_filled = pd.DataFrame(all_rows)
            # Merge with template columns to keep order and missing columns
            df_final = pd.concat([df_template, df_filled], ignore_index=True)[COLUMNS]

            st.success(f"Data fetched for {len(all_rows)} entries.")
            st.dataframe(df_final)

            # Provide download button
            excel_bytes = df_final.to_excel(index=False, engine='openpyxl')
            import io
            buffer = io.BytesIO()
            df_final.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)

            st.download_button(
                label="Download Filled Excel",
                data=buffer,
                file_name=f"{state}_research_institutes_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No verified data found for the selected state.")
