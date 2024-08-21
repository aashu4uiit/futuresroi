import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def extract_month_year(symbol):
    month_mapping = {
        'JAN': 'January', 'FEB': 'February', 'MAR': 'March',
        'APR': 'April', 'MAY': 'May', 'JUN': 'June',
        'JUL': 'July', 'AUG': 'August', 'SEP': 'September',
        'OCT': 'October', 'NOV': 'November', 'DEC': 'December'
    }
    month_code = symbol[7:10]
    year = symbol[5:7]
    month = month_mapping.get(month_code.upper(), 'Unknown')
    return f"{month[:3]}-{year}"

def plot_futures_monthly_returns(df):
    st.header("Futures Monthly Percentage Returns")
    
    # Calculate geometric mean return
    monthly_returns = df.groupby('Month-Year')['Realized P&L Pct.'].mean()
    monthly_returns = monthly_returns[monthly_returns != 0]  # Filter out 0 values
    gmean_return = np.prod(monthly_returns + 1) ** (1 / len(monthly_returns)) - 1
    
    # Filter the DataFrame to include only Futures transactions (Symbol ends with 'FUT')
    df = df[df['Symbol'].str.endswith('FUT')]
    
    # Extract month and year from the Symbol column
    df['Month-Year'] = df['Symbol'].apply(extract_month_year)
    
    # Filter the DataFrame to only include rows with Realized P&L values
    df = df[df['Realized P&L Pct.'].notnull()]

    # Define the correct order of months starting from April
    month_order = [
        'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 
        'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'
    ]
    
    # Create a list of ordered Month-Year combinations
    ordered_month_year = []
    for year in sorted(df['Month-Year'].str[-2:].unique()):
        for month in month_order:
            ordered_month_year.append(f"{month}-{year}")
    
    # Aggregate returns by Month-Year
    monthly_returns = df.groupby('Month-Year')['Realized P&L Pct.'].mean()

    # Filter out months with 0 values
    monthly_returns = monthly_returns[monthly_returns != 0]

    # Reindex the DataFrame to ensure the correct order of Month-Year
    monthly_returns = monthly_returns.reindex(ordered_month_year).dropna()

    # Calculate the overall return
    overall_return = monthly_returns.mean()

    # Add the overall return as a new entry
    monthly_returns['Overall'] = overall_return

     # Add geometric mean return as a new entry
    monthly_returns['Overall (Geometric Mean)'] = gmean_return * 100  # Convert to percentage

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(monthly_returns.index, monthly_returns.values, color='skyblue')
    plt.xlabel('Month-Year')
    plt.ylabel('Average Realized P&L Pct. (%)')
    plt.title('Futures Average Monthly Realized P&L Percentage with Overall Return')
    plt.xticks(rotation=45)
    
    # Add the return numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', ha='center', va='bottom')

    # Display the plot in Streamlit
    st.pyplot(plt)

