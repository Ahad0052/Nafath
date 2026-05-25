# 🐍 Week 8 — Power BI Project: Talabat Operations Dashboard
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Project Overview](#1-project-overview)
2. [SRS — Software Requirements Specification](#2-srs--software-requirements-specification)
3. [Dataset — Column Reference](#3-dataset--column-reference)
4. [Data Quality Issues & Fixes](#4-data-quality-issues--fixes)
5. [DAX Measures — All 25](#5-dax-measures--all-25)
6. [Dashboard Pages — All 6](#6-dashboard-pages--all-6)
7. [Key Insights](#7-key-insights)
8. [Recommendations](#8-recommendations)
9. [Power BI — Concepts Applied](#9-power-bi--concepts-applied)
10. [Notes & Tasks](#10-notes--tasks)

---

## 1. Project Overview

> **Project:** Talabat Operations Dashboard
> **Tool:** Microsoft Power BI Desktop
> **Prepared by:** Ahad Salim ALjabri
> **Date:** 21/5/2026

### Dataset at a Glance
| Metric | Value |
|--------|-------|
| Total Orders | 100,000 |
| Unique Customers | 9,000 |
| Unique Restaurants | 1,000 |
| Unique Drivers | 500 |
| Total Revenue | EGP 26,892,573 |
| Avg Order Value | EGP 268.93 |
| Cities Covered | 7 (Cairo, Giza, Alexandria, Mansoura, Tanta, Zagazig, Assiut) |
| Data Period | 15 days |
| Delivery Success Rate | 85.2% |

### What the dashboard does
Transforms 100,000 raw food delivery order records into actionable insights across **6 analytical domains**: executive overview, delivery performance, revenue analysis, restaurant & menu analysis, operational intelligence, and customer behaviour.

---

## 2. SRS — Software Requirements Specification

### Purpose
Document the design, development, and analytical outcomes of the Talabat Operations Dashboard — a business intelligence solution built in Power BI.

### Scope
Covers the complete Talabat order lifecycle across 7 Egyptian cities over a 15-day operational period. Serves executives, operations managers, finance teams, restaurant partners, logistics coordinators, and marketing analysts.

### Functional Requirements — Dashboard Pages
| Page | Title | Key Visuals |
|------|-------|-------------|
| 1 | Executive Overview | 4 KPI cards, line chart (orders over time), bar chart (orders by city), 2 donut charts (order status + payment method) |
| 2 | Delivery Performance | 4 cards, bar chart (delivery time by city), clustered bar (traffic impact), scatter (distance vs time), stacked bar (on-time vs delayed) |
| 3 | Revenue & Orders | 4 cards, bar chart (top items), column charts (revenue by hour + day), gauge (orders per customer) |
| 4 | Restaurant & Menu | 3 cards, bar chart (top 10 restaurants), donut (orders by item), leaderboard table, clustered bar (items by city) |
| 5 | Operations & Traffic | 3 cards, map visual, clustered bar (traffic vs delay), donut (vehicle split), matrix (vehicle vs traffic) |
| 6 | Customer Behaviour | 4 cards, column charts (orders by day + hour), stacked bar (payment by city), bar chart (avg order value by city) |

### Non-Functional Requirements
- Dashboard loads within 5 seconds on 100,000 rows
- Each page has one clear purpose
- All measures use `DIVIDE()` to prevent division-by-zero errors
- `VALUE()` applied to `Delivery_Delay` to resolve text/numeric type mismatch
- All 25 measures organized into 7 display folders in the data model
- All values use human-readable format strings

### Tools & Technologies
| Tool | Purpose |
|------|---------|
| Power BI Desktop (2026) | Dashboard development, data modeling |
| DAX | 25 calculated measures across 7 function categories |
| Power Query | Data loading and initial transformation |
| Azure Maps / ArcGIS | Geographic map on Operations page |
| Kaggle | Source dataset (`talabat_enhanced_orders`) |

### Constraints
- Static dataset — no live connection; reflects a snapshot only
- `Day_of_Week` source column is empty — fixed via calculated column
- `Driver_Availability` excluded — offline drivers showed completed deliveries (unreliable data)
- No time intelligence — dataset only covers 15 days
- Map visual requires Azure Maps or ArcGIS license
- Currency labeled as EGP — inferred from Egyptian city data (original had no label)

### Financial Plan
| Item | Cost (OMR) |
|------|------------|
| Dashboard Development | 150 |
| Data Cleaning | 60 |
| DAX Measures & KPIs | 80 |
| Interactive Visuals | 100 |
| Deployment & Publishing | 40 |
| Documentation | 40 |
| **Total** | **470 OMR** |

> 💡 **Payment Terms:** 50% upfront, 50% after completion.

### Project Timeline
| Phase | Activity | Duration |
|-------|----------|----------|
| 1 | Data Exploration — load dataset, audit 21 columns | Day 1 |
| 2 | SRS Documentation | Day 1–2 |
| 3 | Data Quality Fixes — VALUE(), Day_of_Week calculated column | Day 1–2 |
| 4 | Data Modeling — 25 DAX measures across 7 folders | Day 2–3 |
| 5 | Dashboard Build — 6 pages, all visuals and slicers | Day 3–5 |
| 6 | Review & Fix — visual corrections | Day 5–6 |
| 7 | Currency Update — format all revenue strings to EGP | Day 6–7 |

---

## 3. Dataset — Column Reference

| Column | Type | Description |
|--------|------|-------------|
| `Order_ID` | Text | Unique order identifier |
| `User_ID` | Text | Customer identifier — 9,000 unique values |
| `Restaurant_ID` | Text | Restaurant identifier — 1,000 unique values |
| `Driver_ID` | Text | Driver identifier — 500 unique values |
| `Item_Name` | Text | Menu item ordered — 9 categories |
| `Quantity` | Integer | Number of items per order |
| `Total_Price` | Decimal | Order total in EGP |
| `Order_Date` | Date | Date of order placement |
| `Order_Time` | Time | Time of order placement |
| `Delivery_Duration_Minutes` | Integer | Actual delivery time in minutes |
| `Delivery_Distance_km` | Decimal | Distance from restaurant to customer |
| `Delivery_Delay` | Text | Actual duration minus 37-min benchmark — **stored as text, converted via `VALUE()`** |
| `City` | Text | One of 7 Egyptian cities |
| `Payment_Method` | Text | Cash / Credit Card / Wallet |
| `Order_Status` | Text | Delivered / Cancelled / In Transit |
| `Traffic_Level` | Text | Low / Medium / High |
| `Driver_Vehicle` | Text | Motorbike / Car / Bicycle |
| `Day_of_Week` | Text | **Empty in source** — fixed via `FORMAT([Order_Date], "dddd")` |
| `order_hour` | Integer | Hour of day (0–23) |
| `Customer_Lat` | Decimal | Customer latitude — used in map visual |
| `Customer_Lon` | Decimal | Customer longitude — used in map visual |

---

## 4. Data Quality Issues & Fixes

| Issue | Root Cause | Fix Applied |
|-------|-----------|-------------|
| `Day_of_Week` column is empty | Source data not populated | Calculated column: `FORMAT([Order_Date], "dddd")` |
| `Delivery_Delay` stored as Text | Source data type mismatch | Wrapped in `VALUE()` inside every DAX measure that uses it |
| `Driver_Availability` unreliable | Offline drivers showed completed deliveries | Column excluded entirely from analysis |
| No currency label | Dataset from Kaggle had no currency info | EGP inferred from Egyptian city context and applied to all format strings |

> 💡 **Lesson:** Real datasets always have quality issues. Auditing all 21 columns on Day 1 before writing any DAX saved hours of debugging later.

---

## 5. DAX Measures — All 25

> All 25 measures are organized into **7 display folders** in the Power BI data model.

### Aggregation Measures
```dax
Total Orders        = COUNTROWS(talabat_enhanced_orders)
Total Revenue       = SUM(talabat_enhanced_orders[Total_Price])
Avg Order Value     = AVERAGE(talabat_enhanced_orders[Total_Price])
Avg Delivery Time   = AVERAGE(talabat_enhanced_orders[Delivery_Duration_Minutes])
Avg Delivery Distance = AVERAGE(talabat_enhanced_orders[Delivery_Distance_km])
Unique Customers    = DISTINCTCOUNT(talabat_enhanced_orders[User_ID])
Unique Restaurants  = DISTINCTCOUNT(talabat_enhanced_orders[Restaurant_ID])
Unique Drivers      = DISTINCTCOUNT(talabat_enhanced_orders[Driver_ID])
```

### Filter Measures (CALCULATE)
```dax
Delivered Orders = CALCULATE(COUNTROWS(talabat_enhanced_orders),
                    talabat_enhanced_orders[Order_Status] = "Delivered")

Cancelled Orders = CALCULATE(COUNTROWS(talabat_enhanced_orders),
                    talabat_enhanced_orders[Order_Status] = "Cancelled")

Delayed Orders   = CALCULATE(COUNTROWS(talabat_enhanced_orders),
                    VALUE(talabat_enhanced_orders[Delivery_Delay]) > 37)

On Time Orders   = CALCULATE(COUNTROWS(talabat_enhanced_orders),
                    VALUE(talabat_enhanced_orders[Delivery_Delay]) <= 37)

Avg Delivery Time High Traffic = CALCULATE([Avg Delivery Time (mins)],
                                   talabat_enhanced_orders[Traffic_Level] = "High")

Avg Delivery Time Low Traffic  = CALCULATE([Avg Delivery Time (mins)],
                                   talabat_enhanced_orders[Traffic_Level] = "Low")
```

### Iterating Measures (AVERAGEX + FILTER)
```dax
Avg Delay (mins) = AVERAGEX(
    FILTER(talabat_enhanced_orders, VALUE(talabat_enhanced_orders[Delivery_Delay]) > 0),
    VALUE(talabat_enhanced_orders[Delivery_Delay])
)
```

### Rate Measures (DIVIDE)
```dax
Delivery Success Rate = DIVIDE([Delivered Orders], [Total Orders], 0)
Cancellation Rate     = DIVIDE([Cancelled Orders], [Total Orders], 0)
Delay Rate            = DIVIDE([Delayed Orders],   [Total Orders], 0)
High Traffic Rate     = DIVIDE(
                            CALCULATE([Total Orders],
                                talabat_enhanced_orders[Traffic_Level] = "High"),
                            [Total Orders], 0)
```

### Per-Unit Measures (DIVIDE)
```dax
Orders per Customer   = DIVIDE([Total Orders],   [Unique Customers],    0)
Revenue per Customer  = DIVIDE([Total Revenue],  [Unique Customers],    0)
Revenue per Order     = DIVIDE([Total Revenue],  [Total Orders],        0)
Revenue per Restaurant= DIVIDE([Total Revenue],  [Unique Restaurants],  0)
```

### Date Measure
```dax
Data Period (Days) = DATEDIFF(MIN([Order_Date]), MAX([Order_Date]), DAY)
```

### Constant (Gauge Target)
```dax
Orders per Customer Target = 15
```

> 💡 **DAX functions used across all 25 measures:**
> `COUNTROWS`, `SUM`, `AVERAGE`, `DISTINCTCOUNT`, `CALCULATE`, `VALUE`, `AVERAGEX`, `FILTER`, `DIVIDE`, `DATEDIFF`, `MIN`, `MAX`, `FORMAT`

---

## 6. Dashboard Pages — All 6

### Page 1 — Executive Overview
Answers: *How is Talabat performing overall?*
- 4 KPI cards: Total Orders, Total Revenue, Avg Order Value, Delivery Success Rate
- Line chart: Orders over time (daily trend over 15 days)
- Bar chart: Orders by city
- Donut: Order status split (Delivered / Cancelled / In Transit)
- Donut: Payment method split (Cash / Card / Wallet)

### Page 2 — Delivery Performance
Answers: *How fast and reliable are deliveries?*
- 4 KPI cards: Avg Delivery Time, Avg Distance, On-Time Rate, Delay Rate
- Bar chart: Avg delivery time by city (Zagazig slowest at 37.67 mins)
- Clustered bar: Delivery time by traffic level (High vs Low — less than 0.2 min difference)
- Scatter: Delivery distance vs delivery time
- Stacked bar: On-time vs delayed orders per city

### Page 3 — Revenue & Orders
Answers: *Where is revenue coming from?*
- 4 KPI cards: Total Revenue, Revenue per Customer, Revenue per Restaurant, Revenue per Order
- Bar chart: Top menu items by revenue (Shawarma #1 at EGP 3.06M)
- Column charts: Revenue by hour and by day of week
- Gauge: Orders per customer vs target of 15

### Page 4 — Restaurant & Menu Analysis
Answers: *Which restaurants and items are performing?*
- 3 KPI cards: Unique Restaurants, Top Restaurant Revenue, Top Item Revenue
- Bar chart: Top 10 restaurants by order count
- Donut: Orders by item category (9 categories)
- Leaderboard table: Restaurant ranking
- Clustered bar: Item popularity by city

### Page 5 — Operations & Traffic
Answers: *What operational patterns exist?*
- 3 KPI cards: Avg Distance, High Traffic Rate, Unique Drivers
- Map visual: Customer locations across 7 cities (latitude + longitude)
- Clustered bar: Traffic level vs avg delivery delay
- Donut: Driver vehicle split (Motorbike / Car / Bicycle)
- Matrix: Vehicle type vs traffic level performance

### Page 6 — Customer Behaviour
Answers: *When and how do customers order?*
- 4 KPI cards: Unique Customers, Orders per Customer, Revenue per Customer, Cancellation Rate
- Column charts: Orders by day of week and by hour of day
- Stacked bar: Payment method preference by city
- Bar chart: Avg order value by city

---

## 7. Key Insights

| # | Insight | Evidence |
|---|---------|----------|
| 1 | Sunday is the busiest day — 30% above weekdays | 17,317 orders on Sunday vs avg 13,300 on weekdays |
| 2 | Talabat is a true 24/7 platform — no peak hours | Every hour: 4,100–4,260 orders, flat distribution |
| 3 | Customers are highly loyal — 11.1 orders each | 9,000 customers / 100,000 orders = 11.1 repeat rate |
| 4 | All 3 payment methods equally used | Cash 33.5%, Card 33.2%, Wallet 33.3% |
| 5 | Shawarma leads revenue but margin gap is small | Shawarma EGP 3.06M vs Sushi EGP 2.93M — only 4% apart |
| 6 | All 7 cities within 3% of each other in order volume | Range: 14,044 (Mansoura) to 14,538 (Zagazig) |
| 7 | Traffic has minimal impact on delivery time | High vs Low traffic: less than 0.2 min difference |
| 8 | Vehicle type has no performance difference | Motorbike, Car, Bicycle all average 37.5 mins |
| 9 | 9.8% cancellation rate is the biggest revenue risk | 9,812 orders cancelled |

---

## 8. Recommendations

| Recommendation | Reasoning |
|----------------|-----------|
| Surge staffing on Sundays | 30% higher demand justifies temporary driver increase |
| Investigate cancellation reasons | 9,812 cancellations at 9.8% — target below 5% |
| Review Zagazig operations | Highest delay rate (50.9%) and slowest avg delivery (37.67 mins) |
| Keep all 3 payment methods | Perfect 33% split — removing any would alienate one third of customers |
| Feature Shawarma in promotions | Top revenue item with broad appeal across all cities |
| Connect to live data | Current dashboard is a static snapshot — live refresh would make it operational |

---

## 9. Power BI — Concepts Applied

### Display Folders
> Organize all measures into named folders in the data model so the field list stays clean.

```
📁 Aggregations       → Total Orders, Total Revenue, Avg Order Value ...
📁 Filter Measures    → Delivered Orders, Cancelled Orders, Delayed Orders ...
📁 Rate Measures      → Delivery Success Rate, Cancellation Rate, Delay Rate ...
📁 Per-Unit Measures  → Orders per Customer, Revenue per Restaurant ...
📁 Time Measures      → Data Period (Days)
📁 Traffic Measures   → High Traffic Rate, Avg Delivery Time High/Low Traffic
📁 Targets            → Orders per Customer Target
```

### VALUE() — Type Conversion in DAX
```dax
-- Delivery_Delay is stored as Text in the source — can't do math on it
-- VALUE() converts Text to Number inline
Delayed Orders = CALCULATE(
    COUNTROWS(talabat_enhanced_orders),
    VALUE(talabat_enhanced_orders[Delivery_Delay]) > 37
)
```

### DIVIDE() — Safe Division
```dax
-- Always use DIVIDE() instead of / to avoid division-by-zero errors
-- Third argument is the alternate result (0 means return 0 if denominator is 0)
Delivery Success Rate = DIVIDE([Delivered Orders], [Total Orders], 0)
```

### FORMAT() — Calculated Column
```dax
-- Calculated column to fix empty Day_of_Week source column
Day_of_Week_Fixed = FORMAT([Order_Date], "dddd")
-- Returns: "Monday", "Tuesday", etc.
```

### AVERAGEX() + FILTER() — Row-by-Row Aggregation
```dax
-- Average delay only for orders that are actually delayed (delay > 0)
-- FILTER() returns a filtered table, AVERAGEX() iterates over it row by row
Avg Delay (mins) = AVERAGEX(
    FILTER(talabat_enhanced_orders,
           VALUE(talabat_enhanced_orders[Delivery_Delay]) > 0),
    VALUE(talabat_enhanced_orders[Delivery_Delay])
)
```

### Gauge Visual
> Used to show Orders per Customer (11.1) against a target value (15). Visually shows how far the metric is from the goal.

### Map Visual (Page 5)
> Uses `Customer_Lat` and `Customer_Lon` columns from the dataset to plot customer locations across all 7 cities. Requires Azure Maps or ArcGIS in Power BI settings.

---

## 10. Notes & Tasks

| # | Note |
|---|------|
| 📝 | Always audit all columns before writing any DAX — bad data types cause silent wrong results |
| 📝 | `DIVIDE()` instead of `/` — non-negotiable in any production dashboard |
| 📝 | `VALUE()` is the DAX equivalent of `int()` in Python — converts text to number |
| 📝 | Display folders keep the field list clean — essential when you have 25+ measures |
| 📝 | `CALCULATE()` is the most powerful DAX function — it modifies the filter context |
| 📝 | `AVERAGEX()` + `FILTER()` = row-by-row computation on a filtered subset |
| 📝 | Static dashboards are good for learning — live connections are needed for production |
| 📝 | Always include `FORMAT()` strings so numbers display as currency, %, etc. |
| 🔧 | **Task:** Publish the Talabat dashboard to Power BI Service |
| 🔧 | **Task:** Learn `CALCULATE()` with multiple filter arguments |
| 🔧 | **Task:** Practice time intelligence: `DATEADD()`, `TOTALYTD()`, `SAMEPERIODLASTYEAR()` |
| 🔧 | **Task:** Try connecting a Power BI report to a live MySQL database |

---

*📅 Notes taken: May 21, 2026*
