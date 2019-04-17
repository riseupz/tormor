CREATE TABLE customer(
    name text NOT NULL,
    CONSTRAINT customer_pk PRIMARY KEY(name));
INSERT INTO customer(name)
    VALUES('Customer1'); 
INSERT INTO customer(name)
    VALUES('Customer2');
INSERT INTO customer(name)
    VALUES('Customer3');