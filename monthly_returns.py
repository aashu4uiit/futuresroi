import streamlit as st
import matplotlib.pyplot as plt

def plot_monthly_returns(df):
    st.header("Monthly Percentage Returns")
    
    # Define the correct order of months starting from April
    month_order = [
        'April', 'May', 'June', 'July', 'August', 'September', 
        'October', 'November', 'December', 'January', 'February', 'March'
    ]
    
    # Aggregate returns by month
    monthly_returns = df.groupby('Month')['Realized P&L Pct.'].mean()

    # Reindex the DataFrame to ensure the correct order of months
    monthly_returns = monthly_returns.reindex(month_order)

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly_returns.index, monthly_returns.values, color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Average Realized P&L Pct. (%)')
    plt.title('Average Monthly Realized P&L Percentage')
    plt.xticks(rotation=90)
    
    # Add the return numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}%', ha='center', va='bottom')

    # Display the plot in Streamlit
    st.pyplot(plt)
