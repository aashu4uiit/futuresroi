import streamlit as st
import pandas as pd
import openpyxl
import yfinance as yf
from stage2 import stage2_analysis  # Import the stage2 functionality
from futures_monthly_returns import plot_futures_monthly_returns
from options_monthly_returns import plot_options_monthly_returns
from charges import extract_charges  # Import the extract_charges function
from total_returns import calculate_total_returns  # Import the calculate_total_returns function

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Stage 2 Stocks", "F&O Returns"])

if page == "Home":
    # Your existing home page code here
    st.title("Welcome to Portfolio Check")
    st.write("Use this tool to analyze your portfolio.")

elif page == "Stage 2 Stocks":
    st.title("Stage 2 Stocks Analysis")
    st.write("Analyze your portfolio for stocks meeting Stage 2 criteria.")

    # File uploader for Stage 2 analysis
    uploaded_file = st.file_uploader("Upload your portfolio file", type=[ "xlsx"])
    if uploaded_file is not None:
        stage2_analysis(uploaded_file)

else:
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
        st.title("Futures & Options Returns Calculator")
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
                else:
                    st.error("Charges value could not be found or is invalid.")
                    return

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
                
                # Calculate and summarize total returns
                total_returns_df = calculate_total_returns(df, charges_value)
                st.write("Total Returns Summary:")
                st.write(total_returns_df)

            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")

    if __name__ == "__main__":
        main()
