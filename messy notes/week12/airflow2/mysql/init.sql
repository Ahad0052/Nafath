CREATE DATABASE IF NOT EXISTS gold_db;

USE gold_db;

CREATE TABLE IF NOT EXISTS gold_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50),
    price FLOAT,
    currency VARCHAR(20),
    timestamp DATETIME
);
