-- create and select the database
DROP DATABASE IF EXISTS LAB2;
CREATE DATABASE LAB2;
USE LAB2;

-- create the tables
CREATE TABLE authors (
  author_id         INT                 AUTO_INCREMENT  PRIMARY KEY,
  name              VARCHAR(100),
  birth_year        INT
);

CREATE TABLE books (
  book_id           INT                 AUTO_INCREMENT  PRIMARY KEY,
  title             VARCHAR(100),
  published_year    INT,
  author_id         INT,
  price             DECIMAL(10,2),
  copies_sold       INT,
  FOREIGN KEY (author_id) REFERENCES authors (author_id)
);

-- insert data into the database
INSERT INTO authors (name, birth_year) VALUES
('Alice Munro', 1931),
('Margaret Atwood', 1939),
('Michael Ondaatje', 1943);

INSERT INTO books (title, published_year, author_id, price, copies_sold) VALUES
('Dear Life', 2012, 1, 20.00, 500),
('The Handmaid\'s Tale', 1985, 2, 15.00, 2000),
('The English Patient', 1992, 3, 22.50, 1500);

-- 1.	UPDATE: Increase the price of books published before 2000 by 10%.
UPDATE books
SET price = 1.1 * price
WHERE published_year < 2000;

-- 2.	DELETE: Remove all books that have sold fewer than 500 copies.
DELETE FROM books
WHERE copies_sold < 500;

-- 3.	DISTINCT: List all unique publication years in the books table.
SELECT DISTINCT published_year
FROM books;

-- 4.	AGGREGATE FUNCTIONS: Calculate the total revenue (price * copies sold) for each author.
SELECT price, copies_sold, (price * copies_sold) AS total_revenue
FROM books;

-- 5.	SELF JOIN: Find pairs of authors who were born in the same year.
SELECT A.name, B.name
FROM authors A, authors B
WHERE A.birth_year = B.birth_year
AND A.author_id != B.author_id;

SELECT A.name, B.name
FROM authors A JOIN authors B
ON A.birth_year = B.birth_year
AND A.author_id != B.author_id;

-- 6.	UNION: Create a list of all author names and book titles together in one column.
SELECT name FROM authors
UNION
SELECT title FROM books;

-- 7.	HAVING: Show authors who have published more than one book.
SELECT name, COUNT(book_id) AS num_books
FROM authors AS A JOIN books AS B
ON A.author_id = B.author_id
GROUP BY name
HAVING num_books > 1;

-- 8.	EXISTS: List all authors who have sold at least one book with more than 1000 copies.
SELECT name
FROM authors AS a 
WHERE EXISTS (
  SELECT 1 
  FROM books AS b
  WHERE b.author_id = a.author_id 
  AND copies_sold > 1000
);

-- 9.	ANY/ALL: Identify books that have sold more copies than any book by 'Alice Munro'.
SELECT title
FROM books
WHERE copies_sold > ANY (
  SELECT copies_sold
  FROM books
  WHERE author_id IN
    (SELECT author_id
     FROM authors
     WHERE name = 'Alice Munro')
);

-- 10.	CASE: Categorize books into 'Low', 'Medium', and 'High' sellers based on copies sold (<500, 500-1500, >1500).
SELECT title, copies_sold,
    CASE
        WHEN copies_sold < 500 THEN 'Low'
        WHEN copies_sold BETWEEN 500 AND 1500 THEN 'Medium'
        ELSE 'Hight'
    END AS copies_sold_category
FROM books;

-- 11.	NULL Functions: Update all book prices to include a default price of $10 where price is NULL.
SELECT title, price, COALESCE(price, 10)
FROM books;

-- 12.	SUBQUERIES: Increase the price of books by 5% where the author is older than the average age of all authors.
UPDATE books 
SET price = price * 1.05
WHERE author_id IN 
  (SELECT author_id
   FROM authors 
   WHERE birth_year <
      (SELECT AVG(birth_year)
       FROM authors)
   );
   

SELECT *
FROM  authors;

SELECT *
FROM  books;