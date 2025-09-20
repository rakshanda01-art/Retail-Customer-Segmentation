-- Dimension tables
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name NVARCHAR(100),
    signup_date DATE
);

CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name NVARCHAR(100),
    unit_price DECIMAL(10,2)
);

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY IDENTITY(1,1),
    full_date DATE,
    year INT,
    month INT,
    day INT
);

-- Fact table
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);
