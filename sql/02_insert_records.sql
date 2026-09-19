-- Project 3: The Data Warehouse
-- Inserts dummy records to test persistence

-- Single row insert
INSERT INTO Interns (InternID, FirstName, LastName, Email, Role)
VALUES (1, 'John', 'Doe', 'jdoe@decodelabs.com', 'Cloud Intern');

-- Multi-row insert (batch)
INSERT INTO Interns (InternID, FirstName, LastName, Email, Role)
VALUES
    (2, 'Jane', 'Smith', 'jsmith@decodelabs.com', 'Backend Intern'),
    (3, 'Conan', 'O''Leary', 'coleary@decodelabs.com', 'DevOps Intern'),
    (4, 'Ayesha', 'Khan', 'akhan@decodelabs.com', 'Cloud Intern'),
    (5, 'Bilal', 'Ahmed', 'bahmed@decodelabs.com', 'Data Intern');

-- Note: apostrophes inside a string (O'Leary) are escaped with a second
-- single quote -> 'O''Leary'
