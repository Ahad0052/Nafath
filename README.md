# 🤖 AI & Data Science Bootcamp — Notes
**Student:** Ahad Aljabri | **Program:** 20-Week AI & Data Science Bootcamp

---

## 📁 Repository Structure

```
📦 repo/
├── README.md
│
├── 📂 Notes by week/
│   ├── Week1_Python_Fundamentals.md              ← Variables, strings, conditionals, loops
│   ├── Week2_Loops_Functions_Git.md              ← For loops, functions, recursion, Git
│   ├── Week3_Data_Structures_Files.md            ← Lists, dicts, tuples, sets, files, errors
│   ├── Week4_NumPy_Pandas_Visualization.md       ← NumPy, Pandas, Matplotlib, Seaborn, IQR
│   ├── Week5_AdvPandas_Plotly_Dash_DB.md         ← Advanced Pandas, Plotly, Dash, Altair, DB & ERD
│   ├── Week6_SQL_DatabaseDesign_Normalization.md ← SQL, Normalization, Subqueries, JOINs
│   ├── Week7_DBProject_PowerBI.md                ← DB Project delivery (FRMS), Power BI intro
│   └── Week8_PowerBI_TalabatDashboard.md         ← Power BI project: Talabat Operations Dashboard
│
├── 📂 Projects/
│   ├── FRMS/                                     ← Food Recipes Management System (Week 7)
│   │   ├── RecipeSRS_V1_0.pdf
│   │   ├── frms_schema.sql
│   │   ├── frms_data.sql
│   │   └── frms_queries.sql
│   │
│   └── Talabat_Dashboard/                        ← Talabat Operations Dashboard (Week 8)
│       ├── TalabatSRS_V1_0.pdf
│       └── talabat_dashboard.pbix
│
└── 📂 messy notes/   ← raw in-class notebooks (updated daily)
```

---

## 📚 Weekly Progress

| Week | Topics | Status |
|------|--------|--------|
| Week 1 | Variables, Strings, Conditionals, While Loops | ✅ |
| Week 2 | For Loops, Functions, Recursion, Git | ✅ |
| Week 3 | Lists, Dictionaries, Tuples, Sets, Files, Error Handling | ✅ |
| Week 4 | NumPy, Pandas, Matplotlib, Seaborn, Outlier Detection | ✅ |
| Week 5 | Advanced Pandas, Plotly, Dash, Altair, Database Design & ERD | ✅ |
| Week 6 | SQL (DDL/DML/DCL/TCL), Normalization, Subqueries, JOINs | ✅ |
| Week 7 | DB Project Delivery (FRMS), SRS Writing, Power BI Intro | ✅ |
| Week 8 | Power BI Project: Talabat Operations Dashboard (100K rows, 25 DAX measures, 6 pages) | ✅ |

---

## 🧠 Key Concepts by Week

### Week 1
- Python math operators (`%`, `//`, `**`)
- String methods (`.upper()`, `.replace()`, `.find()`, `.count()`)
- `if / elif / else` conditionals
- Boolean logic (`and`, `or`, `not`)
- `while` loops
- User input and `%` formatting

### Week 2
- Git & GitHub workflow (push, clone, branch)
- ATM banking system assignment
- `while` loops deep dive (sum, max, min, duplicates)
- `for` loops and `range()`
- Nested loops and star patterns
- Functions, `return`, default arguments, `*args`
- Lambda functions
- Recursion (factorial, sum, fibonacci)
- `split()`, `map()`, regex intro

### Week 3
- Lists — creating, indexing, slicing, methods (`.append()`, `.insert()`, `.pop()`, `.remove()`)
- Searching — linear search O(n), binary search O(log n)
- Dictionaries — key-value pairs, `.items()`, `.keys()`, `.values()`, nested dicts
- Tuples — immutable sequences, `.count()`, `.index()`
- Sets — unique elements, `set()` vs `{}`
- Files — `open()`, `.readline()`, `.readlines()`, `.read()`, `.write()`, modes `r/w/a`
- Error handling — `try / except / finally`, `raise`, input validation loops

