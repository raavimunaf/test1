-- Sybase Database Setup Script
-- Connect to Sybase using: isql -U sa -P StrongPass1 -S localhost:5000

-- Create database if it doesn't exist
IF NOT EXISTS (SELECT * FROM master.dbo.sysdatabases WHERE name = 'testdb')
BEGIN
    CREATE DATABASE testdb
    ON DEFAULT = 10
    LOG ON DEFAULT = 5
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
        name varchar(100) NOT NULL,
        dept varchar(50) NOT NULL,
        salary numeric(10,2) NOT NULL,
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

-- Verify data
SELECT * FROM employees
GO

-- Create index on updated_at for better incremental sync performance
IF NOT EXISTS (SELECT * FROM sysindexes WHERE name = 'idx_employees_updated_at')
BEGIN
    CREATE INDEX idx_employees_updated_at ON employees(updated_at)
END
GO

-- Show table structure
sp_help employees
GO 