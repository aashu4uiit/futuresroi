import streamlit as st
import pandas as pd
import openpyxl

# Function to extract the month from the 'Symbol' column
def extract_month(symbol):
    month_mapping = {
        'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
        'APR': 'April', 'MAY': 'May', 'JUN': 'June',
        'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
        'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    }
    month_code = symbol[7:10]
    return month_mapping.get(month_code.upper(), 'Unknown')

# Function to extract the year from the 'Symbol' column
def extract_year(symbol):
    return '20' + symbol[5:7]  # Extract the year from the Symbol (e.g., '23' -> '2023')

# Function to calculate returns by year
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

# Function to summarize returns
def summarize_returns(df):
    st.title("Yearly Returns Summary")

    # Calculate returns by Calendar Year
    calendar_year_returns = calculate_returns_by_year(df, 'Calendar')
    
    # Calculate returns by Financial Year
    financial_year_returns = calculate_returns_by_year(df, 'Financial')
    
    # Merge the results into one table
    summary_table = pd.merge(calendar_year_returns, financial_year_returns, on='Year', how='outer')

    # Adding Charges to Table
    try:
        # Identify the row where "Charges" is located
        charges_row = df[df[1] == 'Charges']
        
        # Extract the value associated with "Charges"
        if not charges_row.empty:
            charges_value = charges_row.iloc[0, 2]  # Assuming the value is in the third column
            charges_row_data = pd.DataFrame({
                'Year': ['Charges'], 
                f'{calendar_year_returns.columns[1]}': [charges_value], 
                f'{financial_year_returns.columns[1]}': [charges_value]
            })
            
            # Append the charges row to the summary table
            summary_table = summary_table.append(charges_row_data, ignore_index=True)
        else:
            st.error("Charges row not found.")
    
    except Exception as e:
        st.error(f"An error occurred while processing the charges: {e}")
    
    # Display the table
    st.write(summary_table)

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload an Excel file to view and analyze percentage returns.")

    # File uploader for the main data
    uploaded_file = st.file_uploader("Choose an Excel file for main data", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the uploaded Excel file, skip the first 13 rows
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=13, header=None)
            
            # Inspect the first few rows and column headers
            st.write("Data preview:")
            st.write(df.head())  # Display the first few rows to inspect the structure
            
            # Identify the actual headers and data
            if 'Symbol' not in df.columns:
                st.error("The 'Symbol' column could not be found. Please check the data structure.")
            else:
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
                
                # Summarize returns by Calendar and Financial Years, including charges
                summarize_returns(df)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
