-- Create the database
CREATE DATABASE IF NOT EXISTS geeklogin;

-- Use the newly created database
USE geeklogin;

-- Create the accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
);
