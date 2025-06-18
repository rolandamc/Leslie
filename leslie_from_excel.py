import streamlit as st
import pandas as pd
import time
from io import BytesIO
from drive_uploader import upload_file  # Make sure this file exists in the same directory

def tag_cause(name):
    name_lower = str(name).lower()
    if "youth" in name_lower:
        return "Youth"
    elif "health" in name_lower:
        return "Health"
    elif "education" in name_lower:
        return "Education"
    elif "housing" in name_lower:
        return "Housing"
    elif "food" in name_lower:
        return "Food Insecurity"
    elif "community" in name_lower:
        return "Community Development"
    elif "violence" in name_lower:
        return "Violence Prevention"
    elif "art" in name_lower or "culture" in name_lower:
        return "Arts & Culture"
    elif "justice" in name_lower:
        return "Social Justice"
    elif "economic" in name_lower:
        return "Economic Empowerment"
    elif "mental" in name_lower:
        return "Mental Health"
    else:
        return "Other"

st.set_page_config(page_title="Leslie - Lead Generator", layout="wide")
st.title("📊 Leslie - Nonprofit Lead Review Tool")

uploaded_file = st.file_uploader("Upload your Excel file with nonprofit data", type=["xlsx"])

if uploaded_file:
    columns_to_load = [
        "ORG_NAME_L1", "WEBSITE", "EMAIL", "PHONE", "TYPE",
        "ORG_ADDR_CITY", "ORG_ADDR_STATE", "ORG_ADDR_IN_CARE_OF",
        "PRIN_OFF_NAME_ORG_L1", "PRIN_OFF_NAME_PERS"
    ]

    df = pd.read_excel(uploaded_file, usecols=columns_to_load)
    df = df.astype(str)  # Ensures all values are strings for compatibility

    df = df.rename(columns={
        "ORG_ADDR_IN_CARE_OF": "Attn Contact",
        "PRIN_OFF_NAME_ORG_L1": "Primary Org
