# 🐍 Week 6 — SQL, Database Normalization & Advanced Queries
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Mail Order Database Project](#1-mail-order-database-project)
2. [Normal Forms & Normalization](#2-normal-forms--normalization)
3. [SQL Language Categories](#3-sql-language-categories)
4. [SQL Data Types](#4-sql-data-types)
5. [DDL — Data Definition Language](#5-ddl--data-definition-language)
6. [DML — Data Manipulation Language](#6-dml--data-manipulation-language)
7. [DCL & TCL](#7-dcl--tcl)
8. [Constraints in MySQL](#8-constraints-in-mysql)
9. [Advanced SELECT Queries](#9-advanced-select-queries)
10. [Subqueries & Set Operations](#10-subqueries--set-operations)
11. [Aggregate Functions](#11-aggregate-functions)
12. [JOINs](#12-joins)
13. [Movie Database — Full Schema Example](#13-movie-database--full-schema-example)
14. [Notes & Tasks](#14-notes--tasks)

---

## 1. Mail Order Database Project

> **Project brief:** Design a MAIL_ORDER database where employees take orders for parts from customers.

### Requirements Summary
- **Employees** — identified by unique employee number, first name, last name, and Zip Code
- **Customers** — identified by unique customer number, first name, last name, and Zip Code
- **Parts** — identified by unique part number, part name, price, and quantity in stock
- **Orders** — each order has a unique order number, is placed by a customer, and taken by an employee
  - Contains specified quantities of one or more parts
  - Has a date of receipt, expected ship date, and actual ship date

> 💡 Data will be **synthetic** (AI-generated). Start by writing an SRS (Software Requirements Specification) before designing the ERD.

---

## 2. Normal Forms & Normalization

> **Normalization** improves data efficiency, consistency, and accuracy by eliminating redundancy and bad dependencies.

### Views (Virtual Data)
```sql
-- A VIEW is virtual data derived from the database — like the output of a query, but saved
CREATE VIEW actor_ages AS
SELECT name1, dob, (YEAR(CURDATE()) - YEAR(dob)) AS age FROM actor;
```

### The Three Normal Forms

| Form | Rule |
|------|------|
| **1NF** | Each cell contains only one value (no multi-valued cells) |
| **2NF** | Already in 1NF + no partial dependency — every column depends on the full primary key |
| **3NF** | Already in 2NF + no transitive dependency — non-key columns don't depend on other non-key columns |

> 📌 Reference: [DB Normalization Example](https://mebrahimii.github.io/comp440-fall2020/lecture/week_13/DB%20Normalization%20Example.pdf)

---

## 3. SQL Language Categories

```
SQL
├── DDL  — Data Definition Language    → CREATE, ALTER, DROP
├── DML  — Data Manipulation Language  → INSERT, UPDATE, DELETE, SELECT
├── DCL  — Data Control Language       → GRANT, REVOKE
└── TCL  — Transaction Control Language → COMMIT, ROLLBACK, SAVEPOINT
```

> ⚠️ To use TCL (rollback, savepoint), you must be inside a transaction — not using auto-commit.

### SQL Syntax Rules
- SQL is **not case-sensitive**
- Statements end with `;`
- Can span multiple lines — indentation is for readability only
- Comments use `--`

---

## 4. SQL Data Types

| Type | Description |
|------|-------------|
| `VARCHAR(n)` | Variable-length string up to n characters |
| `CHAR(n)` | Fixed-length string |
| `INT` | Integer |
| `DECIMAL` | Decimal number (can be generated/computed) |
| `DATE` | Date value (YYYY-MM-DD) |
| `YEAR` | Year value |
| `ENUM` | One value from a defined list |
| `SET` | One or more values from a defined list |

### Computed Column
```sql
-- Generated (derived) column — always computed, stored on disk
newcol DECIMAL GENERATED ALWAYS AS (col1 + col2) STORED
```

---

## 5. DDL — Data Definition Language

### CREATE
```sql
DROP DATABASE IF EXISTS MOVIE_DB;
CREATE DATABASE MOVIE_DB;
USE MOVIE_DB;

CREATE TABLE users (
    status VARCHAR(20) DEFAULT 'active'
);

-- With named constraint
CREATE TABLE actor (
    actor_id INT PRIMARY KEY,
    age      INT,
    name1    VARCHAR(50),
    dob      DATE,
    CONSTRAINT c CHECK (age > 0)
);
```

### ALTER
```sql
-- Add a column
ALTER TABLE Moviec ADD COLUMN duration INT;
ALTER TABLE Moviec ADD COLUMN year1 YEAR;

-- Modify a column
ALTER TABLE actor MODIFY actor_id INT NOT NULL;
ALTER TABLE actor MODIFY actor_id INT AUTO_INCREMENT;

-- Add a constraint
ALTER TABLE Moviec ADD CONSTRAINT con UNIQUE(title);
ALTER TABLE actor ADD CONSTRAINT c CHECK (age > 0);

-- Add a foreign key
ALTER TABLE Moviec
  ADD CONSTRAINT fk_prod
  FOREIGN KEY (PID) REFERENCES PROD(P_ID) ON DELETE CASCADE;

-- Add an index
ALTER TABLE actor ADD INDEX idx_name (age);

-- Rename a table
RENAME TABLE old_name TO new_name;
```

### DROP vs TRUNCATE vs DELETE
| Command | Description | Reversible? |
|---------|-------------|-------------|
| `DROP TABLE name` | Deletes table structure and data permanently | ❌ |
| `TRUNCATE TABLE name` | Deletes all rows permanently — no WHERE | ❌ |
| `DELETE FROM name` | Deletes rows — can use WHERE, can ROLLBACK | ✅ |

---

## 6. DML — Data Manipulation Language

### INSERT
```sql
-- Without specifying columns (must match column order exactly)
INSERT INTO prod VALUES (100, 'Netflix', 'USA');

-- Explicit column names (safer, order-independent)
INSERT INTO prod (P_ID, PNAME, ADDRESS) VALUES (101, 'Amazon Prime', 'USA');

-- Multiple rows at once
INSERT INTO director VALUES
    (301, 'Steven Spielberg', '1960-12-01', 'Direct only'),
    (302, 'Christopher Nolan', '1970-07-30', 'Direct only');
```

### UPDATE
```sql
UPDATE Moviec SET duration = 120 WHERE M_ID = 500;
UPDATE Moviec SET year1 = 2014 WHERE M_ID = 500;
```

### SELECT
```sql
SELECT * FROM actor;
SELECT DISTINCT age, name1 FROM actor;
SELECT * FROM moviec LIMIT 5;
```

### DELETE
```sql
DELETE FROM actor WHERE actor_id = 201;   -- reversible with ROLLBACK
```

---

## 7. DCL & TCL

```sql
-- DCL
GRANT SELECT ON MOVIE_DB.* TO 'user'@'localhost';
REVOKE SELECT ON MOVIE_DB.* FROM 'user'@'localhost';

-- TCL
SAVEPOINT before_update;
UPDATE actor SET age = 35 WHERE actor_id = 201;
ROLLBACK TO before_update;   -- undo back to savepoint
COMMIT;                       -- make changes permanent
```

---

## 8. Constraints in MySQL

| Constraint | Example |
|-----------|---------|
| `PRIMARY KEY` | `CONSTRAINT pk_gener PRIMARY KEY (gener_id)` |
| `FOREIGN KEY` | `FOREIGN KEY (PID) REFERENCES PROD(P_ID) ON DELETE CASCADE` |
| `UNIQUE` | `ADD CONSTRAINT con UNIQUE(title)` |
| `CHECK` | `CONSTRAINT c CHECK (age > 0)` |
| `DEFAULT` | `status VARCHAR(20) DEFAULT 'active'` |
| `NOT NULL` | `MODIFY actor_id INT NOT NULL` |
| `AUTO_INCREMENT` | `MODIFY actor_id INT AUTO_INCREMENT` |
| `INDEX` | `CREATE INDEX idx_name ON actor (age)` |

### ENUM & SET
```sql
-- ENUM: exactly one value from the list
CREATE TABLE shirts (
    id   INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(35),
    size ENUM('small', 'medium', 'large', 'x-large')
);

-- SET: one or more values from the list
CREATE TABLE products (
    tags SET('new', 'sale', 'popular')
);
```

### Inspect Constraints
```sql
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'MOVIE_DB';

DESCRIBE actor;   -- quick column overview
SHOW TABLES;
```

---

## 9. Advanced SELECT Queries

```sql
-- Basic filtering
SELECT * FROM actor WHERE age > 30;
SELECT * FROM actor WHERE age > 30 AND age < 40;
SELECT * FROM actor WHERE age BETWEEN 30 AND 40;

-- LIKE patterns
-- '_a%' = second character is 'a'
SELECT * FROM actor WHERE name1 LIKE '_a%';

-- NULL check
SELECT * FROM actor WHERE name1 IS NOT NULL;

-- ORDER BY (multiple columns)
SELECT * FROM actor ORDER BY age ASC, name1 DESC;

-- DISTINCT
SELECT DISTINCT age, name1 FROM actor;
SELECT DISTINCT address FROM prod;

-- LIMIT
SELECT * FROM moviec LIMIT 5;
```

---

## 10. Subqueries & Set Operations

> A **subquery** is a SELECT inside another SELECT.

```sql
-- ANY: true if condition is true for at least one value
SELECT * FROM actor
WHERE actor_id > ANY (
    SELECT actor_id FROM actor WHERE actor_id IN (204, 206, 209)
);

-- ALL: true only if condition is true for every value
-- Find movies longer than ALL movies from 2014
SELECT duration FROM Moviec
WHERE duration > ALL (
    SELECT duration FROM Moviec WHERE year1 = 2014
);

-- IN / NOT IN
SELECT moid FROM movie_actor WHERE actid NOT IN (
    SELECT actid FROM actor WHERE name1 = 'Steve Hill'
);

-- Find movies featuring both Actor 201 and some other condition
SELECT moid FROM movie_actor
WHERE actid = 100
  AND moid IN (
    SELECT moid FROM movie_actor WHERE actid = 201
  );
```

### Pattern Recognition Table

| Keyword in question | SQL pattern |
|---------------------|-------------|
| in a list | `IN` |
| not in a list | `NOT IN` |
| greater than every | `> ALL` |
| greater than at least one | `> ANY` |
| maximum | `MAX()` |
| average | `AVG()` |
| never / has not | `NOT IN` |
| both | `AND` with `IN` |
| exists | `EXISTS` |

---

## 11. Aggregate Functions

```sql
SELECT COUNT(*) FROM actor;
SELECT SUM(duration) FROM Moviec;
SELECT AVG(age) FROM actor;
SELECT MIN(age) FROM actor;
SELECT MAX(age) FROM actor;
```

---

## 12. JOINs

> A **JOIN** combines rows from two or more tables based on a related column.

```sql
-- INNER JOIN — only matching rows in both tables
SELECT a.name1, m.title, ma.role1
FROM actor a
INNER JOIN movie_actor ma ON a.actor_id = ma.actid
INNER JOIN Moviec m ON ma.moid = m.M_ID;

-- LEFT JOIN — all rows from left table, NULLs where no match on right
SELECT a.name1, m.title
FROM actor a
LEFT JOIN movie_actor ma ON a.actor_id = ma.actid
LEFT JOIN Moviec m ON ma.moid = m.M_ID;
```

> 💡 **Key join types:**
> - `INNER JOIN` → matching rows in both tables
> - `LEFT JOIN` → all left rows + matching right (NULLs for no match)
> - `RIGHT JOIN` → all right rows + matching left (NULLs for no match)
> - `FULL OUTER JOIN` → all rows from both (not native in MySQL — use UNION)

---

## 13. Movie Database — Full Schema Example

> Full working schema built in class (MOVIE_DB2):

```sql
CREATE DATABASE MOVIE_DB2;
USE MOVIE_DB2;

CREATE TABLE PROD (
    P_ID    INT PRIMARY KEY,
    PNAME   VARCHAR(50),
    ADDRESS VARCHAR(100)
);

CREATE TABLE actor (
    actor_id INT PRIMARY KEY,
    age      INT,
    name1    VARCHAR(50),
    dob      DATE,
    CONSTRAINT c CHECK (age > 0)
);

CREATE TABLE director (
    director_id INT PRIMARY KEY,
    name1       VARCHAR(50),
    dob         DATE,
    act         VARCHAR(50)
);

CREATE TABLE gener (
    gener_id INT PRIMARY KEY,
    name1    VARCHAR(50)
);

CREATE TABLE Moviec (
    M_ID     INT PRIMARY KEY,
    actor_ID VARCHAR(50),
    rol      VARCHAR(100),
    PID      INT,
    status1  VARCHAR(20) DEFAULT 'active',
    title    VARCHAR(700) UNIQUE,
    FOREIGN KEY (PID) REFERENCES PROD(P_ID) ON DELETE CASCADE
);

-- Junction tables (many-to-many relationships)
CREATE TABLE movie_actor (
    actid INT,
    moid  INT,
    role1 VARCHAR(70),
    FOREIGN KEY (actid) REFERENCES actor(actor_id) ON DELETE CASCADE,
    FOREIGN KEY (moid)  REFERENCES Moviec(M_ID)   ON DELETE CASCADE
);

CREATE TABLE movie_director (
    dirid INT,
    mid   INT,
    role1 VARCHAR(70),
    FOREIGN KEY (dirid) REFERENCES director(director_id) ON DELETE CASCADE,
    FOREIGN KEY (mid)   REFERENCES Moviec(M_ID)          ON DELETE CASCADE
);

CREATE TABLE movie_gener (
    generid INT,
    movieid INT,
    FOREIGN KEY (generid) REFERENCES gener(gener_id) ON DELETE CASCADE,
    FOREIGN KEY (movieid) REFERENCES Moviec(M_ID)    ON DELETE CASCADE
);

CREATE TABLE quots (
    actid INT,
    moid  INT,
    text1 VARCHAR(70),
    FOREIGN KEY (actid) REFERENCES actor(actor_id) ON DELETE CASCADE,
    FOREIGN KEY (moid)  REFERENCES Moviec(M_ID)    ON DELETE CASCADE
);
```

### Derived age using SELECT
```sql
-- Calculate age from DOB without storing it
SELECT name1, dob, (YEAR(CURDATE()) - YEAR(dob)) AS age
FROM actor;
```

---

## 14. Notes & Tasks

| # | Note |
|---|------|
| 📝 | `DELETE` can be rolled back; `TRUNCATE` cannot — always know which you need |
| 📝 | `> ANY` = true if greater than at least one value; `> ALL` = must beat every value |
| 📝 | 1NF → one value per cell; 2NF → no partial dependency; 3NF → no transitive dependency |
| 📝 | `ENUM` = pick one; `SET` = pick one or more |
| 📝 | `ON DELETE CASCADE` — deleting the parent row auto-deletes child rows |
| 📝 | `AUTO_INCREMENT` lets MySQL assign IDs automatically (surrogate key) |
| 📝 | Views are virtual — they don't store data, just save the query |
| 🔧 | **Task:** Write SRS document for Mail Order database project |
| 🔧 | **Task:** Design ERD for Mail Order database (employees, customers, parts, orders) |
| 🔧 | **Task:** Practice normalizing a denormalized table through 1NF → 2NF → 3NF |
| 🔧 | **Task:** Choose project title from [ER diagram examples](https://edrawmax.wondershare.com/examples/er-diagram-examples.html) |
| 🔧 | **Task:** Practice subqueries — `IN`, `NOT IN`, `ANY`, `ALL`, `EXISTS` |

---

*📅 Notes taken: May 9, 2026*
