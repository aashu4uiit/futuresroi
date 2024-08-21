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

def format_month_year(month, year):
    month_abbr = month[:3].upper()
    year_abbr = year[-2:]
    return f"{month_abbr}-{year_abbr}"

def calculate_financial_year_returns(df):
    df['Month'] = df['Symbol'].apply(extract_month)
    df['Year'] = df['Symbol'].apply(extract_year)
    
    # Adjust the year for the financial year grouping
    df['FY_Year'] = df.apply(lambda x: str(int(x['Year']) - 1) if x['Month'] in [
        'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] else x['Year'], axis=1)

    # Format Month-Year
    df['Month-Year'] = df.apply(lambda x: format_month_year(x['Month'], x['Year']), axis=1)

    # Aggregate returns by FY_Year and collect months used
    financial_year_data = df.groupby('FY_Year').agg({
        'Realized P&L Pct.': 'mean',
        'Month-Year': lambda x: ', '.join(sorted(x.unique()))
    }).reset_index()

    financial_year_data.columns = ['Financial Year', 'Financial Yearly Return (%)', 'Financial Year Months Used']
    
    return financial_year_data

def summarize_financial_year_returns(df):
    st.title("Financial Year Returns Summary")

    # Calculate returns by Financial Year
    financial_year_returns = calculate_financial_year_returns(df)
    
    # Display the table
    st.write(financial_year_returns)

def main():
    st.title("Upload Excel File to Summarize Returns by Financial Year")
    
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

            # Summarize returns by Financial Year
            summarize_financial_year_returns(df)
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
