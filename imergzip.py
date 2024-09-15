import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the app
st.title("CSV File Plotter from GitHub")

# GitHub raw CSV link
csv_url = "https://raw.githubusercontent.com/VMantas/IMERGzip/Central1/Data/clim_demo.csv"

# Read the CSV from GitHub directly
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(csv_url)

# Show a preview of the data
st.write("Here is a preview of the data from GitHub:")
st.write(df.head())

# Ensure the CSV has the expected format
if df.shape[1] == 13:
    # Select which row to plot (first column is the ID)
    row_id = st.selectbox('Select row ID to plot:', df.iloc[:, 0])
    
    # Extract the row data (excluding the ID)
    row_data = df[df.iloc[:, 0] == row_id].iloc[:, 1:].values.flatten()
    
    # Plot the data using Plotly
    fig = px.line(x=list(range(1, 13)), y=row_data, 
                  labels={'x': 'Column Index', 'y': 'Value'},
                  title=f'Plot for Row ID {row_id}')
    st.plotly_chart(fig)
else:
    st.error("The CSV file should have exactly 13 columns.")

