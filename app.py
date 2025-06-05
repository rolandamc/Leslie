import streamlit as st
import pandas as pd

st.set_page_config(page_title="Leslie - Nonprofit Lead Generator", layout="centered")

# Title
st.title("📊 Meet Leslie: Your Nonprofit Lead Finder")
st.markdown("Leslie is your AI-powered assistant that finds nonprofit websites, emails, and phone numbers so you don’t have to.")

# Input fields
with st.form("search_form"):
    st.subheader("🔍 What are you looking for?")
    location = st.text_input("Enter a city or state", placeholder="e.g. Tampa, Florida")
    cause = st.text_input("What type of nonprofits?", placeholder="e.g. youth development, education, health")
    email = st.text_input("Enter your email to receive results")
    submitted = st.form_submit_button("Search with Leslie")

# Simulate Results
if submitted:
    with st.spinner("Leslie is searching the web..."):
        # Simulated results
        data = {
            "Nonprofit Name": ["Youth Empowerment Tampa", "Health for All Inc.", "Education Forward Foundation"],
            "Website": ["https://youthtampa.org", "https://healthforall.org", "https://educationforward.org"],
            "Email": ["info@youthtampa.org", "contact@healthforall.org", "hello@educationforward.org"],
            "Phone": ["(813) 555-1234", "(813) 555-5678", "(813) 555-9012"]
        }
        df = pd.DataFrame(data)
        
        st.success("✅ Done! Here are a few nonprofits Leslie found:")
        st.dataframe(df)

        st.markdown("📩 Leslie will also email this list to you soon.")

        # Option to download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Your List", csv, "nonprofit_leads.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("💼 Powered by **Rolanda S. McDuffie, CPA** | [rsmcduffiecpa.com](https://rsmcduffiecpa.com)")
