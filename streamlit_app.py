import streamlit as st
import pandas as pd
import openpyxl

def calculate_roi(beginning_value, ending_value):
    return ((ending_value - beginning_value) / beginning_value) * 100

def extract_month(symbol):
    # Mapping from the three-character month code to the full month name
    month_mapping = {
        'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
        'APR': 'April', 'MAY': 'May', 'JUN': 'June',
        'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
        'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    }
    # Extract the month code from characters 8, 9, 10 of the symbol
    month_code = symbol[7:10]
    return month_mapping.get(month_code.upper(), 'Unknown')

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload an Excel file or manually input values to calculate ROI.")

    # File uploader section
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the uploaded Excel file, skip the first 36 rows, and use row 37 as the header
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=36)
            
            # Debugging: Display the column names to ensure 'Symbol' is present
            st.write("Columns in the uploaded file:", df.columns.tolist())
            
            if 'Symbol' in df.columns:
                # Add the "Month" column based on the "Symbol" column
                df['Month'] = df['Symbol'].apply(extract_month)
                
                # Reorder columns to place "Month" before "Symbol"
                columns = ['Month'] + [col for col in df.columns if col != 'Month']
                df = df[columns]
                
                # Display the dataframe
                st.write(df)
            else:
                st.error("The 'Symbol' column was not found in the uploaded file.")
                
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

    st.write("---")  # Separator line

    # Manual ROI calculation section
    st.header("Manual ROI Calculation")
    beginning_value = st.number_input("Enter the Beginning Value (Buy Value):", min_value=0.0, format="%.2f")
    ending_value = st.number_input("Enter the Ending Value (Sell Value):", min_value=0.0, format="%.2f")

    if st.button("Calculate ROI"):
        if beginning_value > 0:
            roi = calculate_roi(beginning_value, ending_value)
            st.success(f"The ROI is {roi:.2f}%")
        else:
            st.error("Beginning Value must be greater than 0 to calculate ROI.")

if __name__ == "__main__":
    main()
