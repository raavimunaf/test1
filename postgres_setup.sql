-- PostgreSQL Database Setup Script
-- This script creates the sample database and table for migration testing

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE testdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testdb')\gexec

-- Connect to the test database
\c testdb

-- Create employees table if it doesn't exist
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    dept VARCHAR(50),
    salary NUMERIC(10,2),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index on updated_at for better incremental sync performance
CREATE INDEX IF NOT EXISTS idx_employees_updated_at ON employees(updated_at);

-- Verify the setup
SELECT 'Database setup completed successfully' as status;
SELECT COUNT(*) as employee_count FROM employees;
SELECT * FROM employees; 