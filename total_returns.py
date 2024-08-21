import pandas as pd
import streamlit as st
from futures_monthly_returns import plot_futures_monthly_returns
from options_monthly_returns import plot_options_monthly_returns

def calculate_total_returns(futures_df, options_df):
    # Calculate futures returns
    futures_returns = futures_df['Realized P&L Pct.'].sum()
    
    # Calculate options returns
    options_returns = options_df['Realized P&L Pct.'].sum()
    
    # Calculate total returns
    total_returns = futures_returns + options_returns
    
    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Category': ['Futures', 'Options', 'Total'],
        'Returns (%)': [futures_returns, options_returns, total_returns]
    })
    
    return summary_df

def summarize_total_returns(futures_df, options_df):
    st.title("Total Returns Summary")

    # Calculate and display the total returns
    total_returns_df = calculate_total_returns(futures_df, options_df)
    st.write(total_returns_df)
    
    # Plot individual and combined returns
    st.subheader("Returns Breakdown")
    st.bar_chart(total_returns_df.set_index('Category')['Returns (%)'])

def main():
    st.title("Upload Excel Files to Calculate Total Returns")
    
    # File uploader for the futures data
    futures_file = st.file_uploader("Choose an Excel file for futures data", type=["xlsx", "xls"])
    
    # File uploader for the options data
    options_file = st.file_uploader("Choose an Excel file for options data", type=["xlsx", "xls"])

    if futures_file is not None and options_file is not None:
        try:
            # Read the uploaded Excel files
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
            
            # Plot futures monthly returns
            plot_futures_monthly_returns(futures_df)
            
            # Plot options monthly returns
            plot_options_monthly_returns(options_df)
            
            # Summarize total returns
            summarize_total_returns(futures_df, options_df)
        
        except Exception as e:
            st.error(f"An error occurred while processing the files: {e}")

if __name__ == "__main__":
    main()
