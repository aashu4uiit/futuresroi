import pandas as pd
import streamlit as st
import pygwalker as pyg

# Function to calculate geometric mean
def geometric_mean(returns):
    # Convert percentage returns to decimal form
    returns = returns / 100 + 1
    # Calculate geometric mean
    gmr = returns.prod() ** (1 / len(returns)) - 1
    # Convert back to percentage form
    return gmr * 100

# Function to calculate total returns
def calculate_total_returns(df, charges_value):
    st.write("Calculating total returns...")

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

    # Assuming charges_value is in absolute terms, calculate its impact
    total_notional_amount = futures_df['Amount'].sum() + options_df['Amount'].sum()
    charges_percentage_impact = (charges_value / total_notional_amount) * 100

    # Adjust the total geometric mean by the charges
    net_total_geometric_mean = total_geometric_mean - charges_percentage_impact

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Category': ['Futures', 'Options', 'Total', 'Net Total (after Charges)'],
        'Geometric Mean (%)': [futures_gmr, options_gmr, total_geometric_mean, net_total_geometric_mean]
    })

    return summary_df

# Main function
def main():
    st.title("Upload Excel File to Explore and Calculate Returns with Pygwalker")

    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file, sheet_name='F&O', engine='openpyxl', skiprows=36, header=0)
            df.columns = df.iloc[0]  # Set the first row as the header
            df = df[1:]  # Remove the first row from the dataframe
            df.columns = df.columns.str.strip()
            df.columns.name = None

            # Display the data with Pygwalker
            pyg.walk(df)  # Interactive data exploration

            # Extract charges
            charges_value = df.loc[df['Symbol'] == 'Charges', 'Amount'].values[0]
            st.write(f"Charges: {charges_value}")

            # Calculate and display total returns
            summary_df = calculate_total_returns(df, charges_value)
            st.write(summary_df)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    main()
