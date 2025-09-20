# 🛍️ Retail Customer Segmentation (SQL + Python + Power BI)

This project is an **end-to-end customer segmentation pipeline** using:
- **SQL Server** for data storage and feature engineering
- **Python (Pandas, Scikit-learn)** for clustering (KMeans)
- **Power BI** for visualization of customer segments

---

## 🔹 Project Workflow

1. **Data Generation (Python)**
   - Synthetic retail data (customers, products, sales) created with Faker.
   - `generate_dataset.py` generates a CSV file with realistic transactions.

2. **Data Warehousing (SQL Server)**
   - Tables created: `dim_customer`, `dim_product`, `dim_date`, `fact_sales`.
   - `views.sql` builds `customer_features_vw` with features:
     - Frequency
     - Monetary
     - Recency
     - Tenure
     - Avg Order Value
     - Return Rate
     - % Online Orders

3. **Machine Learning (Python)**
   - Features loaded from SQL → Preprocessing (scaling, log-transform).
   - **KMeans clustering** applied.
   - Elbow method + silhouette score used to choose `k`.
   - Customers segmented into:
     - 🏆 Champions → High sales, loyal, frequent
     - 🤝 Loyal → Stable orders, decent spend
     - 🌱 Potential → New customers with low frequency but high tenure
     - ⚠️ At Risk → High recency days, declining orders
   - Results saved back to SQL table `customer_segments`.

4. **Visualization (Power BI)**
   - Power BI dashboard built 
     


