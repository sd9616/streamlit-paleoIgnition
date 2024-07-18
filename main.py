import streamlit as st 
from streamlit_option_menu import option_menu

# st.title('Lightning App')


# st.sidebar.success("Select a demo above.")

col1, col2 = st.columns(2)

with col1: 
    st.write("# Welcome to PaleoIgnition!👋")
    st.markdown(
        """
        PaleoIgnition is an app built to provide paleofire practitioners with a paleolightning reconstruction for their study sites. 
        
        * Head to the __Lightning Time Series Plotter__ page on the left side bar to create a reconstruction of any site
        * Find out more about the datasets used on the __Dataset Info + References__ page
        
        """)

with col2: 
    st.image("paleoignition_logo_white.png", width=500)

# with st.sidebar:
#   selected = option_menu(
#     menu_title = "Main Menu",
#     options = ["Home","Lightning Plotter","Contact"],
#     icons = ["house","lightning","envelope"],
#     menu_icon = "cast",
#     default_index = 0,

#   )