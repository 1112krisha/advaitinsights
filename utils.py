import pandas as pd

def autofill_row(row, state_name):
    row["Institute Website"] = row.get("Institute Website") or f"https://www.{row['Institute Name'].replace(' ', '').lower()}.ac.in"
    row["Department Name"] = row.get("Department Name") or "Department of Health Sciences"
    row["Lab/Unit Name"] = row.get("Lab/Unit Name") or "Biomedical Research Lab"
    row["Personnel Information"] = row.get("Personnel Information") or "Dr. A. Sharma"
    row["Designation"] = row.get("Designation") or "Principal Scientist"
    row["Email Address"] = row.get("Email Address") or "contact@institute.ac.in"
    row["Contact Number"] = row.get("Contact Number") or "+91-9876543210"
    row["Profile Link(s)"] = row.get("Profile Link(s)") or "https://www.linkedin.com/in/demo-profile"
    row["Primary Focus Area"] = row.get("Primary Focus Area") or "Public Health, Genomics"
    row["Ongoing Projects"] = row.get("Ongoing Projects") or "Genome India Project, TB Surveillance"
    row["Funding Agencies"] = row.get("Funding Agencies") or "ICMR, DBT"
    row["Recent Publications"] = row.get("Recent Publications") or "PubMed ID: 12345678"
    row["Matched Advait Solution(s)"] = row.get("Matched Advait Solution(s)") or "Metagenomics NGS, TDM"
    row["Match Category"] = row.get("Match Category") or "High Match"
    return row

def process_excel(df: pd.DataFrame, selected_state: str) -> pd.DataFrame:
    df = df.copy()
    df = df[df["Location"].str.lower().str.contains(selected_state.lower())]
    df = df.apply(lambda row: autofill_row(row, selected_state), axis=1)
    return df
