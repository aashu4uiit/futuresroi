import streamlit as st
import pandas as pd

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl')
    
    # Display the dataframe
    st.write(df)

    # Additional processing can go here...
