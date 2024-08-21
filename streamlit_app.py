import streamlit as st
import pandas as pd
import openpyxl

def calculate_roi(beginning_value, ending_value):
    return ((ending_value - beginning_value) / beginning_value) * 100

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload an Excel file or manually input values to calculate ROI.")

    # File uploader section
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the uploaded Excel file, skip the first 36 rows, and use row 37 as the header
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=36)
            
            # Display the dataframe
            st.write(df)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

    st.write("---")  # Separator line

    # Manual ROI calculation section
    st.header("Manual ROI Calculation")
    beginning_value = st.number_input("Enter the Beginning Value (Buy Value):", min_value=0.0, format="%.2f")
    ending_value = st.number_input("Enter the Ending Value (Sell Value):", min_value=0.0, 
