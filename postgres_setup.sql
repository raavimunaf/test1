-- PostgreSQL Database Setup Script
-- Connect to PostgreSQL using: psql -h localhost -U postgres -d postgres

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE testdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'testdb')\gexec

-- Connect to the test database
\c testdb

-- Create employees table if it doesn't exist
CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept VARCHAR(50) NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index on updated_at for better incremental sync performance
CREATE INDEX IF NOT EXISTS idx_employees_updated_at ON employees(updated_at);

-- Show table structure
\d employees

-- Verify table is empty (data will be migrated from Sybase)
SELECT COUNT(*) as row_count FROM employees; 