# For any help we can follow streamlit documentation
# https://docs.streamlit.io/

# To run the app, open terminal and run the following command
# streamlit run app.py


#imports
import streamlit as st
import pandas as pd
import os
# Convert Files into Binary and keep them safe temporarily in memory
from io import BytesIO

# Set up our Streamlit app

st.set_page_config(page_title="📊Data Sweeper",layout='wide')
st.title("📊Data Sweeper")
st.write("Transform Your Files Between CSV and Excel Formats with built-in Data Cleaning and Visualization!")


