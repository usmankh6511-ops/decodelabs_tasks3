-- Project 3: The Data Warehouse
-- Creates the Interns table with proper constraints

CREATE TABLE Interns (
    InternID   INT PRIMARY KEY,
    FirstName  VARCHAR(50) NOT NULL,
    LastName   VARCHAR(50) NOT NULL,
    Email      VARCHAR(100) UNIQUE NOT NULL,
    Role       VARCHAR(50) NOT NULL
);

-- Notes:
-- PRIMARY KEY  -> InternID uniquely identifies each row, no duplicates
-- UNIQUE       -> Email can't repeat across interns
-- NOT NULL     -> these fields can never be left empty
