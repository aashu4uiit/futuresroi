import streamlit as st
import pandas as pd
import yfinance as yf

# Function to calculate simple moving averages
def sma(data, window):
    return data.rolling(window=window).mean()

# Function to fetch historical data and calculate moving averages
def fetch_moving_averages(ticker):
    try:
        # Fetch historical data for the past year
        df_stock = yf.download(ticker, period="1y", interval="1d")
        
        # Calculate moving averages
        sma50 = sma(df_stock['Close'], 50)
        sma150 = sma(df_stock['Close'], 150)
        sma200 = sma(df_stock['Close'], 200)
        sma200_22 = sma200.shift(22)
        
        return sma50, sma150, sma200, sma200_22, df_stock['Close']
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None, None, None

def stage2_analysis():   
 uploaded_file = st.file_uploader("Upload your portfolio file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Check if the file is empty
    if uploaded_file.size == 0:
        st.error("Uploaded file is empty. Please upload a valid CSV or Excel file.")
        st.stop()

    st.write(f"File name: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size} bytes")

    # Load the data based on file type
    try:
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        st.write(f"Loaded DataFrame shape: {df.shape}")
        st.write(f"First few rows of the DataFrame:")
        st.write(df.head())

        if df.empty:
            st.error("No data found in the file. Please check the file content.")
            st.stop()

    except pd.errors.EmptyDataError:
        st.error("The file is empty or not in the correct format. Please check the file and try again.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
        st.stop()

    # Strip any leading or trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Handle the Date column, assuming it might contain Excel serial date numbers
    try:
        # Attempt to convert the Date column to integers first
        df['Date'] = pd.to_numeric(df['Date'], errors='coerce').fillna(df['Date'])
        # Now convert to datetime, handling Excel serial numbers and standard date formats
        df['Date'] = pd.to_datetime(df['Date'], origin='1899-12-30', unit='D', errors='coerce').fillna(pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce'))

        if df['Date'].isnull().any():
            st.warning("Some dates could not be parsed. Please check your data.")
            df = df.dropna(subset=['Date'])

    except Exception as e:
        st.error(f"Error parsing dates: {e}")
        st.stop()

    # Initialize a list to store results for each stock
    results = []

    # Loop through each stock to fetch data and check the conditions
    for i, row in df.iterrows():
        ticker = row['Corrected Ticker']

        # Fetch historical data and calculate moving averages
        sma50, sma150, sma200, sma200_22, close = fetch_moving_averages(ticker)

        if sma50 is not None and not sma50.empty and not sma150.empty and not sma200.empty:
            # Ensure the Series are long enough to access the last element
            if len(close) > 0 and len(sma150) > 0 and len(sma200) > 0:
                # Criteria checks
                is_price_above_sma_150_and_200 = (close.iloc[-1] > sma150.iloc[-1]) & (close.iloc[-1] > sma200.iloc[-1])
                is_sma_150_above_sma_200 = (sma150.iloc[-1] > sma200.iloc[-1])
                is_trending_at_least_1_month = (sma200.iloc[-1] > sma200_22.iloc[-1]) if len(sma200_22) > 0 else False
                is_sma_50_above_sma_150_and_200 = (sma50.iloc[-1] > sma150.iloc[-1]) & (sma50.iloc[-1] > sma200.iloc[-1])

                # Store the result for this stock including the moving averages
                result = {
                    'Ticker': ticker,
                    'Close Price': close.iloc[-1],
                    'SMA 50': sma50.iloc[-1],
                    'SMA 150': sma150.iloc[-1],
                    'SMA 200': sma200.iloc[-1],
                    'Price > MA 150 & 200': 'Yes' if is_price_above_sma_150_and_200 else 'No',
                    'MA 150 > MA 200': 'Yes' if is_sma_150_above_sma_200 else 'No',
                    'MA 200 trending > 1 month': 'Yes' if is_trending_at_least_1_month else 'No',
                    'MA 50 > MA 150 & 200': 'Yes' if is_sma_50_above_sma_150_and_200 else 'No',
                }
                results.append(result)
            else:
                st.warning(f"Not enough data points to evaluate {ticker}.")
        else:
            st.warning(f"Insufficient data to calculate moving averages for {ticker}.")

    # Convert results to a DataFrame for display
    results_df = pd.DataFrame(results)
    
    # Display the results including moving averages
    st.subheader("Analysis Results for All Stocks")
    st.write(results_df)
    
    # Optionally, allow download of the results as a CSV file
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Results as CSV", data=csv, file_name='analysis_results.csv', mime='text/csv')

