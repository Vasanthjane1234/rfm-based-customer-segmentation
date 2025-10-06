import streamlit as st
import pandas as pd

# Load precomputed RFM with clusters
rfm = pd.read_csv('rfm_segments_output.csv')

st.title("Customer Segmentation Dashboard with Clusters")

# Sidebar for cluster selection
clusters = rfm['cluster'].unique()
selected_cluster = st.sidebar.selectbox('Select Cluster', clusters)

# Filter data based on selected cluster
filtered_data = rfm[rfm['cluster'] == selected_cluster]

st.subheader(f"Cluster {selected_cluster} Summary")

# Display summary stats for the cluster
cluster_summary = filtered_data[['recency', 'frequency', 'monetary']].describe()
st.write(cluster_summary)

# Show raw data if needed
if st.checkbox('Show raw data'):
    st.write(filtered_data)

# Optional: Display scatter plot
st.subheader("Recency vs Frequency")
chart_data = filtered_data[['recency', 'frequency', 'monetary']]
st.scatter_chart(chart_data)

