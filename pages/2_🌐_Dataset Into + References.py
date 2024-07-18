import streamlit as st 


st.markdown("""

## 

## Dataset Info

The models we used are TraCE, FAMOUS, and LOVECLIM 

We parameterize lightning from paleoclimate model data using the function Lighting~=CONCLD x PRECIP (mm/day)

We considered time range from 21 kaBP to present We have converted each models time variable to the unit kaBP.  
## References

Community Climate System Model (CCSM3) and CESM1.2 (Liu et al., 2009; letter of collaboration: Bette Otto-Bliesner) \n
FAst Met Office/UK Universities Simulator (FAMOUS; Smith and Gregory, 2012) \n
Loch-Vecode-Ecbilt-Clio-Agism Model (LOVECLIM; Timm and Timmermann, 2007) \n 

Link to the fire reconstruction website, reference and description
Global Paleofire Database
https://www.paleofire.org/index.php?p=CDA/index&gcd_menu=CDA


""")