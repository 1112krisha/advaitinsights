import pandas as pd
import json
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_data_from_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["GOOGLE_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Make sure both name and tab are correct
    sheet = client.open("Advait_Insights_Backend").worksheet("Sheet1")

    data = sheet.get_all_records()
    return pd.DataFrame(data)
