#!/usr/bin/env python3
"""
Generate RFM analysis for ALL customer records (not just last 365 days)
This will create a comprehensive customer segmentation with all 1000 transactions
"""

import pandas as pd
import numpy as np
from datetime import timedelta
import math
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def load_and_prepare_data():
    """Load and prepare the customer transaction data"""
    print("Loading customer transaction data...")
    
    # Load the original transaction data
    df = pd.read_csv('customer_transactions.csv')
    
    # Convert date column to datetime
    df['Sale_Date'] = pd.to_datetime(df['Sale_Date'], errors='coerce')
    
    # Rename columns for RFM processing
    df.rename(columns={
        'Customer_ID': 'id',
        'Sales_Amount': 'monetary',
        'Quantity_Sold': 'units',
        'Sale_Date': 'date',
        'Region': 'country'
    }, inplace=True)
    
    # Drop any invalid dates
    df = df.dropna(subset=['date'])
    
    print(f"Loaded {len(df)} transactions")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Unique customers: {df['id'].nunique()}")
    
    return df

def calculate_rfm_metrics(df):
    """Calculate RFM metrics for all customers"""
    print("Calculating RFM metrics...")
    
    # Create unique customer identifier
    df['id+'] = df['country'].astype(str) + df['id'].astype(str)
    
    # Reference date is the latest transaction date
    NOW = df['date'].max() + timedelta(days=1)
    
    # Calculate days since last purchase for each transaction
    df['days_since_purchase'] = df['date'].apply(lambda x: (NOW - x).days)
    
    # Aggregation for RFM metrics
    agg_funcs = {
        'days_since_purchase': 'min',  # Recency: most recent purchase
        'date': 'count'                # Frequency: number of purchases
    }
    
    # Group by customer to get RFM metrics
    rfm = df.groupby(['id', 'id+', 'country']).agg(agg_funcs).reset_index()
    
    # Rename columns
    rfm.rename(columns={
        'days_since_purchase': 'recency',
        'date': 'frequency'
    }, inplace=True)
    
    # Calculate monetary value per customer
    monetary = df.groupby('id+')['monetary'].sum()
    rfm = rfm.merge(monetary, left_on='id+', right_index=True)
    
    # Drop the temporary id+ column
    rfm.drop(columns=['id+'], inplace=True)
    
    print(f"RFM analysis completed for {len(rfm)} unique customers")
    return rfm

def calculate_rfm_scores(rfm):
    """Calculate RFM scores (1-5 scale)"""
    print("Calculating RFM scores...")
    
    # Compute quintiles for R, F, and M
    quintiles = rfm[['recency', 'frequency', 'monetary']].quantile([0.2, 0.4, 0.6, 0.8]).to_dict()
    
    # Define scoring functions
    def r_score(x):
        if x <= quintiles['recency'][0.2]:
            return 5
        elif x <= quintiles['recency'][0.4]:
            return 4
        elif x <= quintiles['recency'][0.6]:
            return 3
        elif x <= quintiles['recency'][0.8]:
            return 2
        else:
            return 1

    def fm_score(x, col):
        if x <= quintiles[col][0.2]:
            return 1
        elif x <= quintiles[col][0.4]:
            return 2
        elif x <= quintiles[col][0.6]:
            return 3
        elif x <= quintiles[col][0.8]:
            return 4
        else:
            return 5

    # Apply scoring
    rfm['r'] = rfm['recency'].apply(r_score)
    rfm['f'] = rfm['frequency'].apply(lambda x: fm_score(x, 'frequency'))
    rfm['m'] = rfm['monetary'].apply(lambda x: fm_score(x, 'monetary'))
    
    # Create combined RFM score
    rfm['rfm_score'] = rfm['r'].map(str) + rfm['f'].map(str) + rfm['m'].map(str)
    
    return rfm

def assign_customer_segments(rfm):
    """Assign customer segments based on RFM scores"""
    print("Assigning customer segments...")
    
    # Calculate combined FM score
    rfm['fm'] = ((rfm['f'] + rfm['m']) / 2).apply(math.trunc)
    
    # Segment mapping
    segment_map = {
        r'22': 'hibernating',
        r'[1-2][1-2]': 'lost',
        r'15': "can't lose",
        r'[1-2][3-5]': 'at risk',
        r'3[1-2]': 'about to sleep',
        r'33': 'need attention',
        r'55': 'champions',
        r'[3-5][4-5]': 'loyal customers',
        r'41': 'promising',
        r'51': 'new customers',
        r'[4-5][2-3]': 'potential loyalists'
    }
    
    # Assign segments
    rfm['segment'] = (rfm['r'].astype(str) + rfm['fm'].astype(str)).replace(segment_map, regex=True)
    
    return rfm

def perform_clustering(rfm):
    """Perform K-means clustering on RFM data"""
    print("Performing K-means clustering...")
    
    # Scale RFM features
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary']])
    
    # Use 4 clusters (you can adjust this)
    kmeans = KMeans(n_clusters=4, random_state=42)
    rfm['cluster'] = kmeans.fit_predict(rfm_scaled)
    
    return rfm

def generate_summary_stats(rfm):
    """Generate summary statistics"""
    print("Generating summary statistics...")
    
    # Segment summary
    segment_summary = rfm.groupby('segment').agg({
        'recency': 'mean',
        'frequency': 'mean', 
        'monetary': ['mean', 'sum'],
        'id': 'count'
    }).rename(columns={'id': 'count'})
    
    print("\n=== SEGMENT SUMMARY ===")
    print(segment_summary)
    
    # Cluster summary
    cluster_summary = rfm.groupby('cluster').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean',
        'id': 'count'
    }).rename(columns={'id': 'count'})
    
    print("\n=== CLUSTER SUMMARY ===")
    print(cluster_summary)
    
    return segment_summary, cluster_summary

def main():
    """Main function to generate complete RFM analysis"""
    print("=" * 60)
    print("COMPREHENSIVE CUSTOMER SEGMENTATION ANALYSIS")
    print("Processing ALL customer records (no time filter)")
    print("=" * 60)
    
    # Step 1: Load and prepare data
    df = load_and_prepare_data()
    
    # Step 2: Calculate RFM metrics
    rfm = calculate_rfm_metrics(df)
    
    # Step 3: Calculate RFM scores
    rfm = calculate_rfm_scores(rfm)
    
    # Step 4: Assign customer segments
    rfm = assign_customer_segments(rfm)
    
    # Step 5: Perform clustering
    rfm = perform_clustering(rfm)
    
    # Step 6: Generate summary statistics
    segment_summary, cluster_summary = generate_summary_stats(rfm)
    
    # Step 7: Save results
    print("\nSaving results...")
    rfm.to_csv('rfm_segments_output_full.csv', index=False)
    segment_summary.to_csv('rfm_segment_summary_full.csv')
    
    print(f"\n✅ Analysis complete!")
    print(f"📊 Processed {len(rfm)} unique customers")
    print(f"📁 Saved: rfm_segments_output_full.csv")
    print(f"📁 Saved: rfm_segment_summary_full.csv")
    
    # Display segment distribution
    print(f"\n=== SEGMENT DISTRIBUTION ===")
    segment_counts = rfm['segment'].value_counts()
    for segment, count in segment_counts.items():
        percentage = (count / len(rfm)) * 100
        print(f"{segment:20}: {count:3d} customers ({percentage:5.1f}%)")
    
    return rfm

if __name__ == "__main__":
    rfm_data = main()
