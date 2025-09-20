import pandas as pd
import numpy as np
import random
from faker import Faker

faker = Faker()

# Parameters
n_customers = 500
n_products = 200
n_regions = 20
n_transactions = 50000  # 50k transactions

# --- Dimension Tables ---

# Customers
segments = ["Consumer", "Corporate", "Home Office"]
dim_customer = pd.DataFrame({
    "customer_id": range(1, n_customers+1),
    "customer_name": [faker.name() for _ in range(n_customers)],
    "gender": np.random.choice(["Male", "Female"], n_customers),
    "age": np.random.randint(18, 65, n_customers),
    "segment": np.random.choice(segments, n_customers)
})

# Products
categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases"],
    "Technology": ["Phones", "Laptops", "Accessories"],
    "Office Supplies": ["Paper", "Binders", "Pens"]
}
product_rows = []
pid = 1
for cat, subs in categories.items():
    for sub in subs:
        for _ in range(20):  # 20 products per subcategory
            product_rows.append((pid, faker.word().capitalize()+" "+sub, cat, sub, round(np.random.uniform(5, 1000),2)))
            pid += 1
dim_product = pd.DataFrame(product_rows, columns=["product_id","product_name","category","sub_category","price"])

# Regions
countries = ["Pakistan","UAE","USA","UK","India"]
states = ["Sindh","Punjab","KPK","Balochistan","Dubai","Texas","California","London","Delhi"]
dim_region = pd.DataFrame({
    "region_id": range(1, n_regions+1),
    "region_name": [faker.city() for _ in range(n_regions)],
    "country": np.random.choice(countries, n_regions),
    "state": np.random.choice(states, n_regions),
    "city": [faker.city() for _ in range(n_regions)]
})

# Dates
date_range = pd.date_range("2018-01-01", "2024-12-31")
dim_date = pd.DataFrame({
    "date_id": range(1, len(date_range)+1),
    "full_date": date_range,
    "day": date_range.day,
    "month": date_range.month,
    "quarter": date_range.quarter,
    "year": date_range.year
})

# --- Fact Table ---
fact_rows = []
for i in range(1, n_transactions+1):
    cust = random.choice(dim_customer["customer_id"].tolist())
    prod = random.choice(dim_product["product_id"].tolist())
    reg = random.choice(dim_region["region_id"].tolist())
    date = random.choice(dim_date["date_id"].tolist())
    qty = np.random.randint(1, 10)
    price = dim_product.loc[dim_product["product_id"]==prod, "price"].values[0]
    discount = round(np.random.choice([0,0.05,0.1,0.2,0.3]),2)
    sales = qty * price * (1-discount)
    cost = sales * np.random.uniform(0.6,0.9)
    profit = sales - cost
    fact_rows.append((i, f"ORD{i:05}", cust, prod, reg, date, round(sales,2), round(profit,2), qty, discount))

fact_sales = pd.DataFrame(fact_rows, columns=[
    "sales_id","order_id","customer_id","product_id","region_id","date_id","sales","profit","quantity","discount"
])

# Save CSVs
dim_customer.to_csv("dim_customer.csv", index=False)
dim_product.to_csv("dim_product.csv", index=False)
dim_region.to_csv("dim_region.csv", index=False)
dim_date.to_csv("dim_date.csv", index=False)
fact_sales.to_csv("fact_sales.csv", index=False)

print("✅ Synthetic dataset generated with star schema CSVs!")
