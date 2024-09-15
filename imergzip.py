import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Set page config
st.set_page_config(page_title="Precipitation Data", layout="wide")

# Function to load data from GitHub
@st.cache_data
def load_data(url):
    response = requests.get(url)
    data = StringIO(response.text)
    df = pd.read_csv(data, header=None, names=['ZIP'] + list(range(1, 13)))
    return df

# Main app
def main():
    st.title("Monthly Precipitation Data")

    # GitHub raw file URL
    github_url = "https://raw.githubusercontent.com/yourusername/yourrepository/main/yourfile.csv"

    # Load data
    df = load_data(github_url)

    # User input for ZIP code
    zip_code = st.text_input("Enter ZIP Code:")

    if zip_code:
        if int(zip_code) in df['ZIP'].values:
            # Get data for the specified ZIP code
            zip_data = df[df['ZIP'] == int(zip_code)].iloc[0, 1:].reset_index()
            zip_data.columns = ['Month', 'Precipitation']
            zip_data['Month'] = zip_data['Month'] + 1  # Adjust month numbers

            # Create line chart
            fig = px.line(zip_data, x='Month', y='Precipitation', 
                          title=f"Monthly Precipitation for ZIP Code {zip_code}",
                          labels={'Precipitation': 'Precipitation', 'Month': 'Month'},
                          markers=True)
            
            fig.update_layout(xaxis = dict(tickmode = 'linear', tick0 = 1, dtick = 1))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("ZIP code not found in the dataset.")

if __name__ == "__main__":
    main()
