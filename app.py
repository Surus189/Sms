import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import io

st.title("🚀 Automated Finance Pipeline")

# File uploader
uploaded_file = st.file_uploader("Upload your RAW SMS file (XML or CSV)", type=["xml", "csv"])

if uploaded_file is not None:
    # 1. Processing Logic
    if uploaded_file.name.endswith('.xml'):
        st.write("Processing XML...")
        # Add your XML parsing function here (previously in convert.py)
        # df = parse_xml_to_df(uploaded_file) 
    else:
        df = pd.read_csv(uploaded_file)
    
    # 2. Automated Cleaning Logic
    st.write("Cleaning data...")
    pattern = r'(?i)(debited|credited|spent|received|rs\.|transaction)'
    df_filtered = df[df['message'].str.contains(pattern, na=False)].copy()
    
    def extract_amount(text):
        match = re.search(r'(?:rs\.?|inr)\s?(\d+(?:,\d+)*(?:\.\d+)?)', text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(',', ''))
        return None

    df_filtered['amount'] = df_filtered['message'].apply(extract_amount)
    df_final = df_filtered.dropna(subset=['amount']).copy()
    
    # 3. Display Results
    st.success("Data Cleaned Successfully!")
    st.write(df_final.head())
    
    # 4. Download Button (The Pro Feature)
    csv_buffer = io.BytesIO()
    df_final.to_csv(csv_buffer, index=False)
    
    st.download_button(
        label="Download Cleaned CSV",
        data=csv_buffer.getvalue(),
        file_name="cleaned_financial_data.csv",
        mime="text/csv"
    )