### Week 4
- NumPy — arrays, slicing, broadcasting, `np.where()`, math, random, statistics
- Pandas — Series, DataFrame, `iloc`/`loc`, filtering, groupby, encoding, datetime
- Matplotlib — line, bar, histogram, scatter, pie, box plots
- Seaborn — heatmaps, violin plots, bubble charts
- Outlier detection & removal using IQR method

### Week 5
- Geographic maps with Basemap (bubble size = data value)
- Multi-index DataFrames — `loc` with tuples, `slice(None)` as wildcard
- `pd.merge()` vs `.join()` — inner, left, right, outer, cross
- `df.query()` — SQL-like filtering
- `pd.cut()` vs `pd.qcut()` — binning strategies
- Plotly Express — scatter, bar, line charts with hover & interactivity
- Plotly animations — `animation_frame`, `animation_group`
- Dash — building reactive web dashboards with `@app.callback`
- Altair — declarative chart grammar
- DBMS concepts — define, construct, manipulate, maintain
- Database design process — requirements → conceptual → logical → physical
- ERD — entities, attributes, relationships, cardinality, and keys

### Week 6
- SQL language categories — DDL, DML, DCL, TCL and when to use each
- Normal forms — 1NF, 2NF, 3NF
- DDL commands — `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`
- DML commands — `INSERT`, `UPDATE`, `DELETE`, `SELECT` with `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`
- Constraints — `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, `DEFAULT`, `NOT NULL`, `AUTO_INCREMENT`
- `ENUM` vs `SET` — single-choice vs multi-choice column types
- Subqueries — `IN`, `NOT IN`, `ANY`, `ALL`, `EXISTS`
- Aggregate functions — `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- JOINs — `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`
- Views — virtual tables derived from queries
- `ON DELETE CASCADE` — cascading deletes through foreign key relationships

### Week 7
- SRS writing — purpose, scope, functional & non-functional requirements, timeline, financial plan
- Food Recipes Management System (FRMS) — full project from SRS to deployed DB
- ERD design — RECIPE, CHEF, INGREDIENT, NUTRITION, CATEGORY, MEAL + junction tables
- 3NF normalization applied to a real project schema
- Power BI Desktop — connecting to data, Power Query transformations
- DAX basics — `COUNT`, `AVERAGE`, `SUM`, `FILTER`, `CALCULATE`
- Data model relationships in Power BI — mirroring SQL foreign keys
- Visual types: cards, bar charts, donut charts, slicers, cross-filtering

### Week 8
- Full Power BI project lifecycle — SRS → data audit → Power Query → DAX → 6-page dashboard → presentation
- Dataset audit — identifying and documenting data quality issues before writing any DAX
- Data fixes — `VALUE()` for text-to-number conversion, `FORMAT()` calculated column for empty `Day_of_Week`
- 25 DAX measures across 7 display folders: aggregations, filters, rates, per-unit, time, traffic, targets
- DAX functions: `COUNTROWS`, `SUM`, `AVERAGE`, `DISTINCTCOUNT`, `CALCULATE`, `AVERAGEX`, `FILTER`, `DIVIDE`, `DATEDIFF`, `VALUE`, `FORMAT`
- `CALCULATE()` — modifying filter context (most important DAX function)
- `DIVIDE()` — safe division, always use instead of `/`
- `AVERAGEX()` + `FILTER()` — row-by-row iteration on filtered subsets
- 6 dashboard pages: Executive Overview, Delivery Performance, Revenue & Orders, Restaurant & Menu, Operations & Traffic, Customer Behaviour
- Map visual using latitude/longitude columns
- Gauge visual with target value
- Display folders — organizing 25+ measures to keep the field list clean
- Key business insights from 100,000 real-world food delivery records

---

- Build solid Python foundations
- Practice Git & GitHub habits early
- Work toward Computer Vision and Kaggle projects

---

*Last updated: May 2026*
