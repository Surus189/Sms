import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# App Title
st.title("Automated Finance Pipeline")

# File Uploader
uploaded_file = st.file_uploader("Upload your RAW SMS file (XML or CSV)", type=['xml', 'csv'])

if uploaded_file is not None:
    st.write("Processing data...")
    
    # 1. XML Parsing Logic
    if uploaded_file.name.endswith('.xml'):
        # XML to DataFrame logic
        try:
            df = pd.read_xml(uploaded_file, xpath=".//sms")
            if 'body' in df.columns:
                df.rename(columns={'body': 'message'}, inplace=True)
        except Exception as e:
            st.error(f"Error reading XML: {e}")
            st.stop()
            
    # 2. CSV Parsing Logic
    else:
        df = pd.read_csv(uploaded_file)

    # Show Data Preview
    st.write("Preview of your data:")
    st.write(df.head())

    # 3. Visualization Logic (Pie Chart)
    # Assuming 'type' column exists to distinguish Debit/Credit
    if 'type' in df.columns:
        st.write("Expense vs Income Distribution:")
        
        # Count the types
        summary = df['type'].value_counts()
        
        # Plotting
        fig, ax = plt.subplots()
        summary.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
        ax.set_title('Expense vs Income Distribution')
        ax.set_ylabel('') # Remove y-label
        
        # Display in Streamlit
        st.pyplot(fig)
    else:
        st.warning("Could not find 'type' column to plot the chart. Check your data!")