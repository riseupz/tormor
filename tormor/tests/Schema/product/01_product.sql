CREATE TABLE product(
    name text NOT NULL,
    CONSTRAINT product_pk PRIMARY KEY(name));
INSERT INTO product(name)
    VALUES('Product1'); 