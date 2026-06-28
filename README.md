# 🤖 AI & Data Science Bootcamp — Notes
**Student:** Ahad Aljabri | **Program:** 20-Week AI & Data Science Bootcamp

---

## 📁 Repository Structure

```
📦 Nafath/
├── README.md
│
└── 📂 Notes by week/
    ├── Week1_Python_Fundamentals.md
    ├── Week2_Loops_Functions_Git.md
    ├── Week3_Data_Structures_Files.md
    ├── Week4_NumPy_Pandas_Visualization.md
    ├── Week5_AdvPandas_Plotly_Dash_DB.md
    ├── Week6_SQL_DatabaseDesign_Normalization.md
    ├── Week7_DBProject_PowerBI.md
    ├── Week8_PowerBI_TalabatDashboard.md
    ├── Week10_Statistics_WebScraping.md
    ├── Week11_ETL_Docker_Prefect.md
    ├── Week12_Airflow_Prefect_ETL.md
    └── Week13_MachineLearning.md
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
| Week 10 | Statistics for AI (probability, regression, hypothesis testing) + Selenium web scraping | ✅ |
| Week 11 | ETL Pipelines, Docker, Docker Compose, Prefect orchestration | ✅ |
| Week 12 | Apache Airflow, Prefect + Docker, TRA Telecom Analytics Pipeline | ✅ |
| Week 13 | Introduction to Machine Learning — Linear/Logistic Regression, KNN, K-Means, SVM, Decision Trees | ✅ |

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
- Key business insights from 100,000 real-world food delivery records

### Week 10
- Descriptive statistics — mean, median, mode, std, variance, IQR using NumPy and Pandas
- Probability — basic rules, conditional probability, Bayes' theorem
- Permutations vs combinations — when order matters vs doesn't, `factorial()`, `comb()`
- Distributions & sampling — normal distribution, z-scores, Central Limit Theorem, sampling methods
- Confidence intervals — formula, z-scores for 95%/99%, computing with `scipy.stats.t.interval()`
- Hypothesis testing — H₀ vs H₁, p-value, significance level α, t-tests, Type I & II errors
- Linear regression — slope/intercept, R², MSE, RMSE, assumptions, `sklearn.linear_model.LinearRegression`
- Logistic regression — sigmoid function, binary classification, precision/recall/F1, confusion matrix
- Web scraping with Selenium — `webdriver`, `By` locators, `WebDriverWait`, explicit waits
- Two-phase scraping architecture — Phase 1: collect links, Phase 2: deep scrape each article
- Headless Chrome — faster scraping without a visible browser window
- Progressive CSV saving — write row-by-row to prevent data loss on crash
- Times of Oman news scraper — scraped 1,000+ Oman news articles (title, description, image, URL)

### Week 11
- ETL pipeline architecture — Extract → Transform → Load as three separated, testable modules
- Store Sales ETL — merged 3 messy CSV files, cleaned data quality issues, loaded star schema into MySQL
- Data cleaning — per-group median imputation, junk value removal, type conversion, currency normalisation (USD → OMR)
- Star schema design — fact table (`sales`) + dimension tables (`store`, `customer`, `product`)
- Weather ETL (basic) — OpenWeatherMap API → transform → append to CSV, config via `.env`
- Dockerfile — `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`
- Docker build & run — `docker build`, `docker run`, `--env-file`
- Docker Compose — multi-container app with Flask backend + Streamlit frontend
- `docker-compose.yml` — services, ports, env_file, environment, depends_on
- Flask API — `@app.route`, `request.args.get`, `jsonify`, `host="0.0.0.0"` for Docker
- Streamlit frontend — `st.text_input`, `st.button`, `st.spinner`, calling a backend via `requests`
- Prefect orchestration — `@task` and `@flow` decorators, retries, Prefect UI
- Gold price ETL with Prefect — goldapi.io → transform → CSV + MySQL, full `@flow` with four `@task` steps
- `python-dotenv` — `load_dotenv(override=True)`, `os.getenv()` — never hardcode credentials

### Week 12
- Apache Airflow — DAGs, `PythonOperator`, task dependencies with `>>`, DAG parameters
- Airflow scheduling — `schedule="@hourly"`, `catchup=False`, `start_date`
- XCom — `ti.xcom_push()` / `ti.xcom_pull()` for passing data between Airflow tasks
- Airflow + Docker Compose — `apache/airflow:3.0.4`, `command: standalone`, DAGs volume mount
- `condition: service_healthy` — healthcheck-gated container startup in Docker Compose
- Prefect + Docker Compose — `prefecthq/prefect:3-latest`, worker pool, 4-service architecture
- `gold_pipeline.serve(cron="*/2 * * * *")` — scheduling a Prefect flow from code
- Startup race condition — polling `api/health` endpoint before calling `.serve()`
- Gold price ETL with Airflow — goldapi.io → XCom → CSV + MySQL, hourly DAG
- Gold price ETL with Prefect + Docker — same pipeline, live Prefect server + worker + MySQL
- Timestamp normalisation — handling None / Unix ms / Unix s / ISO string from the same API field
- TRA Telecom Analytics Pipeline — Prefect + SQLite processing official TRA Oman labor force data
- Derived metrics — `pct_change()` for growth rate, Omanization rate, expat ratio
- Arabic sheet names — `pd.read_excel(sheet_name="التوظيف")` works natively in pandas
- Two SQLite tables — `raw_telecom_data` (original) + `telecom_analytics` (with derived columns)
- Airflow vs Prefect — DAG/flow, XCom/return values, setup complexity, best use cases

### Week 13
- What is ML — algorithms that learn from experience instead of following explicit rules
- Supervised learning — regression & classification from labelled data; unsupervised learning — clustering & dimensionality reduction
- ML workflow — EDA → feature engineering → model selection → train/test split → evaluate → tune → deploy
- Bias-variance tradeoff — underfitting vs overfitting, `train_test_split`, `cross_val_score`
- Linear regression — simple (`y = mx + b`) and multiple; metrics R², MSE, RMSE, MAE
- Gradient descent — optimizing loss iteratively via gradients, `SGDRegressor`, learning rate & epochs
- Regularization — Ridge (L2, shrinks coefficients) vs Lasso (L1, zeroes coefficients → feature selection)
- Logistic regression — sigmoid function, binary classification, `predict()`, `predict_proba()`, insurance prediction task
- Evaluation metrics — accuracy, precision, recall, F1, confusion matrix; macro vs micro averaging
- K-Nearest Neighbors (KNN) — distance-based, majority vote, ALWAYS scale features first
- K-Means clustering — unsupervised, centroids, inertia, elbow method for choosing K
- PCA — dimensionality reduction, `explained_variance_ratio_`, speeds up training & reduces overfitting
- Support Vector Machines (SVM) — maximum-margin hyperplane, support vectors, kernels (linear, rbf, poly)
- Decision Trees — Gini/MSE split criteria, no scaling needed, feature importances, prone to overfitting
- scaling rules: KNN & SVM are distance-based → must scale; Decision Trees split on thresholds → no scaling

---

- Build solid Python foundations
- Practice Git & GitHub habits early
- Work toward Computer Vision and Kaggle projects

---

*Last updated: June 2026*
