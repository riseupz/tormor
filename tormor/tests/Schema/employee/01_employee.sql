CREATE TABLE employee(
    name text NOT NULL,
    CONSTRAINT employee_pk PRIMARY KEY(name));
INSERT INTO employee(name)
    VALUES('Employee1'); 
INSERT INTO employee(name)
    VALUES('Employee2');
INSERT INTO employee(name)
    VALUES('Employee3');