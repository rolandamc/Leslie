import streamlit as st
import pandas as pd
import time
from io import BytesIO
from drive_uploader import upload_to_drive

def tag_cause(name):
    name_str = str(name).lower()
    if "youth" in name_str:
        return "Youth"
    elif "health" in name_str:
        return "Health"
    elif "education" in name_str:
        return "Education"
    elif "housing" in name_str:
        return "Housing"
    elif "food" in name_str:
        return "Food Insecurity"
    elif "community" in name_str:
        return "Community Development"
    elif "violence" in name_str:
        return "Violence Prevention"
    elif "art" in name_str or "culture" in name_str:
        return "Arts & Culture"
    elif "justice" in name_str:
        return "Social Justice"
    elif "economic" in name_str:
        return "Economic Empowerment"
    elif "mental" in name_str:
        return "Mental Health"
    else:
        return "Other"

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Leads')
    output.seek(0)
    return output.read()

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
    df = df.applymap(lambda x: str(x) if not pd.isnull(x) else "")

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

    # Export Excel Download
    excel_data = convert_df_to_excel(editable_df[editable_df['READY_FOR_CONTACT'] == True])
    st.download_button(
        label="📥 Export Filtered Leads (Excel)",
        data=excel_data,
        file_name="filtered_leads_ready_for_contact.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Upload to Google Drive
    if st.button("📤 Upload to Google Drive (Ready for Contact Only)"):
        file_id = upload_to_drive(
            file_bytes=excel_data,
            file_name="ReadyLeads.xlsx",
            folder_id="1iFOkoeS02hq4QhzmWTvW1sEEh4QwDZPt"
        )

        if file_id:
            st.success("✅ File uploaded successfully to Google Drive!")
        else:
            st.error("❌ Upload failed. Please check authentication.")

    print("⏳ Waiting 60 seconds before next request to respect API limits...")
    time.sleep(60)
