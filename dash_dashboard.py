import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Load the RFM data
try:
    # Try to load the full dataset first, fallback to original if not available
    try:
        rfm = pd.read_csv('rfm_segments_output_full.csv')
        print(f"Loaded {len(rfm)} customer records (FULL DATASET)")
    except FileNotFoundError:
        rfm = pd.read_csv('rfm_segments_output.csv')
        print(f"Loaded {len(rfm)} customer records (ORIGINAL DATASET)")
except FileNotFoundError:
    print("Error: No RFM data files found. Please run the analysis first.")
    exit(1)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Customer Segmentation Dashboard"

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Customer Segmentation Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
        html.P("Interactive RFM Analysis and Customer Segmentation - Complete Dataset", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px'}),
        html.P(f"Analyzing {len(rfm)} customers across all transactions", 
               style={'textAlign': 'center', 'color': '#27ae60', 'fontSize': '16px', 'fontWeight': 'bold'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'marginBottom': '20px'}),
    
    # Controls Row
    html.Div([
        html.Div([
            html.Label("Select Segment:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='segment-dropdown',
                options=[{'label': 'All Segments', 'value': 'all'}] + 
                        [{'label': seg, 'value': seg} for seg in sorted(rfm['segment'].unique())],
                value='all',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Select Cluster:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='cluster-dropdown',
                options=[{'label': 'All Clusters', 'value': 'all'}] + 
                        [{'label': f'Cluster {i}', 'value': i} for i in sorted(rfm['cluster'].unique())],
                value='all',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Select Country:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': 'All Countries', 'value': 'all'}] + 
                        [{'label': country, 'value': country} for country in sorted(rfm['country'].unique())],
                value='all',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
    
    # Summary Cards
    html.Div([
        html.Div([
            html.H3(id='total-customers', style={'color': '#2c3e50', 'margin': '0'}),
            html.P("Total Customers", style={'color': '#7f8c8d', 'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#e8f5e8', 
                 'borderRadius': '10px', 'margin': '5px', 'flex': '1'}),
        
        html.Div([
            html.H3(id='avg-recency', style={'color': '#2c3e50', 'margin': '0'}),
            html.P("Avg Recency (days)", style={'color': '#7f8c8d', 'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#e8f4fd', 
                 'borderRadius': '10px', 'margin': '5px', 'flex': '1'}),
        
        html.Div([
            html.H3(id='avg-frequency', style={'color': '#2c3e50', 'margin': '0'}),
            html.P("Avg Frequency", style={'color': '#7f8c8d', 'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#fff3cd', 
                 'borderRadius': '10px', 'margin': '5px', 'flex': '1'}),
        
        html.Div([
            html.H3(id='avg-monetary', style={'color': '#2c3e50', 'margin': '0'}),
            html.P("Avg Monetary", style={'color': '#7f8c8d', 'margin': '0'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f8d7da', 
                 'borderRadius': '10px', 'margin': '5px', 'flex': '1'})
    ], style={'display': 'flex', 'marginBottom': '30px'}),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='segment-distribution')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='cluster-distribution')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='rfm-scatter')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='country-distribution')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # RFM Analysis Charts
    html.Div([
        html.Div([
            dcc.Graph(id='rfm-heatmap')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='monetary-distribution')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Data Table
    html.Div([
        html.H3("Customer Data", style={'textAlign': 'center', 'marginBottom': '20px'}),
        html.Div([
            html.Label("Show Raw Data:", style={'marginRight': '10px'}),
            dcc.Checklist(
                id='show-raw-data',
                options=[{'label': 'Display detailed customer data', 'value': 'show'}],
                value=[]
            )
        ], style={'marginBottom': '20px', 'textAlign': 'center'}),
        html.Div(id='data-table')
    ], style={'marginTop': '30px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'})
])

# Callback for updating summary cards
@app.callback(
    [Output('total-customers', 'children'),
     Output('avg-recency', 'children'),
     Output('avg-frequency', 'children'),
     Output('avg-monetary', 'children')],
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_summary_cards(selected_segment, selected_cluster, selected_country):
    # Filter data based on selections
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    total_customers = len(filtered_df)
    avg_recency = round(filtered_df['recency'].mean(), 1) if len(filtered_df) > 0 else 0
    avg_frequency = round(filtered_df['frequency'].mean(), 1) if len(filtered_df) > 0 else 0
    avg_monetary = round(filtered_df['monetary'].mean(), 0) if len(filtered_df) > 0 else 0
    
    return total_customers, avg_recency, avg_frequency, f"${avg_monetary:,.0f}"

# Callback for segment distribution chart
@app.callback(
    Output('segment-distribution', 'figure'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_segment_distribution(selected_segment, selected_cluster, selected_country):
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    segment_counts = filtered_df['segment'].value_counts()
    
    fig = px.bar(
        x=segment_counts.index, 
        y=segment_counts.values,
        title="Customer Segment Distribution",
        labels={'x': 'Segment', 'y': 'Number of Customers'},
        color=segment_counts.values,
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Callback for cluster distribution chart
@app.callback(
    Output('cluster-distribution', 'figure'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_cluster_distribution(selected_segment, selected_cluster, selected_country):
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    cluster_counts = filtered_df['cluster'].value_counts().sort_index()
    
    fig = px.pie(
        values=cluster_counts.values,
        names=[f'Cluster {i}' for i in cluster_counts.index],
        title="Customer Cluster Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Callback for RFM scatter plot
@app.callback(
    Output('rfm-scatter', 'figure'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_rfm_scatter(selected_segment, selected_cluster, selected_country):
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    fig = px.scatter(
        filtered_df,
        x='recency',
        y='frequency',
        size='monetary',
        color='segment',
        title="RFM Analysis: Recency vs Frequency (Bubble size = Monetary)",
        labels={'recency': 'Recency (days)', 'frequency': 'Frequency'},
        hover_data=['monetary', 'cluster']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Callback for country distribution
@app.callback(
    Output('country-distribution', 'figure'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_country_distribution(selected_segment, selected_cluster, selected_country):
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    country_counts = filtered_df['country'].value_counts()
    
    fig = px.bar(
        x=country_counts.index,
        y=country_counts.values,
        title="Customer Distribution by Country",
        labels={'x': 'Country', 'y': 'Number of Customers'},
        color=country_counts.values,
        color_continuous_scale='blues'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

# Callback for RFM heatmap
@app.callback(
    Output('rfm-heatmap', 'figure'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_rfm_heatmap(selected_segment, selected_cluster, selected_country):
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    # Create RFM score heatmap
    rfm_scores = filtered_df.groupby(['r', 'f']).agg({
        'm': 'mean',
        'id': 'count'
    }).reset_index()
    
    # Pivot for heatmap
    heatmap_data = rfm_scores.pivot(index='r', columns='f', values='m').fillna(0)
    
    fig = px.imshow(
        heatmap_data.values,
        x=[f'F{i}' for i in heatmap_data.columns],
        y=[f'R{i}' for i in heatmap_data.index],
        title="RFM Score Heatmap (Average Monetary Value)",
        color_continuous_scale='RdYlBu_r',
        aspect="auto"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Callback for monetary distribution
@app.callback(
    Output('monetary-distribution', 'figure'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_monetary_distribution(selected_segment, selected_cluster, selected_country):
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    fig = px.histogram(
        filtered_df,
        x='monetary',
        nbins=30,
        title="Monetary Value Distribution",
        labels={'monetary': 'Monetary Value', 'count': 'Number of Customers'},
        color_discrete_sequence=['#3498db']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

# Callback for data table
@app.callback(
    Output('data-table', 'children'),
    [Input('segment-dropdown', 'value'),
     Input('cluster-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('show-raw-data', 'value')]
)
def update_data_table(selected_segment, selected_cluster, selected_country, show_raw):
    if 'show' not in show_raw:
        return html.Div()
    
    # Filter data
    filtered_df = rfm.copy()
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    if selected_cluster != 'all':
        filtered_df = filtered_df[filtered_df['cluster'] == selected_cluster]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    
    # Create data table
    table = dash_table.DataTable(
        data=filtered_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in filtered_df.columns],
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#2c3e50', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            }
        ],
        page_size=20,
        sort_action="native",
        filter_action="native"
    )
    
    return table

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
