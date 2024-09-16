import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Function to load and process the CSV file from GitHub
@st.cache_data
def load_data():
    # URL of the raw CSV file on GitHub
    url = "https://raw.githubusercontent.com/VMantas/IMERGzip/Central1/Data/clim_demo.csv"
    
    # Fetch the content of the file
    response = requests.get(url)
    
    if response.status_code == 200:
        # Load the CSV content into a pandas DataFrame
        df = pd.read_csv(StringIO(response.text), header=None)
        
        # Assign column names
        df.columns = ['zip_code'] + [f'month_{i+1}' for i in range(12)]
        
        return df
    else:
        st.error("Failed to fetch data from the server.")
        return None

# Set up the Streamlit app
st.title("Monthly Precipitation Viewer")

# Load the data
df = load_data()

if df is not None:
    # User input for zip code
    zip_code = st.text_input("Enter a ZIP code:")
    
    if zip_code:
        # Check if the zip code exists in the dataset
        if int(zip_code) in df['zip_code'].values:
            # Get the data for the specified zip code
            zip_data = df[df['zip_code'] == int(zip_code)].iloc[0]
            
            # Prepare data for plotting
            months = [f'Month {i}' for i in range(1, 13)]
            precipitation = zip_data[1:].tolist()
            
            # Create a bar chart using Plotly
            fig = px.bar(x=months, y=precipitation,
                         labels={'x': 'Month', 'y': 'Precipitation'},
                         title=f'Monthly Precipitation for ZIP Code {zip_code}')
            
            # Display the plot
            st.plotly_chart(fig)
        else:
            st.error("ZIP code not found in the dataset.")
else:
    st.error("Failed to load data. Please try again later.")
