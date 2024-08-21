import streamlit as st
import pandas as pd
import openpyxl
from futures_monthly_returns import plot_futures_monthly_returns
from options_monthly_returns import plot_options_monthly_returns
from charges import extract_charges  # Import the extract_charges function
from total_returns import summarize_total_returns  # Import the summarize_total_returns function

def extract_month(symbol):
    month_mapping = {
        'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
        'APR': 'April', 'MAY': 'May', 'JUN': 'June',
        'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
        'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    }
    month_code = symbol[7:10]
    return month_mapping.get(month_code.upper(), 'Unknown')

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload a single Excel file to view and analyze percentage returns for futures, options, and combined totals.")

    # File uploader for the data
    uploaded_file = st.file_uploader("Choose an Excel file for the data", type=["xlsx", "xls"])

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

            # Separate futures and options data
            futures_df = df[df['Symbol'].str.endswith('FUT')]
            options_df = df[df['Symbol'].str.endswith(('CE', 'PE'))]
            
            # Display the dataframes
            st.write("Futures Data:")
            st.write(futures_df)
            st.write("Options Data:")
            st.write(options_df)

            # Plot Futures Monthly Returns
            plot_futures_monthly_returns(futures_df)
            
            # Plot Options Monthly Returns
            plot_options_monthly_returns(options_df)
            
            # Summarize total returns
            summarize_total_returns(futures_df, options_df)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
