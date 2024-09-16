import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load and process the CSV file
@st.cache_data
def load_data(file_path):
    # Load the CSV file without headers
    df = pd.read_csv(file_path, header=None)
    
    # Assign column names
    df.columns = ['zip_code'] + [f'month_{i+1}' for i in range(12)]
    
    return df

# Set up the Streamlit app
st.title("Monthly Precipitation Viewer")

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the data
    df = load_data(uploaded_file)
    
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
    st.info("Please upload a CSV file to proceed.")
