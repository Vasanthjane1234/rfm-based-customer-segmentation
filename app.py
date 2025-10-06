import streamlit as st
import pandas as pd

# Load RFM data
rfm = pd.read_csv('rfm_segments_output.csv')

# Sidebar filters
selected_segment = st.sidebar.selectbox('Select Segment', rfm['segment'].unique())

# Filter data
filtered_df = rfm[rfm['segment'] == selected_segment]

st.title('Customer Segmentation Dashboard')
st.write(f"Showing data for segment: {selected_segment}")
st.dataframe(filtered_df)
