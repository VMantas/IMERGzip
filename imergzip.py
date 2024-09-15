import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Set page title and layout
st.set_page_config(page_title="Precipitation Data Visualization", layout="wide")

# Function to load data from GitHub
@st.cache_data
def load_data(url):
    response = requests.get(url)
    data = StringIO(response.text)
    df = pd.read_csv(data, header=None, names=['ZIP'] + [f'Month_{i}' for i in range(1, 13)])
    return df

# Main app
def main():
    st.title("Precipitation Data Visualization")

    # GitHub raw file URL
    github_url = "https://github.com/VMantas/IMERGzip/blob/Central1/Data/clim_demo.csv"

    # Load data
    df = load_data(github_url)

    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(df)

    # Melt the dataframe for easier plotting
    df_melted = df.melt(id_vars=['ZIP'], var_name='Month', value_name='Precipitation')
    df_melted['Month'] = df_melted['Month'].str.replace('Month_', '')

    # Select ZIP code
    selected_zip = st.selectbox("Select ZIP Code", df['ZIP'].unique())

    # Filter data for selected ZIP code
    df_selected = df_melted[df_melted['ZIP'] == selected_zip]

    # Create line chart
    fig = px.line(df_selected, x='Month', y='Precipitation', title=f"Monthly Precipitation for ZIP Code {selected_zip}")
    st.plotly_chart(fig, use_container_width=True)

    # Show statistics
    st.subheader("Precipitation Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Precipitation", f"{df_selected['Precipitation'].mean():.2f}")
    col2.metric("Minimum Precipitation", f"{df_selected['Precipitation'].min():.2f}")
    col3.metric("Maximum Precipitation", f"{df_selected['Precipitation'].max():.2f}")

    # Heatmap of all ZIP codes
    st.subheader("Precipitation Heatmap")
    fig_heatmap = px.imshow(df.set_index('ZIP').T, 
                            labels=dict(x="ZIP Code", y="Month", color="Precipitation"),
                            aspect="auto",
                            title="Precipitation Heatmap for All ZIP Codes")
    st.plotly_chart(fig_heatmap, use_container_width=True)

if __name__ == "__main__":
    main()
