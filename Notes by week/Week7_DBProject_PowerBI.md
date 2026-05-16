# 🐍 Week 7 — Database Project Delivery & Introduction to Power BI
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Project: Food Recipes Management System](#1-project-food-recipes-management-system)
2. [SRS — Software Requirements Specification](#2-srs--software-requirements-specification)
3. [ERD — Entity Relationship Diagram](#3-erd--entity-relationship-diagram)
4. [Database Schema (MySQL)](#4-database-schema-mysql)
5. [Normalization Applied](#5-normalization-applied)
6. [SQL Queries — Key Examples](#6-sql-queries--key-examples)
7. [Power BI — Introduction](#7-power-bi--introduction)
8. [Power BI — Core Concepts](#8-power-bi--core-concepts)
9. [Notes & Tasks](#9-notes--tasks)

---

## 1. Project: Food Recipes Management System

> **Project title:** Food Recipes Management System (FRMS)
> **Team:** Ahad Al-jabri & Mayar Al-khalili
> **Submitted:** 3 May 2026

### What the system does
A database that stores and manages information about recipes, ingredients, cooking instructions, chefs, and meal plans. Users can search for recipes, view nutrition facts, and manage recipe data.

### Target Users
| User | Use Case |
|------|----------|
| Chef | Manage personal recipes and cooking instructions |
| Restaurant | Store menus and meal plans |
| Nutritionist | Analyze nutrition data per recipe |
| Food Blogger | Browse and publish recipes |

### Project Constraints
- Limited project time (one week)
- Database covers core recipe management only (not online ordering or customer interaction)
- Dataset is synthetic (AI-generated)

---

## 2. SRS — Software Requirements Specification

> An **SRS** documents what a system should do before any code is written. It's the contract between the developer and the stakeholder.

### Standard SRS Structure
```
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Overview

2. General Description
   2.1 Users
   2.2 Objectives

3. Data Requirements
4. Functional Requirements
5. Non-Functional Requirements
6. Tools & Technologies
7. Expected Outputs (include Prototype)
8. Constraints
9. Project Timeline
10. Financial Requirements
    10.1 Cost Breakdown
    10.2 Payment Terms
11. Key Insights
12. Recommendations
```

### Functional Requirements (FRMS)
- Store and manage recipe data (CRUD operations)
- Allow adding, viewing, updating, and deleting recipes
- Store related information: ingredients, categories, nutrition facts
- Search recipes by name or ingredient
- Ensure data integrity using keys and relationships
- Retrieve data efficiently using SQL queries

### Non-Functional Requirements
- Data accuracy and consistency
- Efficient query execution
- Simple and well-structured design
- Maintainable and scalable

### Tools & Technologies
| Tool | Purpose |
|------|---------|
| MySQL | DBMS — store and manage data |
| MySQL Workbench | GUI for writing and running SQL |
| Draw.io | ERD diagram design |
| Claude | AI assistance |

### Financial Plan (FRMS)
| Item | Description | Cost (OMR) |
|------|-------------|------------|
| Data Preparation | Collecting and organizing recipe data | 50 |
| Database Design | Creating tables, relationships, schema | 70 |
| Testing & Validation | Ensuring data integrity and query accuracy | 30 |
| Deployment | Setting up and delivering the database | 20 |
| **Total** | | **170 OMR** |

> 💡 **Payment Terms:** 50% upfront, 50% after completion.

### Project Timeline (3–10 May 2026)
| Phase | Day |
|-------|-----|
| Requirement Gathering | Sun 3 |
| Database / ERD Design | Mon 4 |
| Normalization | Tue 5 |
| SQL Coding | Wed 6 |
| SQL Implementation | Thu 7 |
| Testing | Fri 8 |
| Final Documentation | Sat 9 |
| Review & Submission | Sun 10 |

---

## 3. ERD — Entity Relationship Diagram

### Entities & Relationships

```
CHEF ──── Prepare ──── RECIPE ──── have ──── NUTRITION
 (M)                    (M)                    (1)
                         |
              ┌──────────┼──────────┐
          belongs_to  Contain   composed_of
              |           |           |
           CATEGORY   INGREDIENT    MEAL
```

### Entity Attributes

**CHEF** — `chef_id` (PK), `name`, `email`, `country`, `experience_years`, `number_of_chef`

**RECIPE** — `recipe_id` (PK), `title`, `description`, `cooking_time`, `difficulty_level`, `category_id` (FK)

**INGREDIENT** — `ingredient_id` (PK), `ingredient_name`, `unit`

**NUTRITION** — `nutrition_id` (PK), `recipe_id` (FK), `calories`, `fat`, `protein`, `carbohydrates`

**CATEGORY** — `category_id` (PK), `category_name`

**MEAL** — `meal_id` (PK), `meal_name`, `description`

### Junction Tables (Many-to-Many)
| Junction Table | Connects |
|---------------|---------|
| `recipe_ingredient` | RECIPE ↔ INGREDIENT |
| `recipe_chef` | RECIPE ↔ CHEF |
| `meal_recipe` | MEAL ↔ RECIPE |

---

## 4. Database Schema (MySQL)

```sql
CREATE DATABASE FRMS;
USE FRMS;

CREATE TABLE category (
    category_id   INT PRIMARY KEY,
    category_name VARCHAR(200)
);

CREATE TABLE chef (
    chef_id          INT PRIMARY KEY,
    name             VARCHAR(50),
    experience_years INT,
    country          VARCHAR(50),
    email            VARCHAR(200),
    number_of_chef   INT
);

CREATE TABLE recipe (
    recipe_id        INT PRIMARY KEY,
    title            VARCHAR(300),
    description      VARCHAR(500),
    cooking_time     TIME,
    difficulty_level VARCHAR(50),
    category_id      INT,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE ingredient (
    ingredient_id   INT PRIMARY KEY,
    ingredient_name VARCHAR(300),
    unit            DECIMAL(50, 2)
);

CREATE TABLE nutrition (
    nutrition_id  INT PRIMARY KEY,
    recipe_id     INT,
    calories      DECIMAL(5, 2),
    fat           DECIMAL(5, 2),
    protein       DECIMAL(5, 2),
    carbohydrates DECIMAL(5, 2),
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
);

CREATE TABLE meal (
    meal_id     INT PRIMARY KEY,
    meal_name   VARCHAR(700),
    description VARCHAR(900)
);

-- Junction tables
CREATE TABLE recipe_ingredient (
    recipe_id     INT,
    ingredient_id INT,
    quantity      DECIMAL(60, 2),
    FOREIGN KEY (recipe_id)     REFERENCES recipe(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

CREATE TABLE recipe_chef (
    chef_id   INT,
    recipe_id INT,
    FOREIGN KEY (chef_id)   REFERENCES chef(chef_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
);

CREATE TABLE meal_recipe (
    meal_id   INT,
    recipe_id INT,
    FOREIGN KEY (meal_id)   REFERENCES meal(meal_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(recipe_id)
);
```

---

## 5. Normalization Applied

| Form | How it's applied in FRMS |
|------|--------------------------|
| **1NF** | Each cell holds one value — nutrition split into separate columns (calories, fat, protein, carbs) |
| **2NF** | Junction tables remove partial dependencies — quantity depends on both recipe AND ingredient |
| **3NF** | No transitive dependencies — chef country lives in `chef`, not repeated inside `recipe` |

---

## 6. SQL Queries — Key Examples

```sql
-- All recipes with their category
SELECT r.title, c.category_name
FROM recipe r
JOIN category c ON r.category_id = c.category_id;

-- Recipes with their chef
SELECT r.title, ch.name, ch.experience_years
FROM recipe r
JOIN recipe_chef rc ON r.recipe_id = rc.recipe_id
JOIN chef ch ON rc.chef_id = ch.chef_id;

-- Nutrition facts for a specific recipe
SELECT r.title, n.calories, n.fat, n.protein, n.carbohydrates
FROM recipe r
JOIN nutrition n ON r.recipe_id = n.recipe_id
WHERE r.title = 'Omani Halwa';

-- Ingredients used in each recipe
SELECT r.title, i.ingredient_name, ri.quantity
FROM recipe r
JOIN recipe_ingredient ri ON r.recipe_id = ri.recipe_id
JOIN ingredient i ON ri.ingredient_id = i.ingredient_id
ORDER BY r.title;

-- Recipe count per category
SELECT c.category_name, COUNT(r.recipe_id) AS recipe_count
FROM category c
LEFT JOIN recipe r ON c.category_id = r.category_id
GROUP BY c.category_name
ORDER BY recipe_count DESC;

-- Average calories per difficulty level
SELECT difficulty_level, AVG(n.calories) AS avg_calories
FROM recipe r
JOIN nutrition n ON r.recipe_id = n.recipe_id
GROUP BY difficulty_level;
```

---

## 7. Power BI — Introduction

> After submitting the FRMS project, we moved into a new topic: **Power BI** — Microsoft's tool for connecting to data, building visualizations, and sharing interactive dashboards without needing to write frontend code.

### What is Power BI?
Power BI is a business intelligence platform with three main parts:

| Component | Description |
|-----------|-------------|
| **Power BI Desktop** | The main app — build reports locally (.pbix file) |
| **Power BI Service** | Cloud — publish and share reports with others |
| **Power BI Mobile** | View dashboards on phone or tablet |

### The Power BI Workflow
```
Data Source → Power Query (clean & transform) → Data Model → Visuals → Dashboard
```

---

## 8. Power BI — Core Concepts

### Connecting to Data
Power BI can connect to many sources: Excel / CSV files, MySQL / SQL Server, APIs, SharePoint, Azure, and more.

```
Home → Get Data → choose source → load or transform
```

### Power Query — ETL Step
> Power Query is where you clean and shape data **before** it enters the model. Think of it as pandas but with a GUI.

Common transformations:
- Change column data types
- Remove duplicates or nulls
- Rename or remove columns
- Filter rows
- Merge or append tables
- Create calculated columns

### Data Model — Relationships
> Like SQL foreign keys, but visual. Connect tables by dragging matching columns together in Model view.

```
category ──1──── recipe ────M── recipe_ingredient ────M── ingredient
                   │
                   ├────1──── nutrition
                   └────M── recipe_chef ────M── chef
```

> 💡 Set relationships in Model view — Power BI uses them to automatically cross-filter all visuals on a page when a slicer or chart is clicked.

### DAX — Data Analysis Expressions
> DAX is the formula language used to create **measures** — calculated values that update dynamically as filters change.

```dax
Total Recipes = COUNT(recipe[recipe_id])

Avg Calories  = AVERAGE(nutrition[calories])

Hard Recipes  = COUNTROWS(FILTER(recipe, recipe[difficulty_level] = "Hard"))

Total Protein = SUM(nutrition[protein])
```

> 💡 **Power Query vs DAX:**
> - **Power Query** → transforms raw data at load time (runs once)
> - **DAX** → computes measures dynamically (recalculates whenever filters change)

### Visual Types
| Visual | Used For |
|--------|---------|
| Card | Single KPI number |
| Bar / Column chart | Comparing categories |
| Donut / Pie chart | Proportions |
| Line chart | Trends over time |
| Table / Matrix | Detail-level data |
| Slicer | Interactive filter — cross-filters all visuals on the page |

---

## 9. Notes & Tasks

| # | Note |
|---|------|
| 📝 | SRS must be written **before** building — it defines scope and prevents scope creep |
| 📝 | 50/50 payment terms are standard for freelance database projects |
| 📝 | Power BI relationships work like SQL foreign keys — connect tables in Model view |
| 📝 | Power Query runs first (ETL); DAX runs dynamically after filters are applied |
| 📝 | A slicer cross-filters **all** visuals on the page automatically — no code needed |
| 📝 | `.pbix` is the Power BI Desktop file format — push it to GitHub like any other project file |
| 🔧 | **Task:** Practice DAX — `CALCULATE()`, `RELATED()`, `SUMX()` |
| 🔧 | **Task:** Connect FRMS MySQL to Power BI and build the data model |
| 🔧 | **Task:** Build a full FRMS dashboard in Power BI as a follow-up project |
| 🔧 | **Task:** Publish a report to Power BI Service |

---

*📅 Notes taken: May 3–10, 2026*
