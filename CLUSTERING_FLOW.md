# 🔄 Clustering Algorithm Flow

## 📊 **K-Means Clustering Process**

```
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER DATA (1000)                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Recency   │ │  Frequency  │ │  Monetary   │           │
│  │  (days)     │ │  (count)    │ │  (amount)   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                DATA PREPROCESSING                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            StandardScaler()                          │   │
│  │  • Normalize Recency (0-1 scale)                     │   │
│  │  • Normalize Frequency (0-1 scale)                   │   │
│  │  • Normalize Monetary (0-1 scale)                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                K-MEANS CLUSTERING                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  KMeans(n_clusters=4, random_state=42)             │   │
│  │                                                     │   │
│  │  Step 1: Initialize 4 random centers                │   │
│  │  Step 2: Assign customers to nearest center         │   │
│  │  Step 3: Update cluster centers                    │   │
│  │  Step 4: Repeat until convergence                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLUSTER RESULTS                          │
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  │  CLUSTER 0  │ │  CLUSTER 1  │ │  CLUSTER 2  │ │  CLUSTER 3  │
│  │             │ │             │ │             │ │             │
│  │ 236 customers│ │ 277 customers│ │ 263 customers│ │ 224 customers│
│  │             │ │             │ │             │ │             │
│  │ High Value  │ │ Recent High │ │ Low Value   │ │ Recent Low  │
│  │ Low Recency │ │ Spenders    │ │ Low Recency │ │ Spenders    │
│  │             │ │             │ │             │ │             │
│  │ $3,875 avg  │ │ $3,650 avg  │ │ $1,327 avg  │ │ $1,173 avg  │
│  │ 754.9 days  │ │ 243.3 days  │ │ 747.4 days  │ │ 260.7 days  │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                DASHBOARD VISUALIZATION                     │
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Pie Chart   │ │ Scatter Plot│ │ Heatmap     │           │
│  │ Distribution│ │ RFM Analysis│ │ Score Pattern│          │
│  │             │ │             │ │             │           │
│  │ Interactive│ │ Bubble Size │ │ Color Coded │           │
│  │ Legend      │ │ = Monetary │ │ by Cluster  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              FILTER INTEGRATION                    │   │
│  │  • Cluster Dropdown Filter                         │   │
│  │  • Real-time Chart Updates                         │   │
│  │  • Combined with Segment & Country Filters        │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 **Algorithm Details:**

### **K-Means Parameters:**
- **n_clusters**: 4 (optimal for business interpretation)
- **random_state**: 42 (reproducible results)
- **max_iter**: 300 (default)
- **n_init**: 10 (default)

### **Feature Scaling:**
```python
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary']])
```

### **Clustering:**
```python
kmeans = KMeans(n_clusters=4, random_state=42)
rfm['cluster'] = kmeans.fit_predict(rfm_scaled)
```

## 📈 **Business Value:**

### **Cluster 0 - "High Value, Low Recency" (236 customers)**
- **Strategy**: Win-back campaigns
- **Action**: Premium offers, personalized outreach

### **Cluster 1 - "Recent High Spenders" (277 customers)**
- **Strategy**: Retention and upselling
- **Action**: Loyalty programs, cross-selling

### **Cluster 2 - "Low Value, Low Recency" (263 customers)**
- **Strategy**: Cost-effective reactivation
- **Action**: Minimal effort, basic offers

### **Cluster 3 - "Recent Low Spenders" (224 customers)**
- **Strategy**: Value building
- **Action**: Engagement campaigns, education

---

## 🎉 **Result:**
**K-Means successfully identified 4 distinct customer behavioral patterns** that complement RFM segmentation for comprehensive customer insights!
