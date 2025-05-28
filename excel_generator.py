import pandas as pd
import os
import uuid
from utils import generate_data_for_state


def generate_excel(state_name):
    # Generate data for the selected state
    data = generate_data_for_state(state_name)

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Define the file path
    filename = f"KOL_Data_{state_name.replace(' ', '_')}_{uuid.uuid4().hex[:6]}.xlsx"
    filepath = os.path.join("/tmp", filename)

    # Save to Excel
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Sheet2", index=False)

    return filepath, df
