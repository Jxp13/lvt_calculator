import streamlit as st

# Simple test app
st.title("Business Calculator Test")

# Basic inputs
revenue = st.number_input("Monthly Revenue ($)", value=1000)
customers = st.number_input("Number of Customers", value=10)

# Simple calculation
average_revenue = revenue / customers if customers > 0 else 0

# Display result
st.write(f"Average Revenue per Customer: ${average_revenue:.2f}")

# Add a test button
if st.button("Test Button"):
    st.success("Everything is working!")
