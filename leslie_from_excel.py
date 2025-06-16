import streamlit as st
import pandas as pd
import time
from io import BytesIO

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

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='ReadyLeads')
        writer.save()
    processed_data = output.getvalue()
    return processed_data

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
    df = df.astype(str)

    df = df.rename(columns={
        "ORG_ADDR_IN_CARE_OF": "Attn Contact",
        "PRIN_OFF_NAME_ORG_L1": "Primary Org Contact",
        "PRIN_OFF_NAME_PERS": "Primary Person Contact"
    })

    df["CAUSE"] = df["ORG_NAME_L1"].apply(tag_cause)
    df["EMAIL_STATUS"] = "Not Sent"
    df["NOTES"] = ""
    df["READY_FOR_CONTACT"] = False

    leads = df[[
        "ORG_NAME_L1", "WEBSITE", "EMAIL", "PHONE", "TYPE",
        "ORG_ADDR_CITY", "ORG_ADDR_STATE",
        "Attn Contact", "Primary Org Contact", "Primary Person Contact",
        "CAUSE", "EMAIL_STATUS", "NOTES", "READY_FOR_CONTACT"
    ]]

    st.subheader("📝 Review & Tag Leads")

    editable_df = st.data_editor(leads, num_rows="dynamic", use_container_width=True)

    ready_count = editable_df[editable_df['READY_FOR_CONTACT'] == True].shape[0]
    st.info(f"✅ Leads marked as Ready for Contact: {ready_count}")

    filtered_df = editable_df[editable_df['READY_FOR_CONTACT'] == True]
    excel_file = to_excel(filtered_df)

    st.download_button(
        label="📥 Export Filtered Leads to Excel (Ready for Contact Only)",
        data=excel_file,
        file_name="filtered_leads_ready_for_contact.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
