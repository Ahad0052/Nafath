# 📊 Week 4 — NumPy, Pandas & Data Visualization
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [NumPy — Arrays](#1-numpy--arrays)
2. [NumPy — Array Operations](#2-numpy--array-operations)
3. [NumPy — Slicing, Copying & Reshaping](#3-numpy--slicing-copying--reshaping)
4. [NumPy — Math, Random & np.where()](#4-numpy--math-random--npwhere)
5. [NumPy — Statistics & Aggregations](#5-numpy--statistics--aggregations)
6. [Pandas — Series](#6-pandas--series)
7. [Pandas — DataFrame](#7-pandas--dataframe)
8. [Pandas — Data Exploration](#8-pandas--data-exploration)
9. [Pandas — Filtering, Grouping & Encoding](#9-pandas--filtering-grouping--encoding)
10. [Pandas — DateTime](#10-pandas--datetime)
11. [Matplotlib — Line, Bar, Histogram, Scatter, Pie](#11-matplotlib--line-bar-histogram-scatter-pie)
12. [Seaborn & Advanced Plots](#12-seaborn--advanced-plots)
13. [Outlier Detection & Removal (IQR)](#13-outlier-detection--removal-iqr)
14. [Notes & Tasks](#14-notes--tasks)

---

## 1. NumPy — Arrays

```python
import numpy as np

# 1D array
arr = np.array([1, 2, 3, 4, 5, 7])

# 2D array
arr2 = np.array([[1, 2, 3, 4, 7],
                 [9, 8, 7, 5, 5]])

# From a list
l1 = [1, 2, 4]
arr3 = np.array(l1)

# Shape, dtype
l2 = [[1, 2, 3], [4, 5, 6]]
arr4 = np.array(l2)
print(arr4.shape)    # → (2, 3)
print(arr4.shape[0]) # → 2  (rows)
print(arr4.shape[1]) # → 3  (columns)
print(arr4.dtype)    # → int64
```

### Special Arrays
```python
np.zeros(19, 'int')        # array of zeros
np.ones(20, 'int')         # array of ones
np.ones([5, 20], 'int')    # 2D array of ones
np.empty(5)                # uninitialized array
np.eye(5)                  # identity matrix (5x5)
np.arange(8)               # [0,1,2,3,4,5,6,7]
np.arange(0, 11, 2)        # [0,2,4,6,8,10]  (start, end, step)
np.linspace(1, 10, num=5)  # 5 evenly spaced values from 1 to 10
```

---

## 2. NumPy — Array Operations

```python
arr8 = np.array([1, 2, 3])
arr9 = np.array([2, 2, 2])

print(arr8 * arr9)   # element-wise multiply → [2 4 6]
print(arr8 - 11)     # broadcast subtract    → [-10 -9 -8]
print(arr8 ** 3)     # element-wise power    → [1 8 27]
print(arr4.T)        # transpose
```

### Matrix Dot Product
```python
A = np.array([[1, 2, 3], [4, 5, 6]])      # shape (2,3)
B = np.array([[7, 8], [9, 10], [11, 12]]) # shape (3,2)
np.dot(A, B)  # → (2,2) result
```

### Concatenate & Split
```python
arr15 = np.array([1, 2, 3])
arr16 = np.array([5, 6, 7])
np.concatenate([arr15, arr16])  # → [1 2 3 5 6 7]

# Axis matters in 2D
np.concatenate([arr17, arr18], axis=0)  # stack rows (vertically)
np.concatenate([arr17, arr18], axis=1)  # stack columns (horizontally)

# Split
arr19 = np.arange(16).reshape(4, 4)
upper, lower = np.vsplit(arr19, [2])  # split at row 2
left, right  = np.hsplit(arr19, [2]) # split at col 2
```

---

## 3. NumPy — Slicing, Copying & Reshaping

```python
arr10 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(arr10[-1])     # last element
print(arr10[2:6])    # → [2 3 4 5]

# 2D slicing — [rows, cols]
arr11 = np.array([[0,1,2,3,4,5,6,7,8,9,10]] * 3)
print(arr11[0:3, 2:8])  # rows 0-2, cols 2-7

# Assign to slice
arr12 = np.arange(11)
arr12[0:5] = 999         # broadcast value into slice

# 2D column assignment
arr13[: , 0:3] = 999     # all rows, first 3 cols

# ⚠️ Slices are VIEWS (shared memory) — use .copy() to avoid this
arr12copy = arr12[6:9].copy()

# Reshape
arr14 = np.arange(1, 13).reshape(4, 3)  # 12 elements → (4,3)
```

---

## 4. NumPy — Math, Random & np.where()

### Math Functions
```python
arr22 = np.arange(1, 11)
np.sqrt(arr22)   # square root of each element
np.exp(arr22)    # e^x for each element
```

### Random
```python
np.random.randint(0, 100, 20)  # 20 random ints between 0-100
np.random.randn(3)              # 3 numbers from normal distribution
```

### `np.where()` — Conditional Selection
```python
# Syntax: np.where(condition, value_if_true, value_if_false)

# Replace negatives with 0
arr24 = np.random.randn(5, 5)
rr = np.where(arr24 < 0, 0, arr24)

# Nested np.where (like if/elif/else)
marks = np.array([100, 20, 30, 90, 70, 80, 40, 98])
grade = np.where(marks > 85,
                 np.where(marks > 95, "A+", "A"),
                 np.where(marks > 70, "B", "C"))

# Combine conditions
age = np.array([20, 38, 74, 17, 90])
bp  = np.array([120, 140, 140, 170, 190])
status = np.where((age > 60) | (bp > 140), "critical", "normal")

# Salaries with conditional bonus
salaries = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
bonuses = np.where(salaries >= 500, salaries + 100, salaries + 50)

# Patient status
patientID  = np.array([101, 102, 103, 104, 105])
heartRate  = np.array([72, 110, 95, 130, 88])
status     = np.where(heartRate > 100, "Critical", "Stable")
table      = np.array([patientID, heartRate, status]).T

# Clean zero values — replace with average
temp = np.array([30, 0, 73, 0, 67, 7, 2, 0])
filtered  = temp[temp != 0]
avetemp   = filtered.mean()
cleantemp = np.where(temp == 0, avetemp, temp)
```

---

## 5. NumPy — Statistics & Aggregations

```python
arr26 = np.array([[8, 2, 3], [2, 7, 2]])
arr26.sum(0)   # sum per column → [10, 9, 5]
arr26.sum(1)   # sum per row    → [13, 11]
arr26.mean()   # overall mean
arr26.std()    # standard deviation
arr26.var()    # variance
np.sort(arr26) # sort each row

# Boolean aggregations
arr27 = np.array([False, True, True, False])
arr27.any()    # → True  (at least one True?)
arr27.all()    # → False (all True?)

# Unique values
countries = np.array(['om','om','uae','ksa','kuwite'])
np.unique(countries)  # → ['ksa' 'kuwite' 'om' 'uae']

# Element-wise max/min between two arrays
np.maximum(a, b)
np.add(a, b)
```

### Medical Dataset Practice
```python
# columns = [age, heart_rate, cholesterol, blood_pressure]
patients_data = np.array([
    [45, 80, 200, 120],
    [60, 90, 240, 140],
    [30, 70, 180, 110],
    [50, 85, 220, 130],
    [65, 95, 260, 150]
])

patients_data.shape      # → (5, 4)
patients_data[0]         # first patient's data
patients_data[:, :1]     # all ages (column 0)
patients_data[:, 3:]     # all blood pressure values

# Find patient with max blood pressure
pressure = patients_data[:, 3:]
maxP = np.max(pressure)
for i in range(patients_data.shape[0]):
    if pressure[i] == maxP:
        print("patient at index", i, "highest pressure:", maxP)
```

---

## 6. Pandas — Series

```python
import pandas as pd

l = [1, 2, 3, 4]
series = pd.Series(l)

# Custom index
s = pd.Series(l, index=['a', 'b', 'c', 'd'])
s.index.name = "my_index"
s.name = "series_name"

# Useful attributes
s.values          # underlying numpy array
s.index           # index labels
s.values.max()
np.mean(s.values)

# Filtering
print(s[s < 3])        # values less than 3
print(2 in s)          # check if index label 2 exists

# Convert to/from dict
dic = s.to_dict()
ser = pd.Series(dic)

# NaN handling
s2 = pd.Series([10, 20, 30, None, 30, None])
print(s2.isna().sum())   # count nulls
ave = s2.mean()
s2 = s2.fillna(ave)      # fill nulls with mean

# String operations on Series
names = pd.Series(['aaaa', 'bbb', 'cccc', 'ddddd'])
names.str.upper()
names[names.str.len() > 3]  # filter by string length

# Rename index, add element
s.rename(index={'a': 'aa'}, inplace=True)
s['e'] = 2

# Sort
s.sort_values(inplace=True)
s.sort_index()

# Value counts
s.value_counts()

# Compare two Series
print(s1 == s2)
print(s1 < s2)

# Sales example
sales = pd.Series([200, 450, 300, 150, 500],
                  index=["Mon", "Tue", "Wed", "Thu", "Fri"])
print(sales.sum())
print(sales.mean())
print(sales.idxmax())          # day with highest sales
print(sales[sales > 300])      # days above 300
```

---

## 7. Pandas — DataFrame

```python
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age':  [24, 27, 22],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)
```

---

## 8. Pandas — Data Exploration

```python
df.head(2)       # first 2 rows
df.tail(1)       # last 1 row
df.info()        # dtypes, null counts, memory
df.describe()    # statistics for numeric columns
df.shape         # (rows, cols)
df.columns       # column names
df.nunique()     # unique value count per column

# Selecting data
df['Name']                      # single column (Series)
df[['Name', 'City']]            # multiple columns (DataFrame)
df.iloc[0]                      # row by integer position
df.loc[1]                       # row by label
df.iloc[0:2, 0:2]               # rows 0-1, cols 0-1
df.loc[0, "student_id"]         # single cell
df.loc[0:3, ["student_id", "age"]]  # label-based slice

# Value inspection
df['location'].unique()
df['location'].value_counts()
df['location'].count()
df.duplicated().sum()
df.isnull().sum()
df.notnull().sum()

# Null handling
df['City'].fillna(df['City'].mode()[0])

# Rename columns
df.rename(columns={'location': 'City', 'age': 'Age'}, inplace=True)

# Set a column as index
df.set_index('student_id')

# Replace values
df['location'].replace("London", "lon")
```

### Real Dataset — Kaggle (Data Science Students)
```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "sudhirsingh108/data-science-students",
    "data_science_student_marks.csv"
)

df.describe()
df.head()
df.info()
df.nunique()
df['sql_marks'].mean()
df['python_marks'].idxmax()
```

---

## 9. Pandas — Filtering, Grouping & Encoding

### Filtering
```python
df[df['age'] > 23]                             # simple filter
df[(cond1) & (cond2)]                          # multiple conditions
df[df['City'].isin(['Sydney', 'Tokyo'])]        # isin filter
df[df['Age'].between(22, 24)]                   # between filter

above95 = df[df['python_marks'] > 95].shape[0]
total   = df.shape[0]
percent = above95 / total * 100
```

### Encoding (Text → Numbers for ML)
```python
df['Fuel-encoding'] = df['Fuel type'].map({
    "Petrol":     0,
    "Diesel":     1,
    "Electrical": 2
})

df['Key-encoding'] = df['Spare key'].map({
    "Yes": 1,
    "No":  0
})
```

### Map / Lambda on Column
```python
df['python_pass'] = df['python_marks'].map(lambda x: 'pass' if x >= 80 else 'fail')
```

### GroupBy
```python
locgro = df.groupby('City')
locgro['sql_marks'].mean()
locgro['python_marks'].max()['Paris']
locgro['python_marks'].agg(['mean', 'std', 'count', 'max'])

# Cars dataset
avePPBrand = df.groupby('Model Name')
avePPBrand['Price'].mean()

fuel_group = df.groupby("Fuel type")
fuel_group["Price"].mean()

Transmission_group = df.groupby("Transmission")
Transmission_group["Price"].agg(["mean", "max", "min", "count"])
```

### Correlation
```python
n = df.select_dtypes(include='number')  # numeric columns only
n.corr()
```

---

## 10. Pandas — DateTime

```python
df['Date'] = pd.to_datetime(df['Date'])

df['Year']    = df['Date'].dt.year
df['Month']   = df['Date'].dt.month
df['Day']     = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.day_name()
```

---

## 11. Matplotlib — Line, Bar, Histogram, Scatter, Pie

```python
import matplotlib.pyplot as plt
```

### Line Plot
```python
plt.plot(xx, yy, color='Orange', linestyle='dotted', marker='*', label='Sales')
plt.plot(xx, yy2, color='Blue', linestyle='--', marker='*', label='New Y')
plt.title("Sales in Dates")
plt.xlabel("Dates", color="Blue")
plt.ylabel("Sales", color="Blue")
plt.legend()
plt.gcf().autofmt_xdate()   # auto-rotate date labels
plt.show()
```

### Bar Chart
```python
# Vertical
plt.bar(xx, yy, color=['Yellow', 'Green'], width=0.3)

# Horizontal
plt.barh(xx, yy)

# Grouped bar from DataFrame
df1.plot(x="Students", kind="bar", rot=30, edgecolor="Green")
plt.ylabel("marks")
plt.show()
```

### Histogram
```python
plt.hist(n['Price'], bins=50, color='SkyBlue', edgecolor='black', alpha=0.9)
plt.axvline(n['Price'].mean(),   color='LightGreen', linestyle='dashed', linewidth=2, label='mean')
plt.axvline(n['Price'].median(), color='DarkGreen',  linestyle='dashed', linewidth=2, label='median')
plt.axvline(n['Price'].max(),    color='red',         linestyle='dashed', linewidth=5, label='max')
plt.axvline(n['Price'].min(),    color='Blue',        linestyle='dashed', linewidth=5, label='min')
plt.legend()
plt.show()
```

### Scatter Plot
```python
plt.scatter(xx4, yy4, s=n['Price']/19000, color='Red', marker='+')

# With color gradient
plt.scatter(xx3, yy3, s=[100,200,300,400,500,600],
            edgecolor='black', c=[50,100,200,400,800,1600], cmap='viridis')
plt.colorbar()
plt.show()
```

### Pie Chart
```python
Transmission_counts = df['Transmission'].value_counts().reset_index()
plt.pie(Transmission_counts['count'],
        labels=Transmission_counts['Transmission'],
        startangle=180,
        autopct="%1.3f%%",
        wedgeprops={'width': 0.5, 'edgecolor': 'b'})
plt.show()

# With explode
explode = [0.1, 0.2, 0]
plt.pie(fuel_counts['count'], labels=fuel_counts['Fuel type'],
        explode=explode, startangle=180, autopct="%1.1f%%")
plt.show()
```

### Box Plot
```python
plt.boxplot(
    [df["Price"], df["Engine capacity"]],
    labels=["Price", "Engine capacity"],
    whis=[0, 100],           # whiskers to min/max
    patch_artist=True,       # fill boxes with color
    showmeans=True,
    boxprops=dict(facecolor="lightblue", color='yellow'),
    medianprops=dict(color="black"),
    whiskerprops=dict(color='brown'),
    capprops=dict(color="black")
)
plt.yscale('log')   # log scale when values differ greatly
plt.show()
```

---

## 12. Seaborn & Advanced Plots

```python
import seaborn as sns

# Heatmap (correlation matrix)
corr = df.corr()
sns.heatmap(corr,
            annot=True,
            annot_kws={"size": 10},
            vmin=-1,
            vmax=1,
            linewidth=0.5,
            cmap="coolwarm")
plt.show()

# Violin plot
df_iris = sns.load_dataset("iris")
sns.violinplot(x=df_iris["species"], y=df_iris["sepal_length"])

# Bubble chart (scatter with size)
from gapminder import gapminder
data = gapminder[gapminder.year == 2007]
sns.scatterplot(data=data, x="gdpPercap", y="lifeExp",
                size="pop", legend=False, sizes=(20, 2000))
plt.show()
```

---

## 13. Outlier Detection & Removal (IQR)

> **IQR Method:** anything below `Q1 - 1.5*IQR` or above `Q3 + 1.5*IQR` is an outlier.

```python
data = np.array([12, -20, 1, 4, -4, 6, 20, 9, 10])

q1  = np.quantile(data, 0.25)
q2  = np.quantile(data, 0.5)   # median
q3  = np.quantile(data, 0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

# Filter out outliers
clean = data[(data >= lower) & (data <= upper)]

# Find outliers
outliers = data[(data < lower) | (data > upper)]

# Replace outliers with boundary values (capping)
data = np.where(data < lower, clean.min(), data)
data = np.where(data > upper, clean.max(), data)
```

### IQR on a DataFrame column
```python
employees = pd.DataFrame({
    "name":   ["ahmed", "ali", "muna", "reem", "mohammed"],
    "salary": [450, 400, 500, 2000, 50]
})

q1    = np.quantile(employees["salary"], 0.25)
q3    = np.quantile(employees["salary"], 0.75)
iqr   = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

clean_df = employees[(employees["salary"] > lower) & (employees["salary"] < upper)]
outliers = employees[(employees["salary"] > upper) | (employees["salary"] < lower)]

# Cap and put back
new_salary = np.where(employees["salary"] > upper, clean_df["salary"].max(), employees["salary"])
new_salary = np.where(employees["salary"] < lower, clean_df["salary"].min(), new_salary)
employees["salary"] = new_salary
```

---

## 14. Notes & Tasks

| # | Note |
|---|------|
| 📝 | NumPy arrays are **faster** than Python lists — operations are vectorized |
| 📝 | Array slices are **views** (share memory) — use `.copy()` to avoid bugs |
| 📝 | `axis=0` operates on **rows**, `axis=1` operates on **columns** |
| 📝 | `iloc` = integer position \| `loc` = label-based |
| 📝 | Always `select_dtypes(include='number')` before correlation |
| 📝 | IQR is the standard method to detect and handle outliers |
| 🔧 | **Task:** Read about `MinMaxScaler` and `StandardScaler` from `sklearn` |
| 🔧 | **Task:** Read about label encoding vs one-hot encoding |
| 🔧 | **Assignment:** Maze game project — implement with UI |

---

*📅 Notes taken: April 19–23, 2026*
