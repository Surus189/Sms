import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. App UI Setup
st.set_page_config(page_title="Automated Finance Pipeline", layout="wide")
st.title("🚀 Automated Finance Pipeline")

# 2. File Uploader
uploaded_file = st.file_uploader("Upload your RAW SMS file (XML or CSV)", type=['xml', 'csv'])

if uploaded_file is not None:
    st.write("Processing data...")
    
    # 3. Processing Logic
    try:
        # XML Parsing
        if uploaded_file.name.endswith('.xml'):
            df = pd.read_xml(uploaded_file, xpath=".//sms")
            if 'body' in df.columns:
                df.rename(columns={'body': 'message'}, inplace=True)
        # CSV Parsing
        else:
            df = pd.read_csv(uploaded_file)

        # 4. Keyword Matching Logic (To create 'type' column)
        def categorize_message(msg):
            msg = str(msg).lower()
            if any(word in msg for word in ['debited', 'spent', 'paid', 'purchase']):
                return 'Debit'
            elif any(word in msg for word in ['credited', 'received', 'deposited', 'salary']):
                return 'Credit'
            else:
                return 'Other'

        # Create 'type' column
        df['type'] = df['message'].apply(categorize_message)
        
        # Show Data Preview
        st.write("### Data Preview:")
        st.dataframe(df.head())

        # 5. Visualization Logic
        df_plot = df[df['type'] != 'Other']
        
        if not df_plot.empty:
            st.write("### Expense vs Income Distribution:")
            
            # Count the types
            summary = df_plot['type'].value_counts()
            
            # Plotting
            fig, ax = plt.subplots()
            summary.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
            ax.set_title('Expense vs Income Distribution')
            ax.set_ylabel('') # Remove y-label
            
            # Display in Streamlit
            st.pyplot(fig)
        else:
            st.warning("No transactions found (Debit/Credit) to plot the chart!")

    except Exception as e:
        st.error(f"Error processing file: {e}")