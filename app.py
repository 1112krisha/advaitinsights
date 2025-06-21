import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("Test Connection to Google Sheet")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

try:
    sheet = client.open("Advait_Insights_Backend").worksheet("Sheet1")
    rows = sheet.get_all_values()
    st.success("✅ Successfully connected!")
    st.write(rows)
except Exception as e:
    st.error("❌ Failed to connect:")
    st.exception(e)
