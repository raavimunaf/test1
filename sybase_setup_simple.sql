-- Simple Sybase Setup Script
-- Run this directly in Sybase using: isql -U sa -P password -S localhost:5000

-- Switch to master database (if not already there)
USE master
GO

-- Create employees table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'employees')
BEGIN
    CREATE TABLE employees (
        id int primary key,
        name varchar(100),
        dept varchar(50),
        salary numeric(10,2),
        updated_at datetime default getdate()
    )
    PRINT 'Employees table created successfully'
END
ELSE
BEGIN
    PRINT 'Employees table already exists'
END
GO

-- Check if table has data
IF NOT EXISTS (SELECT * FROM employees WHERE id = 1)
BEGIN
    INSERT INTO employees (id, name, dept, salary) VALUES
    (1, 'Alice', 'HR', 55000.00),
    (2, 'Bob', 'IT', 75000.00),
    (3, 'Charlie', 'Finance', 62000.00)
    PRINT 'Sample data inserted successfully'
END
ELSE
BEGIN
    PRINT 'Employees table already has data'
END
GO

-- Verify the setup
SELECT 'Setup completed successfully' as status
SELECT COUNT(*) as employee_count FROM employees
SELECT * FROM employees
GO




