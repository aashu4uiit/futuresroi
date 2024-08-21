import streamlit as st
import pandas as pd
import openpyxl

def extract_charges(df):
    # Diagnostic: Display the entire DataFrame to understand its structure
    st.write("Full DataFrame:")
    st.write(df)
    
    # Attempt to locate the row where "Charges" is located
    charges_row = df[df.isin(['Charges']).any(axis=1)]
    
    # Check if the row was found and extract the value
    if not charges_row.empty:
        # Log the entire row for verification
        st.write("Charges row found:", charges_row)
        
        # Assuming the value is in the third column
        charges_value = charges_row.iloc[0, 2]  # Adjust if the charges value is in a different column
        return charges_value
    else:
        st.error("Charges row not found. Verify that 'Charges' is spelled correctly and present in the data.")
        return None

def main():
    st.title("Charges Extractor")
    st.write("This app allows you to upload an Excel file and extract the Charges value.")

    # File uploader for the main data
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the uploaded Excel file, skip the first 13 rows
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=13, header=None)
            
            # Display the raw data for verification
            st.write("Data preview:")
            st.write(df.head(20))  # Display the first 20 rows to inspect
            
            # Extract and display the charges
            charges_value = extract_charges(df)
            if charges_value is not None:
                # Log the extracted charges value
                st.write(f"Extracted Charges value: {charges_value}")
                
                # Display the charges in a table
                charges_table = pd.DataFrame({'Charges': [charges_value]})
                st.write("Charges Table:")
                st.write(charges_table)
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
