import streamlit as st
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

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
    st.write("This app allows you to upload an Excel file to view and analyze percentage returns.")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

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

            # Convert the 'Realized P&L Pct.' column to numeric
            df['Realized P&L Pct.'] = pd.to_numeric(df['Realized P&L Pct.'], errors='coerce')

            # Plot the percentage returns as a bar chart with the actual return number on the bars
            st.header("Percentage Returns")
            plt.figure(figsize=(10, 6))
            bars = plt.bar(df['Symbol'], df['Realized P&L Pct.'], color='skyblue')
            plt.xlabel('Symbol')
            plt.ylabel('Realized P&L Pct. (%)')
            plt.title('Realized P&L Percentage by Symbol')
            plt.xticks(rotation=90)
            
            # Add the return numbers on top of the bars
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', ha='center', va='bottom')

            # Display the plot in Streamlit
            st.pyplot(plt)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
