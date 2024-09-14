import streamlit as st
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import Point
import uszipcode
import requests
from io import BytesIO
from streamlit_extras.react_component import react_component

# Initialize the zip code search engine
search = uszipcode.SearchEngine()

# Function to convert zip code to coordinates
def zip_to_coords(zipcode):
    result = search.by_zipcode(zipcode)
    if result:
        return result.lat, result.lng
    return None

# Function to extract data from GeoTIFF (local or remote)
def extract_from_geotiff(lat, lon, geotiff_url):
    point = Point(lon, lat)
    
    # If the URL is a local file path, open it directly
    if geotiff_url.startswith(('http://', 'https://')):
        response = requests.get(geotiff_url)
        with rasterio.open(BytesIO(response.content)) as src:
            geom = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326").to_crs(src.crs)
            out_image, out_transform = mask(src, geom.geometry, crop=True)
            return out_image[0][0][0]  # Assuming single-band GeoTIFF
    else:
        with rasterio.open(geotiff_url) as src:
            geom = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326").to_crs(src.crs)
            out_image, out_transform = mask(src, geom.geometry, crop=True)
            return out_image[0][0][0]  # Assuming single-band GeoTIFF

# Streamlit app
st.set_page_config(page_title="GeoTIFF Data Visualization", layout="centered")

st.title("GeoTIFF Data Visualization with Pool Fill")

zipcode = st.text_input("Enter a ZIP code:")
geotiff_url = "https://github.com/VMantas/IMERGzip/blob/Central1/Data/January%20IMERGF%20Mean.tif" #st.text_input("Enter the URL or local path to your GeoTIFF file:")

if zipcode and geotiff_url:
    coords = zip_to_coords(zipcode)
    if coords:
        lat, lon = coords
        st.write(f"Coordinates for {zipcode}: Lat {lat}, Lon {lon}")
        
        try:
            value = extract_from_geotiff(lat, lon, geotiff_url)
            st.write(f"Extracted value from GeoTIFF: {value}")
            
            # Normalize the value to a percentage (0-100)
            # You may need to adjust this based on your GeoTIFF data range
            min_value = 0  # Replace with the minimum value in your GeoTIFF
            max_value = 100  # Replace with the maximum value in your GeoTIFF
            normalized_value = ((value - min_value) / (max_value - min_value)) * 100
            normalized_value = max(0, min(normalized_value, 100))  # Ensure it's between 0 and 100
            
            # Display the pool visualization
            st.write("Pool fill based on GeoTIFF data:")
            react_component("PoolFill", props={"initialFillPercentage": normalized_value})
            
        except Exception as e:
            st.error(f"Error extracting data from GeoTIFF: {str(e)}")
    else:
        st.error("Invalid ZIP code or coordinates not found.")

st.write("""
This app extracts data from a GeoTIFF file based on a given ZIP code and visualizes it as a pool fill level.
Enter a ZIP code and the URL or path to a GeoTIFF file to see the result.
""")

st.write("Note: This app requires the `streamlit-extras`, `geopandas`, `rasterio`, `shapely`, and `uszipcode` packages.")
