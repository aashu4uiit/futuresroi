import streamlit as st
import pandas as pd

# Ensure that the openpyxl package is installed
try:
    import openpyxl
except ImportError:
    st.error("Missing optional dependency 'openpyxl'. Please install it using 'pip install openpyxl'.")
    st.stop()  # Stop the script execution if openpyxl is not available

def calculate_roi(beginning_value, ending_value):
    return ((ending_value - beginning_value) / beginning_value) * 100

def main():
    st.title("ROI Calculator & File Uploader")
    st.write("This app allows you to upload an Excel file or manually input values to calculate ROI.")

    # File uploader section
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the uploaded Excel file
        df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl')
        
        # Display the dataframe
        st.write(df)

        # Additional processing can go here...

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
