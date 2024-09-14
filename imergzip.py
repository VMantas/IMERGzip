import streamlit as st
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import Point
import uszipcode
import requests
from io import BytesIO
import numpy as np

# Initialize the zip code search engine
search = uszipcode.SearchEngine()

# Function to convert zip code to coordinates
def zip_to_coords(zipcode):
    result = search.by_zipcode(zipcode)
    if result:
        return result.lat, result.lng
    return None

# Function to extract mean value from GeoTIFF for given coordinates
def extract_mean_from_geotiff(lat, lon, geotiff_url):
    point = Point(lon, lat)
    
    response = requests.get(geotiff_url)
    with rasterio.open(BytesIO(response.content)) as src:
        # Convert the point to the same CRS as the GeoTIFF file
        geom = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326").to_crs(src.crs)
        
        # Mask the raster using the geometry and extract the pixel values
        out_image, out_transform = mask(src, geom.geometry, crop=True)
        
        # Handle no-data values and compute mean
        out_image = out_image[~np.isnan(out_image)]
        if out_image.size > 0:
            return np.mean(out_image)
        else:
            return None

# Streamlit app
st.title("GeoTIFF Mean Value Extractor")

# Corrected URL to the raw GeoTIFF file
geotiff_url = "https://raw.githubusercontent.com/VMantas/IMERGzip/Central1/Data/January%20IMERGF%20Mean.tif"
st.write(f"Using GeoTIFF file from: {geotiff_url}")

zipcode = st.text_input("Enter a ZIP code:")

if zipcode:
    coords = zip_to_coords(zipcode)
    if coords:
        lat, lon = coords
        st.write(f"Coordinates for {zipcode}: Lat {lat}, Lon {lon}")
        
        try:
            mean_value = extract_mean_from_geotiff(lat, lon, geotiff_url)
            if mean_value is not None:
                st.write(f"Mean value extracted from GeoTIFF: {mean_value:.4f}")
            else:
                st.error("No valid data found in the specified location.")
        except Exception as e:
            st.error(f"Error extracting data from GeoTIFF: {str(e)}")
    else:
        st.error("Invalid ZIP code or coordinates not found.")

st.write("""
This app extracts the mean pixel value from a GeoTIFF file for a given ZIP code.
Enter a ZIP code to see the result.
""")
