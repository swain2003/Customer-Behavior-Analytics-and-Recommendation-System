CREATE DATABASE IF NOT EXISTS customer_behavior;
USE customer_behavior;

CREATE TABLE IF NOT EXISTS transactions_processed (
    customer_id INT NOT NULL,
    transaction_id VARCHAR(32) PRIMARY KEY,
    product_category VARCHAR(64) NOT NULL,
    purchase_amount DECIMAL(10, 2) NOT NULL,
    purchase_date DATE NOT NULL,
    payment_method VARCHAR(32) NOT NULL,
    city VARCHAR(64) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    age INT NOT NULL,
    quantity INT NOT NULL,
    frequency INT NOT NULL,
    recency INT NOT NULL,
    revenue DECIMAL(12, 2) NOT NULL,
    month VARCHAR(16) NOT NULL,
    age_group VARCHAR(16)
);
