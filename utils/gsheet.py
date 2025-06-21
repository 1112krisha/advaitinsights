import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_sheet():
    # Setup credentials
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # Replace with your sheet name
    sheet = client.open("Advait_Insights_Backend").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)
