import streamlit as st
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import Point
import requests
from io import BytesIO
import numpy as np
from geopy.geocoders import Nominatim

# Function to convert ZIP code to coordinates using geopy and Nominatim
import geocoder

def zip_to_coords(zipcode):
    # Use geocoder to get latitude and longitude for a ZIP code
     g = geocoder.osm(zipcode, user_agent="demoinergzip")
    g = geocoder.osm(zipcode)
    if g.ok:
        return g.latlng  # Returns [latitude, longitude]
    return None

# Function to extract mean value from GeoTIFF for given coordinates
def extract_mean_from_geotiff(lat, lon, geotiff_url):
    point = Point(lon, lat)
    
    response = requests.get(geotiff_url)
    if response.status_code == 200:
        with rasterio.open(BytesIO(response.content)) as src:
            geom = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326").to_crs(src.crs)
            out_image, out_transform = mask(src, geom.geometry, crop=True)
            
            # Filter out NoData values
            out_image = out_image[~np.isnan(out_image)]
            
            # Compute mean value if valid data exists
            if out_image.size > 0:
                return np.mean(out_image)
            else:
                return None
    else:
        st.error("Failed to retrieve GeoTIFF from the provided URL.")
        return None

# Streamlit app setup
st.title("GeoTIFF Value Extractor by ZIP Code")

# Provide the URL of the GeoTIFF file (hosted on GitHub in this example)
geotiff_url = "https://raw.githubusercontent.com/VMantas/IMERGzip/Central1/Data/January%20IMERGF%20Mean.tif"
st.write(f"Using GeoTIFF file from: {geotiff_url}")

# User input: ZIP code
zipcode = st.text_input("Enter a ZIP code:")

if zipcode:
    # Convert ZIP code to coordinates
    coords = zip_to_coords(zipcode)
    
    if coords:
        lat, lon = coords
        st.write(f"Coordinates for {zipcode}: Lat {lat}, Lon {lon}")
        
        # Extract the mean value from the GeoTIFF for the given coordinates
        try:
            mean_value = extract_mean_from_geotiff(lat, lon, geotiff_url)
            if mean_value is not None:
                st.write(f"Mean value extracted from GeoTIFF: {mean_value:.4f}")
            else:
                st.write("No valid data found in the GeoTIFF for the specified location.")
        except Exception as e:
            st.error(f"Error extracting data from GeoTIFF: {str(e)}")
    else:
        st.error("Invalid ZIP code or unable to retrieve coordinates.")
        
st.write("""
This app extracts the mean pixel value from a GeoTIFF file for a given ZIP code.
Enter a ZIP code to see the result.
""")

