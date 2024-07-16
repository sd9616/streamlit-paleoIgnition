import streamlit as st 
from streamlit_option_menu import option_menu

# st.title('Lightning App')


# st.sidebar.success("Select a demo above.")

col1, col2 = st.columns(2)

with col1: 
    st.write("# Welcome to PaleoIgnition! 👋")
    # st.markdown(
    #     """
    #     PaleoIgnition is an app built for paleofire researchers to use
    
    #     """)

with col2: 
    st.image("paleoignition_logo_white.png", width=600)

# with st.sidebar:
#   selected = option_menu(
#     menu_title = "Main Menu",
#     options = ["Home","Lightning Plotter","Contact"],
#     icons = ["house","lightning","envelope"],
#     menu_icon = "cast",
#     default_index = 0,

#   )