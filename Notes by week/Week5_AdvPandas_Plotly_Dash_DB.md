# 🐍 Week 5 — Advanced Pandas, Plotly, Dash, Altair & Database Design
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Geographic Map Visualization (Basemap)](#1-geographic-map-visualization-basemap)
2. [Multi-Index DataFrames](#2-multi-index-dataframes)
3. [Merge & Join](#3-merge--join)
4. [df.query()](#4-dfquery)
5. [pd.cut() & pd.qcut()](#5-pdcut--pdqcut)
6. [Plotly — Interactive Charts](#6-plotly--interactive-charts)
7. [Plotly — Animated Charts](#7-plotly--animated-charts)
8. [Dash — Interactive Dashboard](#8-dash--interactive-dashboard)
9. [Altair — Declarative Charts](#9-altair--declarative-charts)
10. [Database Design & DBMS](#10-database-design--dbms)
11. [ERD — Entity Relationship Diagram](#11-erd--entity-relationship-diagram)
12. [Notes & Tasks](#12-notes--tasks)

---

## 1. Geographic Map Visualization (Basemap)

```python
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = 15, 10

# Draw base world map
m = Basemap(llcrnrlon=-180, llcrnrlat=-65, urcrnrlon=180, urcrnrlat=80, projection='merc')
m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
m.fillcontinents(color='grey', alpha=0.3)
m.drawcoastlines(linewidth=0.1, color="white")
```

### Plot Student Locations as Bubbles
```python
coords = {
    'Sydney':      [151.20, -33.86],
    'Tokyo':       [139.65,  35.67],
    'Berlin':      [ 13.40,  52.52],
    'London':      [ -0.12,  51.50],
    'New York':    [-74.00,  40.71],
    'Los Angeles': [-118.24, 34.05],
    'Paris':       [  2.35,  48.85]
}

city_counts = df.groupby('location').size().reset_index(name='count')
city_counts['lon'] = city_counts['location'].map(lambda x: coords.get(x, [None])[0])
city_counts['lat'] = city_counts['location'].map(lambda x: coords.get(x, [None, None])[1])
city_counts = city_counts.dropna()

plt.figure(figsize=(15, 10))
m = Basemap(llcrnrlon=-180, llcrnrlat=-65, urcrnrlon=180, urcrnrlat=80, projection='merc')
m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
m.fillcontinents(color='grey', alpha=0.3, zorder=1)
m.drawcoastlines(linewidth=0.1, color="white", zorder=1)

# ⚠️ Must convert lon/lat through m() before plotting
x, y = m(city_counts['lon'].values, city_counts['lat'].values)

m.scatter(x, y,
          s=city_counts['count'] * 100,  # bubble size = number of students
          c='red',
          alpha=0.7,
          edgecolor='black',
          zorder=5)

plt.title("Student Locations", fontsize=15)
plt.show()
```

---

## 2. Multi-Index DataFrames

> A **Multi-Index** allows a DataFrame to have multiple levels of row labels — useful for hierarchical data (e.g. City → Quarter → ID).

```python
index = pd.MultiIndex.from_tuples([
    ('New York',    'Q1', 'one'), ('New York',    'Q1', 'two'),
    ('Los Angeles', 'Q1', 'one'), ('Los Angeles', 'Q1', 'two'),
    ('Chicago',     'Q2', 'one'), ('Chicago',     'Q2', 'two'),
    ('New York',    'Q2', 'one'), ('New York',    'Q2', 'two')
], names=['City', 'Quarter', 'ID'])

df_multi = pd.DataFrame({
    'Sales':     np.round(np.random.uniform(100, 500, 8), 2),
    'Profit(%)': np.round(np.random.uniform(0, 0.35, 8), 2),
    'Quantity':  np.random.randint(1, 20, 8)
}, index=index)
```

### Selecting from Multi-Index
```python
df_multi.loc["New York", "Q1"]                         # all rows for NY Q1
df_multi.loc["Chicago"]["Sales"]                        # Chicago Sales (way 1)
df_multi.loc["Chicago", "Sales"]                        # Chicago Sales (way 2)
df_multi.loc[("Chicago", "Q2"), 'Profit(%)']            # specific cell
df_multi.loc[("New York", "Q2"), ['Profit(%)', 'Quantity', 'Sales']]  # multiple cols

# Select by third level (ID = 'one') using slice(None) as wildcard
df_multi.loc[(slice(None), slice(None), 'one'), :]
```

### Filtering & Aggregating
```python
df_multi.loc[df_multi['Sales'] > 300]           # filter by value
df_multi.loc[df_multi['Quantity'] < 10]['Quantity']

# Row with max sales
idx = df_multi["Sales"].idxmax()
df_multi.loc[idx]

# Average sales per city
df_multi.groupby("City")['Sales'].mean()
df_multi.groupby(['Quarter']).size()
df_multi.groupby(['Quarter']).count()
```

---

## 3. Merge & Join

> **merge** = SQL-style join on a column | **join** = join on the index

### merge() — All Join Types
```python
df1 = pd.DataFrame({
    'EmployeeID': [1, 2, 3, 4],
    'Name':       ['Alice', 'Bob', 'Charlie', 'David'],
    'Department': ['HR', 'IT', 'Finance', 'IT']
})
df2 = pd.DataFrame({
    'EmployeeID': [2, 4, 3, 5],
    'Salary':     [70000, 80000, 60000, 90000]
})

pd.merge(df1, df2, on='EmployeeID', how='inner')   # only matching rows
pd.merge(df1, df2, on='EmployeeID', how='left')    # all df1 rows, NaN if no match in df2
pd.merge(df1, df2, on='EmployeeID', how='right')   # all df2 rows, NaN if no match in df1
pd.merge(df1, df2, on='EmployeeID', how='outer')   # all rows from both
pd.merge(df1, df2, how='cross')                    # every combination (cartesian product)
```

> 💡 **axis reference:**
> - `axis=0` → stack on top of each other (rows)
> - `axis=1` → place side by side (columns)

### join() — Index-Based
```python
df1.set_index('EmployeeID', inplace=True)
df2.set_index('EmployeeID', inplace=True)

df1.join(df2, how='inner')
df1.join(df2, how='left')
df1.join(df2, how='right')
```

---

## 4. df.query()

> A cleaner, SQL-like way to filter DataFrames.

```python
df.query("Salary > 80000 or Department == 'IT'")
df_multi.query("Sales > 200")
df_multi.query("Sales > 200 and Quantity > 5")
```

---

## 5. pd.cut() & pd.qcut()

### pd.cut() — Custom Bins
```python
# Manually define bin edges and labels
bins   = [0, 60000, 70000, 800000]
labels = ['low', 'medium', 'high']

merged_df['salary_category'] = pd.cut(merged_df['Salary'], bins=bins, labels=labels)
```

### pd.qcut() — Quantile-Based Bins
```python
# Split into equal-frequency buckets
pd.qcut(df2["Salary"], q=2, precision=1)
```

> 💡 **cut vs qcut:**
> - `pd.cut` → equal-width intervals (you define the boundaries)
> - `pd.qcut` → equal-frequency intervals (each bin has the same number of rows)

---

## 6. Plotly — Interactive Charts

```python
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'colab'

df = px.data.gapminder()
df_2007 = df[df['year'] == 2007]
```

### Scatter Plot
```python
fig = px.scatter(
    df_2007,
    x='gdpPercap',
    y='lifeExp',
    color='continent',
    size='pop',
    hover_name='country',
    hover_data={'gdpPercap': ':,.0f', 'lifeExp': ':.1f', 'pop': ':,.0f'},
    log_x=True,
    title='GDP per capita vs Life expectancy (2007)',
    labels={'gdpPercap': 'GDP per capita (USD)', 'lifeExp': 'Life expectancy (years)'}
)
fig.update_layout(height=520, legend_title_text='Continent',
                  font=dict(family='Arial', size=13))
fig.show()
```

### Horizontal Bar Chart
```python
df_avg = (
    df[df['year'] == 2007]
    .groupby('continent', as_index=False)['lifeExp']
    .mean()
    .sort_values('lifeExp')
)
fig = px.bar(
    df_avg,
    x='lifeExp', y='continent',
    orientation='h',
    color='continent',
    text_auto='.1f',
    title='Average life expectancy by continent (2007)'
)
fig.update_traces(textposition='outside')
fig.update_layout(showlegend=False, xaxis_range=[40, 85], height=380)
fig.show()
```

### Line Chart
```python
countries = ['China', 'India', 'United States', 'Brazil', 'Nigeria']
df_sub = df[df['country'].isin(countries)]

fig = px.line(
    df_sub,
    x='year', y='lifeExp',
    color='country',
    markers=True,
    title='Life expectancy trends 1952–2007'
)
fig.update_xaxes(tickvals=df['year'].unique())
fig.update_layout(hovermode='x unified', height=460)
fig.show()
```

---

## 7. Plotly — Animated Charts

```python
fig = px.scatter(
    df,
    x='gdpPercap',
    y='lifeExp',
    animation_frame='year',       # each frame = one year
    animation_group='country',    # keeps point identity consistent across frames
    color='continent',
    size='pop',
    hover_name='country',
    log_x=True,
    range_x=[200, 100000],        # fix axes so they don't rescale per frame
    range_y=[25, 90],
    title='World development 1952–2007'
)

# Slow the animation down (ms per frame)
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300
fig.update_layout(height=540)
fig.show()
```

---

## 8. Dash — Interactive Dashboard

> **Dash** = a Python framework for building web dashboards powered by Plotly. No JavaScript needed.

```python
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()
continents = sorted(df['continent'].unique())

app = dash.Dash(__name__)

# Layout = the structure of the web page
app.layout = html.Div([
    html.H2('Gapminder Explorer', style={'fontFamily': 'Arial'}),
    dcc.Dropdown(
        id='continent-dropdown',
        options=[{'label': c, 'value': c} for c in continents],
        value='Europe',
        clearable=False,
        style={'width': '240px', 'marginBottom': '12px'}
    ),
    dcc.Graph(id='scatter-chart')
])

# Callback = connects input (dropdown) → output (graph)
@app.callback(
    Output('scatter-chart', 'figure'),
    Input('continent-dropdown', 'value')
)
def update_chart(selected_continent):
    filtered = df[(df['continent'] == selected_continent) & (df['year'] == 2007)]
    fig = px.scatter(
        filtered,
        x='gdpPercap', y='lifeExp',
        size='pop', hover_name='country',
        log_x=True,
        title=f'{selected_continent} — 2007'
    )
    fig.update_layout(height=480)
    return fig

if __name__ == '__main__':
    app.run(debug=True)   # debug=True → auto-reload on save
```

> 💡 **Dash structure:**
> - `html.Div`, `html.H2` → HTML elements
> - `dcc.Dropdown`, `dcc.Graph` → interactive Dash components
> - `@app.callback` → the reactive logic that updates the chart when input changes

---

## 9. Altair — Declarative Charts

```python
import altair as alt
import pandas as pd

d = pd.DataFrame({
    'Website': ['StackOverflow', 'FreeCodeCamp', 'GeeksForGeeks', 'MDN', 'CodeAcademy'],
    'Score':   [65, 50, 99, 75, 33]
})

chart = alt.Chart(d).mark_bar().encode(
    x='Website',
    y='Score'
)
chart
```

> 💡 Altair reads like a sentence: *"Take this data, draw bars, encode x as Website and y as Score."*
> Compare this to Matplotlib where you'd need multiple lines of setup code for the same result.

---

## 10. Database Design & DBMS

### What is a DBMS?
> A **Database Management System** is software that manages databases. It lets you define, construct, manipulate, maintain, and share data.

**4 core operations of a DBMS:**
1. **Define** — set data types and restrictions
2. **Construct** — store data in a structured way (e.g. MySQL)
3. **Manipulate** — query, update, generate reports
4. **Maintain** — allow the system to grow and change

**Key DBMS concepts:**
- **Metadata** — data about the data (column names, types, etc.)
- **Application program** — software that uses the database
- **Query** — a request for data (e.g. SQL SELECT)
- **Transaction** — a unit of work (e.g. a bank transfer)
- **Protection** — access control and security

### Database Design Process
```
1. Requirements specification & analysis
   → Ask questions, document everything

2. Conceptual design
   → Draw an ERD diagram
   → [Student] ──/has\── (Courses)
     rectangle  diamond   oval

3. Logical design
   → Define tables, columns, relationships

4. Physical design
   → Actual implementation in a DBMS (MySQL, PostgreSQL, etc.)
```

---

## 11. ERD — Entity Relationship Diagram

> An **ERD** is a diagram that shows entities (things), their attributes (properties), and how they relate to each other.

> ⚠️ ERDs cannot have cycles — they cause deadlocks, increased complexity, and harder maintenance.

### Entities
| Type | Description | Symbol |
|------|-------------|--------|
| Strong entity | Has its own primary key, independent | Rectangle `[ ]` |
| Weak entity | No primary key, depends on another entity | Double rectangle `[[ ]]` |

### Attributes
| Type | Description | Symbol |
|------|-------------|--------|
| Key attribute | Primary key (underlined) | Oval with underlined text |
| Composite attribute | Made of sub-attributes | Oval connected to smaller ovals |
| Multi-valued attribute | Can have multiple values (e.g. phone numbers) | Double oval `(( ))` |
| Derived attribute | Calculated from another attribute (e.g. age from DOB) | Dotted oval |

### Relationships
**Degree** (number of entities in the relationship):
- Unary → 1 entity
- Binary → 2 entities *(most common)*
- Ternary → 3 entities
- N-ary → N entities

**Cardinality:**
| Type | Notation |
|------|----------|
| One-to-one | `1 ── 1` |
| One-to-many | `1 ── M` (also: `\|<`) |
| Many-to-many | `M ── M` |

**Participation constraint:**
- **Total participation** — every entity must participate in the relationship (double line)
- **Partial participation** — not required (single line)

### Keys
| Key | Description |
|-----|-------------|
| Primary key | Uniquely identifies each row |
| Composite key | Two or more columns together form the key |
| Super key | Any set of columns that uniquely identifies a row |
| Surrogate key | System-generated key (e.g. auto-increment ID) |
| Foreign key | Links to the primary key of another table (placed on the "many" side) |

---

## 12. Notes & Tasks

| # | Note |
|---|------|
| 📝 | `pd.merge()` joins on a **column**, `.join()` joins on the **index** |
| 📝 | `pd.cut` = equal-width bins \| `pd.qcut` = equal-frequency bins |
| 📝 | Plotly Express (`px`) is the high-level API — use it first |
| 📝 | Dash `@app.callback` is the reactive core — input changes trigger output updates |
| 📝 | Altair code reads like a sentence describing the chart |
| 📝 | ERD circles (cycles) cause deadlocks — always use trees |
| 🔧 | **Task:** Install and explore `dash` locally |
| 🔧 | **Task:** Read about surrogate keys and when to use them |
| 🔧 | **Task:** Practice drawing ERDs for real-world scenarios (library, hospital, school) |

---

*📅 Notes taken: April 21–29, 2026*
