import streamlit as st
import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import Point
import uszipcode
import requests
from io import BytesIO
from pool_fill_component import st_pool_fill

# Initialize the zip code search engine
search = uszipcode.SearchEngine()

# Function to convert zip code to coordinates
def zip_to_coords(zipcode):
    result = search.by_zipcode(zipcode)
    if result:
        return result.lat, result.lng
    return None

# Function to extract data from GeoTIFF (GitHub or local)
def extract_from_geotiff(lat, lon, geotiff_url):
    point = Point(lon, lat)
    
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

# Assuming the GeoTIFF file is in the Data folder of your GitHub repository
geotiff_url = "https://github.com/VMantas/IMERGzip/blob/Central1/Data/January%20IMERGF%20Mean.tif"
st.write(f"Using GeoTIFF file from: {geotiff_url}")

zipcode = st.text_input("Enter a ZIP code:")

if zipcode:
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
            
            # Display the pool visualization using the custom component
            st.write("Pool fill based on GeoTIFF data:")
            st_pool_fill(normalized_value)
            
        except Exception as e:
            st.error(f"Error extracting data from GeoTIFF: {str(e)}")
    else:
        st.error("Invalid ZIP code or coordinates not found.")

st.write("""
This app extracts data from a GeoTIFF file based on a given ZIP code and visualizes it as a pool fill level.
Enter a ZIP code to see the result.
""")
