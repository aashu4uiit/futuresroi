import streamlit as st
import pandas as pd
import openpyxl
from futures_monthly_returns import plot_futures_monthly_returns
from options_monthly_returns import plot_options_monthly_returns

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

def calculate_returns_by_year(df, year_type='Calendar'):
    if year_type == 'Calendar':
        df['Year'] = df['Symbol'].apply(extract_year)
    elif year_type == 'Financial':
        df['Year'] = df['Symbol'].apply(extract_year)
        df['Month'] = df['Symbol'].str[7:10]
        df['Year'] = df.apply(lambda x: str(int(x['Year']) - 1) if x['Month'] in ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'] else x['Year'], axis=1)

    yearly_returns = df.groupby('Year')['Realized P&L Pct.'].mean().reset_index()
    yearly_returns.columns = ['Year', f'{year_type} Yearly Return (%)']
    
    return yearly_returns

def summarize_returns(df):
    st.title("Yearly Returns Summary")

    # Calculate returns by Calendar Year
    calendar_year_returns = calculate_returns_by_year(df, 'Calendar')
    
    # Calculate returns by Financial Year
    financial_year_returns = calculate_returns_by_year(df, 'Financial')
    
    # Merge the results into one table
    summary_table = pd.merge(calendar_year_returns, financial_year_returns, on='Year', how='outer')

    # Display the summary table
    st.write(summary_table)

def extract_and_display_charges(df):
    st.title("Charges Summary")
    
    try:
        # Ensure there is a second column to check for "Charges"
        if df.shape[1] > 1:
            # Identify the row where "Charges" is located
            charges_row = df[df.iloc[:, 1] == 'Charges']  # Checking the second column

            # Extract the value associated with "Charges"
            if not charges_row.empty:
                charges_value = charges_row.iloc[0, 2]  # Assuming the value is in the third column
                charges_table = pd.DataFrame({'Charges': [charges_value]})
                st.write("Charges Table:")
                st.write(charges_table)
            else:
                st.error("Charges row not found.")
        else:
            st.error("The DataFrame does not contain enough columns to check for 'Charges'.")
    
    except Exception as e:
        st.error(f"An error occurred while processing the charges: {e}")

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload an Excel file to view and analyze percentage returns.")

    # File uploader for the main data
    uploaded_file = st.file_uploader("Choose an Excel file for main data", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
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
            summarize_returns(df)
            
            # Extract and display charges separately
            extract_and_display_charges(df)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
