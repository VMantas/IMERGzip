import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
import plotly.graph_objects as go

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
st.title("IMERG Precipitation Climatology (Prototype)")

# Add a description for IMERG
st.markdown("""
### What is IMERG?
The Integrated Multi-satellite Retrievals for GPM (IMERG) is a product of the Global Precipitation Measurement (GPM) mission. It combines satellite observations from a constellation of satellites to provide global estimates of precipitation. This allows scientists and researchers to track precipitation trends, identify extreme weather events, and monitor water resources across the globe in near real-time. Use the data in this website for educational purposes only. NO quality control was done. This is NOT an official website or affiliated with NASA in any way.

More information about IMERG can be found on the [NASA IMERG website](https://gpm.nasa.gov/data/imerg).
""")

# Add an image related to IMERG
st.image("https://gpm.nasa.gov/sites/default/files/styles/550_width/public/2020-02/GPM_Logo_Transparent.png?itok=rLVGY90d", 
         caption="NASA GPM logo (Source: gpm.nasa.gov)", width=300)

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
            # Highlight September's precipitation
            normal_precipitation_sept = 4.3  # Example normal value (in)
            current_precipitation_sept = 1.7 #precipitation_values[8]  # September's precipitation value

            st.subheader(f"September Precipitation: {current_precipitation_sept} mm ")

            # Create the gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=current_precipitation_sept,
                delta={'reference': normal_precipitation_sept, 'relative': True, 'position': "top",'valueformat': '.0%'},
                gauge={
                    'axis': {'range': [0, normal_precipitation_sept], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, normal_precipitation_sept * 0.6], 'color': "lightcoral"},
                        {'range': [normal_precipitation_sept * 0.6, normal_precipitation_sept], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': current_precipitation_sept},
                },
                title={'text': "September Precipitation"},
                domain={'x': [0, 1], 'y': [0, 1]}
            ))

            # Display the gauge chart
            st.plotly_chart(fig_gauge)
        else:
            st.error("No data found for this ZIP code.")
    except ValueError:
        st.error("Please enter a valid numeric ZIP code.")
