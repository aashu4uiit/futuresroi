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

def extract_year(symbol):
    return '20' + symbol[5:7]  # Extract the year from the Symbol (e.g., '23' -> '2023')

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload Excel files to view and analyze percentage returns for futures, options, and combined totals.")

    # File uploader for the futures data
    futures_file = st.file_uploader("Choose an Excel file for futures data", type=["xlsx", "xls"])
    
    # File uploader for the options data
    options_file = st.file_uploader("Choose an Excel file for options data", type=["xlsx", "xls"])

    if futures_file is not None and options_file is not None:
        try:
            # Extract and display charges using the futures file (assuming charges are in the futures file)
            charges_value = extract_charges(futures_file)
            if charges_value is not None:
                charges_table = pd.DataFrame({'Charges': [charges_value]})
                st.write("Charges Table:")
                st.write(charges_table)

            # Read the uploaded Excel files for futures and options
            futures_df = pd.read_excel(futures_file, sheet_name='F&O', engine='openpyxl', skiprows=36, header=0)
            options_df = pd.read_excel(options_file, sheet_name='F&O', engine='openpyxl', skiprows=36, header=0)
            
            # Rename columns using the first row as headers
            futures_df.columns = futures_df.iloc[0]  # Set the first row as the header
            futures_df = futures_df[1:]  # Remove the first row from the dataframe
            futures_df.columns = futures_df.columns.str.strip()
            futures_df.columns.name = None
            
            options_df.columns = options_df.iloc[0]  # Set the first row as the header
            options_df = options_df[1:]  # Remove the first row from the dataframe
            options_df.columns = options_df.columns.str.strip()
            options_df.columns.name = None
            
            # Add the "Month" column based on the "Symbol" column for both futures and options
            futures_df['Month'] = futures_df['Symbol'].apply(extract_month)
            options_df['Month'] = options_df['Symbol'].apply(extract_month)
            
            # Reorder columns to place "Month" before "Symbol" for both futures and options
            futures_columns = ['Month'] + [col for col in futures_df.columns if col != 'Month']
            futures_df = futures_df[futures_columns]
            
            options_columns = ['Month'] + [col for col in options_df.columns if col != 'Month']
            options_df = options_df[options_columns]
            
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
            st.error(f"An error occurred while processing the files: {e}")

if __name__ == "__main__":
    main()
