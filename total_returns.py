import pandas as pd
import streamlit as st
import numpy as np

# Function to calculate geometric mean
def geometric_mean(returns):
    # Convert percentage returns to decimal form
    returns = returns / 100 + 1
    # Calculate geometric mean
    gmr = np.prod(returns) ** (1 / len(returns)) - 1
    # Convert back to percentage form
    return gmr * 100

# Function to calculate total returns
def calculate_total_returns(df, charges_value):
    # Filter futures and options data
    futures_df = df[df['Symbol'].str.endswith('FUT')]
    options_df = df[df['Symbol'].str.endswith(('CE', 'PE'))]

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

# Main function to summarize total returns
def summarize_total_returns(futures_df, options_df, charges_value):
    # Calculate total returns
    total_returns_df = calculate_total_returns(futures_df, charges_value)

    # Display the summary table
    st.write("Total Returns Summary:")
    st.write(total_returns_df)

    # Plot the returns using Streamlit's bar_chart
    st.subheader("Returns Breakdown")
    st.bar_chart(total_returns_df.set_index('Category')['Geometric Mean (%)'])
