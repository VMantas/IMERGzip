import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px

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
st.title("IMERG Precipitation Climatology")

# Add a description for IMERG
st.markdown("""
### What is IMERG?
The Integrated Multi-satellite Retrievals for GPM (IMERG) is a product of the Global Precipitation Measurement (GPM) mission. It combines satellite observations from a constellation of satellites to provide global estimates of precipitation. This allows scientists and researchers to track precipitation trends, identify extreme weather events, and monitor water resources across the globe in near real-time.

More information about IMERG can be found on the [NASA IMERG website](https://gpm.nasa.gov/data/imerg).
""")

# Add an image related to IMERG
st.image("https://gpm.nasa.gov/sites/default/files/styles/large/public/2019-06/imerg_logo.png", 
         caption="NASA IMERG (Source: gpm.nasa.gov)")

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
            
            # Create a DataFrame for the precipitation values
            months = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
            precipitation_df = pd.DataFrame({
                'Month': months,
                'Precipitation': precipitation_values
            })
            
            # Create a bar graph using plotly
            fig = px.bar(precipitation_df, x='Month', y='Precipitation', 
                         labels={'Precipitation': 'Precipitation (in)'}, 
                         title=f'Monthly Precipitation for ZIP Code {zip_code}')
            
            # Display the bar graph
            st.plotly_chart(fig)
        else:
            st.error("No data found for this ZIP code.")
    except ValueError:
        st.error("Please enter a valid numeric ZIP code.")
