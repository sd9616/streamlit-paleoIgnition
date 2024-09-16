import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
col1, col2 = st.columns(2)

with col1: 
    st.write("# Welcome to PaleoIgnition!👋")
    st.markdown(
        """
        PaleoIgnition is an app built to provide paleofire practitioners with a paleolightning reconstruction for their study sites. 
        
        * Head to the __Lightning Time Series Plotter__ page on the left side bar to create a reconstruction of any site
        * Head to the __Lightning Map Plotter__ page to create heat maps for any point in time 
        * Find out more about the datasets used on the __Dataset Info + References__ page
        
        """)

with col2: 
    st.image("paleoignition_logo_white.png", width=500)

df = pd.read_csv('charcoal_records.csv')



# Streamlit map requires a dataframe with 'latitude' and 'longitude' columns
st.title('Map of Sites')

# Drop rows where latitude or longitude is missing
df_cleaned = df.dropna(subset=['latitude', 'longitude'])

# Display the cleaned map with valid latitude and longitude
st.map(df_cleaned[['latitude', 'longitude']])

# Optionally: Show a table with only the valid rows (with no missing values)
st.dataframe(df_cleaned)
