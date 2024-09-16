import streamlit as st
import pandas as pd
import requests
import io

# URL to the CSV file
url = "https://github.com/VMantas/IMERGzip/raw/Central1/Data/clim_demo.csv"

# Function to load the CSV file from the URL
@st.cache_data
def load_data():
    response = requests.get(url)
    data = response.content.decode('utf-8')
    # Use io.StringIO to convert the string data into a file-like object for pandas
    df = pd.read_csv(io.StringIO(data), header=None)
    return df

# Function to get the precipitation values for a given ZIP code
def get_precipitation_for_zip(df, zip_code):
    # Filter the dataframe by the provided ZIP code (first column)
    row = df[df[0] == zip_code]
    if not row.empty:
        return row.iloc[0, 1:].tolist()  # Return the monthly values
    else:
        return None

# Load the data
df = load_data()

# Streamlit app UI
st.title("Precipitation Data by ZIP Code")

# User input for the ZIP code
zip_code = st.text_input("Enter a ZIP code:", "")

if zip_code:
    # Try to convert ZIP code input to an integer
    try:
        zip_code = int(zip_code)
        # Get the precipitation data for the ZIP code
        precipitation_values = get_precipitation_for_zip(df, zip_code)
        
        if precipitation_values:
            st.subheader(f"Precipitation values for ZIP code: {zip_code}")
            # Display the monthly precipitation values
            months = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
            precipitation_dict = dict(zip(months, precipitation_values))
            st.table(precipitation_dict.items())
        else:
            st.error("No data found for this ZIP code.")
    except ValueError:
        st.error("Please enter a valid numeric ZIP code.")
