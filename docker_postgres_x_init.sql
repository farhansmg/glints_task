CREATE TABLE IF NOT EXISTS sales
(
    id     INTEGER PRIMARY KEY,
    creation_date  VARCHAR(1024),
    sale_value INTEGER
);

INSERT INTO sales (id, creation_date, sale_value)
VALUES (1, '12-12-21', 1000);

INSERT INTO sales (id, creation_date, sale_value)
VALUES (2, '13-12-21', 2000);

INSERT INTO sales (id, creation_date, sale_value)
VALUES (3, '14-12-21', 3000);

INSERT INTO sales (id, creation_date, sale_value)
VALUES (4, '15-12-21', 4000);

INSERT INTO sales (id, creation_date, sale_value)
VALUES (5, '16-12-21', 5000);