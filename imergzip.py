import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io

# Set page config
st.set_page_config(page_title="Precipitation Data", layout="wide")

# Function to load data from GitHub
@st.cache_data
def load_data(url):
    response = requests.get(url)
    data = io.StringIO(response.text)
    
    # Read the CSV file line by line
    zip_data = {}
    for line in data:
        values = line.strip().split(',')
        if len(values) == 13:  # Ensure we have ZIP + 12 months of data
            zip_code = values[0]
            precipitation = [float(v) for v in values[1:]]
            zip_data[zip_code] = precipitation
    
    return zip_data

# Main app
def main():
    st.title("Monthly Precipitation Data")

    # GitHub raw file URL
    github_url = "https://raw.githubusercontent.com/yourusername/yourrepository/main/yourfile.csv"

    # Load data
    data = load_data(github_url)

    # User input for ZIP code
    zip_code = st.text_input("Enter ZIP Code:")

    if zip_code:
        if zip_code in data:
            # Get data for the specified ZIP code
            precipitation = data[zip_code]
            df = pd.DataFrame({
                'Month': range(1, 13),
                'Precipitation': precipitation
            })

            # Create line chart
            fig = px.line(df, x='Month', y='Precipitation', 
                          title=f"Monthly Precipitation for ZIP Code {zip_code}",
                          labels={'Precipitation': 'Precipitation', 'Month': 'Month'},
                          markers=True)
            
            fig.update_layout(xaxis = dict(tickmode = 'linear', tick0 = 1, dtick = 1))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("ZIP code not found in the dataset.")

if __name__ == "__main__":
    main()
