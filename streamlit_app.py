import streamlit as st
import pandas as pd
import openpyxl
from futures_monthly_returns import plot_futures_monthly_returns
from options_monthly_returns import plot_options_monthly_returns
from charges import extract_charges  # Import the extract_charges function
from yearly_returns import summarize_financial_year_returns  # Import the summarize_returns function

def extract_month(symbol):
    month_mapping = {
        'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
        'APR': 'April', 'MAY': 'May', 'JUN': 'June',
        'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
        'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    }
    month_code = symbol[7:10]
    return month_mapping.get(month_code.upper(), 'Unknown')

def extract_year(symbol):
    return '20' + symbol[5:7]  # Extract the year from the Symbol (e.g., '23' -> '2023')

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload an Excel file to view and analyze percentage returns.")

    # File uploader for the main data
    uploaded_file = st.file_uploader("Choose an Excel file for main data", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Extract and display charges using the uploaded file
            charges_value = extract_charges(uploaded_file)
            if charges_value is not None:
                charges_table = pd.DataFrame({'Charges': [charges_value]})
                st.write("Charges Table:")
                st.write(charges_table)

            # Read the uploaded Excel file, skip the first 36 rows, and correctly interpret the header
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=36, header=0)
            
            # Rename columns using the first row as headers
            df.columns = df.iloc[0]  # Set the first row as the header
            df = df[1:]  # Remove the first row from the dataframe
            
            # Rename the columns to standardize naming
            df.columns = df.columns.str.strip()
            df.columns.name = None
            
            # Add the "Month" column based on the "Symbol" column
            df['Month'] = df['Symbol'].apply(extract_month)
            
            # Reorder columns to place "Month" before "Symbol"
            columns = ['Month'] + [col for col in df.columns if col != 'Month']
            df = df[columns]
            
            # Display the dataframe
            st.write(df)

            # Plot Futures Monthly Returns
            plot_futures_monthly_returns(df)
            
            # Plot Options Monthly Returns
            plot_options_monthly_returns(df)
            
            # Summarize returns by Calendar and Financial Years
            summarize_financial_year_returns(df)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
