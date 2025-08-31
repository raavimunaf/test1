-- Sybase Database Setup Script
-- Connect to Sybase using: isql -U sa -P password -S localhost:5000

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT * FROM master.dbo.sysdatabases WHERE name = 'testdb')
BEGIN
    CREATE DATABASE testdb
END
GO

-- Use the test database
USE testdb
GO

-- Create employees table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='employees' AND xtype='U')
BEGIN
    CREATE TABLE employees (
        id int primary key,
        name varchar(100),
        dept varchar(50),
        salary numeric(10,2),
        updated_at datetime default getdate()
    )
END
GO

-- Insert sample data if table is empty
IF NOT EXISTS (SELECT * FROM employees WHERE id = 1)
BEGIN
    INSERT INTO employees (id, name, dept, salary) VALUES
    (1, 'Alice', 'HR', 55000.00),
    (2, 'Bob', 'IT', 75000.00),
    (3, 'Charlie', 'Finance', 62000.00)
END
GO

-- Verify the setup
SELECT 'Database setup completed successfully' as status
SELECT COUNT(*) as employee_count FROM employees
SELECT * FROM employees
GO 