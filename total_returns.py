import pandas as pd
import streamlit as st
import numpy as np
from futures_monthly_returns import plot_futures_monthly_returns
from options_monthly_returns import plot_options_monthly_returns

def geometric_mean(returns):
    # Convert percentage returns to decimal form
    returns = returns / 100 + 1
    # Calculate geometric mean
    gmr = np.prod(returns) ** (1 / len(returns)) - 1
    # Convert back to percentage form
    return gmr * 100

def calculate_total_returns(futures_df, options_df):
    # Calculate geometric mean for futures
    futures_gmr = geometric_mean(futures_df['Realized P&L Pct.'])

    # Calculate geometric mean for options
    options_gmr = geometric_mean(options_df['Realized P&L Pct.'])

    # Calculate combined geometric mean
    combined_returns = pd.concat([futures_df['Realized P&L Pct.'], options_df['Realized P&L Pct.']])
    total_geometric_mean = geometric_mean(combined_returns)

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Category': ['Futures', 'Options', 'Total'],
        'Geometric Mean (%)': [futures_gmr, options_gmr, total_geometric_mean]
    })
    
    return summary_df

def summarize_total_returns(futures_df, options_df):
    st.title("Total Returns Summary")

    # Calculate and display the total returns (geometric mean only)
    total_returns_df = calculate_total_returns(futures_df, options_df)
    st.write(total_returns_df)
    
    # Plot individual and combined returns
    st.subheader("Returns Breakdown")
    st.bar_chart(total_returns_df.set_index('Category')['Geometric Mean (%)'])

def main():
    st.title("Upload Excel File to Calculate Total Returns")
    
    # File uploader for the main data
    uploaded_file = st.file_uploader("Choose an Excel file for data", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the uploaded Excel file
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=36, header=0)
            
            # Rename columns using the first row as headers
            df.columns = df.iloc[0]  # Set the first row as the header
            df = df[1:]  # Remove the first row from the dataframe
            df.columns = df.columns.str.strip()
            df.columns.name = None
            
            # Separate futures and options data
            futures_df = df[df['Symbol'].str.endswith('FUT')]
            options_df = df[df['Symbol'].str.endswith(('CE', 'PE'))]
            
            # Plot futures monthly returns
            plot_futures_monthly_returns(futures_df)
            
            # Plot options monthly returns
            plot_options_monthly_returns(options_df)
            
            # Summarize total returns (geometric mean only)
            summarize_total_returns(futures_df, options_df)
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
