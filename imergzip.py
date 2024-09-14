import os
import ee
import streamlit as st
from PIL import Image
import numpy as np
import io

# Initialize Earth Engine with environment variable
def initialize_earth_engine():
    auth_token = os.getenv('EARTHENGINE_AUTH_TOKEN')
    if auth_token:
        ee.Authenticate(token=auth_token)
    ee.Initialize()

# Function to get an Earth Engine image
def get_earth_engine_image():
    # Define a region of interest (ROI) and date range
    roi = ee.Geometry.Polygon([[
        [-122.6, 37.5],
        [-122.3, 37.5],
        [-122.3, 37.8],
        [-122.6, 37.8]
    ]])
    date_range = ee.DateRange('2022-01-01', '2022-01-31')

    # Load a Sentinel-2 image
    image = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(roi) \
        .filterDate(date_range) \
        .median()

    # Select a specific band (e.g., true color)
    image = image.select(['B4', 'B3', 'B2'])

    # Convert the image to a numpy array
    image_url = image.getThumbURL({'min': 0, 'max': 3000, 'dimensions': 512})
    response = ee.data.getTile(image_url)
    img = Image.open(io.BytesIO(response.content))
    return img

# Streamlit app setup
st.title("Google Earth Engine Streamlit App")

# Initialize Earth Engine
initialize_earth_engine()

# Get the image
try:
    image = get_earth_engine_image()
    st.image(image, caption='Sentinel-2 Image', use_column_width=True)
except Exception as e:
    st.error(f"Error retrieving image from Earth Engine: {str(e)}")

st.write("""
This app uses Google Earth Engine to display a satellite image of a specific region.
""")
