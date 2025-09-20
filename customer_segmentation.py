import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pyodbc
import joblib

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=RetailDW;"
    "Trusted_Connection=yes;"
)
cnxn = pyodbc.connect(conn_str)
query = "SELECT * FROM dbo.customer_features_vw;"  # view with names
df = pd.read_sql(query, cnxn)
cnxn.close()

print(df.shape)
print(df.head())

features = [
    'frequency','monetary','avg_order_value','avg_discount',
    'return_rate','pct_online','recency_days','tenure_days','avg_inter_order_days'
]
X = df[features].copy()

X['avg_inter_order_days'].fillna(X['avg_inter_order_days'].median(), inplace=True)

X['monetary_log'] = np.log1p(X['monetary'])
X['avg_order_value_log'] = np.log1p(X['avg_order_value'])

X2 = X.drop(['monetary','avg_order_value'], axis=1)


for col in X2.columns:
    upper = X2[col].quantile(0.99)
    lower = X2[col].quantile(0.01)
    X2[col] = X2[col].clip(lower, upper)

    
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X2)


pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

inertia = []
sil_scores = []
K_range = range(2,9)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertia.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))

    

    
plt.figure()
plt.plot(list(K_range), inertia, marker='o')
plt.title('Elbow: Inertia vs K')
plt.xlabel('k')
plt.ylabel('inertia')
plt.show()

plt.figure()
plt.plot(list(K_range), sil_scores, marker='o')
plt.title('Silhouette Score vs K')
plt.xlabel('k')
plt.ylabel('silhouette_score')
plt.show()


k_final = 4 
km = KMeans(n_clusters=k_final, random_state=42, n_init=20)
df['cluster'] = km.fit_predict(X_scaled)

summary = df.groupby('cluster')[features].agg(['count','mean','median']).round(2)
print(summary)

cluster_stats = df.groupby('cluster').agg({'monetary':'mean','frequency':'mean'}).reset_index()
cluster_stats = cluster_stats.sort_values(['monetary','frequency'], ascending=False).reset_index(drop=True)

mapping = {}
labels_sorted = cluster_stats['cluster'].tolist()
names = ['Champions','Loyal','Potential','At_Risk']  # adjust length to k_final
for i, cl in enumerate(labels_sorted):
    mapping[cl] = names[i] if i < len(names) else f"Segment_{i}"

df['segment'] = df['cluster'].map(mapping)

import sqlalchemy
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=" + pyodbc.connect(conn_str).getinfo(pyodbc.SQL_DRIVER_NAME))
# create a small df to save
out = df[['customer_id','customer_name','cluster','segment']]
out.to_sql('customer_segments', con=engine, if_exists='replace', index=False)

joblib.dump(km, 'kmeans_model.joblib')
joblib.dump(scaler, 'scaler.joblib')
joblib.dump(pca, 'pca.joblib')

print("Segmentation done. Saved customer_segments table and model files.")


import urllib
import sqlalchemy

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=RetailDW;"
    "Trusted_Connection=yes;"
)

# URL encode the connection string for SQLAlchemy
conn_url = urllib.parse.quote_plus(conn_str)

engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn_url)

out = df[['customer_id','customer_name','cluster','segment']]
out.to_sql('customer_segments', con=engine, if_exists='replace', index=False)


import joblib

model = joblib.load("kmeans_model.joblib")


print("Cluster centers:\n", model.cluster_centers_)
print("Number of clusters:", model.n_clusters)
print("Labels:\n", model.labels_)
print("Inertia:", model.inertia_)