import pandas as pd
import json
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    import gspread
    client = gspread.authorize(creds)
    sheet = client.open("Advait_Insights_Backend").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)
