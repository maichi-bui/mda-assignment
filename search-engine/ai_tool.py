import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import os
import matplotlib.pyplot as plt
import os
os.chdir("C:/Users/lu/Desktop/KUL semester2/mda/EngineDashboard")

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def app():
    st.title("Welcome to the AI tool Page")
    st.write("This is the AI tool section.")