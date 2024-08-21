import pandas as pd
import streamlit as st

def extract_year(symbol):
    return '20' + symbol[5:7]  # Extract the year from the Symbol (e.g., '23' -> '2023')

def extract_month(symbol):
    month_mapping = {
        'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
        'APR': 'April', 'MAY': 'May', 'JUN': 'June',
        'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
        'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    }
    month_code = symbol[7:10]
    return month_mapping.get(month_code.upper(), 'Unknown')

def calculate_returns_by_year(df, year_type='Calendar'):
    if year_type == 'Calendar':
        df['Year'] = df['Symbol'].apply(extract_year)
        df['Month'] = df['Symbol'].apply(extract_month)
    elif year_type == 'Financial':
        df['Year'] = df['Symbol'].apply(extract_year)
        df['Month'] = df['Symbol'].apply(extract_month)
        df['Year'] = df.apply(lambda x: str(int(x['Year']) - 1) if x['Month'] in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] else x['Year'], axis=1)

    # Aggregate returns by Year and collect months used
    yearly_data = df.groupby('Year').agg({
        'Realized P&L Pct.': 'mean',
        'Month': lambda x: ', '.join(sorted(x.unique()))
    }).reset_index()

    yearly_data.columns = ['Year', f'{year_type} Yearly Return (%)', f'{year_type} Months Used']
    
    return yearly_data

def summarize_returns(df):
    st.title("Yearly Returns Summary")

    # Calculate returns by Calendar Year
    calendar_year_returns = calculate_returns_by_year(df, 'Calendar')
    
    # Calculate returns by Financial Year
    financial_year_returns = calculate_returns_by_year(df, 'Financial')
    
    # Merge the results into one table
    summary_table = pd.merge(calendar_year_returns, financial_year_returns, on='Year', how='outer')

    # Reorder columns to have a clear structure
    summary_table = summary_table[['Year', 'Calendar Yearly Return (%)', 'Calendar Months Used', 'Financial Yearly Return (%)', 'Financial Months Used']]

    # Display the table
    st.write(summary_table)

def main():
    st.title("Upload Excel File to Summarize Returns by Year")
    
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

            # Summarize returns by Calendar and Financial Years
            summarize_returns(df)
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
