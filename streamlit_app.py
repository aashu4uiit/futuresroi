import streamlit as st

def calculate_roi(beginning_value, ending_value):
    return ((ending_value - beginning_value) / beginning_value) * 100

def main():
    st.title("ROI Calculator")
    st.write("This app calculates the Return on Investment (ROI) based on beginning and ending values.")

    # User inputs
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
