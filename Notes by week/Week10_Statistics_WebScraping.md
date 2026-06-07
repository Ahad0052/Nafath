# 🐍 Week 10 — Statistics for AI & Web Scraping with Selenium
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Statistics for AI — Overview](#1-statistics-for-ai--overview)
2. [Descriptive Statistics](#2-descriptive-statistics)
3. [Probability](#3-probability)
4. [Permutations & Combinations](#4-permutations--combinations)
5. [Distributions & Sampling](#5-distributions--sampling)
6. [Confidence Intervals](#6-confidence-intervals)
7. [Hypothesis Testing](#7-hypothesis-testing)
8. [Linear Regression](#8-linear-regression)
9. [Logistic Regression](#9-logistic-regression)
10. [Web Scraping with Selenium](#10-web-scraping-with-selenium)
11. [Project — Times of Oman Scraper](#11-project--times-of-oman-scraper)
12. [Notes & Tasks](#12-notes--tasks)

---

## 1. Statistics for AI — Overview

> Statistics is the foundation of machine learning. Before a model can learn, you need to understand what the data looks like, how it's distributed, and whether patterns are real or random noise.

### Why Statistics Matters in AI/DS
| Concept | Where it shows up in ML |
|---------|------------------------|
| Mean, std, distribution | Feature scaling, EDA |
| Probability | Naive Bayes, Bayesian models |
| Confidence intervals | Model evaluation, A/B testing |
| Hypothesis testing | Feature selection, experiment design |
| Linear regression | Prediction, understanding relationships |
| Logistic regression | Classification baseline |

---

## 2. Descriptive Statistics

> Summarize and describe a dataset before doing anything else.

### Measures of Central Tendency
```python
import numpy as np

data = [12, 15, 14, 10, 18, 21, 14, 13]

mean   = np.mean(data)    # average
median = np.median(data)  # middle value — robust to outliers
mode   = 14               # most frequent value (use scipy.stats.mode)
```

### Measures of Spread
```python
std      = np.std(data)          # standard deviation — avg distance from mean
variance = np.var(data)          # std squared
iqr      = np.percentile(data, 75) - np.percentile(data, 25)  # interquartile range
rng      = np.max(data) - np.min(data)                        # range
```

### Quick Summary with Pandas
```python
import pandas as pd

df = pd.DataFrame({'values': data})
df.describe()
# returns: count, mean, std, min, 25%, 50%, 75%, max
```

---

## 3. Probability

> Probability = how likely something is to happen. Ranges from 0 (impossible) to 1 (certain).

### Basic Rules
```
P(A) = number of favorable outcomes / total outcomes

P(A or B)  = P(A) + P(B) - P(A and B)   # Addition rule
P(A and B) = P(A) × P(B|A)              # Multiplication rule
P(B|A)     = P(A and B) / P(A)          # Conditional probability
```

### Independent vs Dependent Events
- **Independent** — P(A and B) = P(A) × P(B)
- **Dependent** — the first event affects the second

### Bayes' Theorem
```
P(A|B) = P(B|A) × P(A) / P(B)
```
> 💡 Used in spam filters, medical diagnosis, and Naive Bayes classifiers.

---

## 4. Permutations & Combinations

> When order matters → Permutations. When order doesn't matter → Combinations.

### Permutations — Order Matters
```python
from math import factorial

# P(n, r) = n! / (n-r)!
# How many ways to arrange r items from n
def permutation(n, r):
    return factorial(n) // factorial(n - r)

permutation(5, 3)  # 60
```

### Combinations — Order Doesn't Matter
```python
from math import comb

# C(n, r) = n! / (r! × (n-r)!)
# How many ways to choose r items from n
comb(5, 3)  # 10
```

### Quick Comparison
| Scenario | Type | Formula |
|----------|------|---------|
| Arranging 3 books from 5 | Permutation | P(5,3) = 60 |
| Choosing 3 toppings from 5 | Combination | C(5,3) = 10 |
| Password with no repeats | Permutation | P(n, r) |
| Lottery numbers | Combination | C(n, r) |

---

## 5. Distributions & Sampling

### Normal Distribution
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Properties: symmetric, bell-shaped, mean = median = mode
# 68% of data within 1 std, 95% within 2 std, 99.7% within 3 std (Empirical Rule)

mu, sigma = 0, 1
x = np.linspace(-4, 4, 100)
y = stats.norm.pdf(x, mu, sigma)

plt.plot(x, y)
plt.title("Standard Normal Distribution")
plt.show()
```

### Z-Score — Standardizing Data
```python
# How many standard deviations a value is from the mean
z = (x - mu) / sigma

# Z-score in scipy
from scipy.stats import zscore
z_scores = zscore(data)
```

### Central Limit Theorem (CLT)
> No matter the shape of the original population, the **distribution of sample means** approaches a normal distribution as sample size increases (n ≥ 30).

This is why we can use normal distribution assumptions even with non-normal data.

### Sampling Methods
| Method | Description |
|--------|-------------|
| Random sampling | Every member has equal chance |
| Stratified sampling | Divide into groups, sample from each |
| Systematic sampling | Every nth member |
| Convenience sampling | Easiest to reach (biased — avoid in research) |

---

## 6. Confidence Intervals

> A **confidence interval** gives a range of values that likely contains the true population parameter.

### Formula (for population mean)
```
CI = x̄ ± z × (σ / √n)

Where:
  x̄ = sample mean
  z  = z-score for confidence level (1.96 for 95%, 2.576 for 99%)
  σ  = standard deviation
  n  = sample size
```

### In Python
```python
import numpy as np
from scipy import stats

data = [12, 15, 14, 10, 18, 21, 14, 13]
n    = len(data)
mean = np.mean(data)
se   = stats.sem(data)   # standard error

# 95% confidence interval
ci = stats.t.interval(
    confidence=0.95,
    df=n - 1,
    loc=mean,
    scale=se
)

print(f"95% CI: {ci}")
# e.g. (12.1, 17.4) — we are 95% confident the true mean is between 12.1 and 17.4
```

### Key Points
- **95% CI** → z = 1.96 (most common)
- **99% CI** → z = 2.576 (wider, more certain)
- Wider interval = more confidence, less precision
- Larger sample → narrower interval

---

## 7. Hypothesis Testing

> Hypothesis testing decides whether observed data provides enough evidence to reject an assumption (the null hypothesis).

### The Two Hypotheses
```
H₀ (Null Hypothesis)     — the default assumption (no effect, no difference)
H₁ (Alternative Hypothesis) — what you're trying to prove
```

### Steps
```
1. State H₀ and H₁
2. Choose significance level α (usually 0.05)
3. Calculate test statistic
4. Find p-value
5. Decision: if p-value < α → reject H₀
```

### t-Test — Comparing Means
```python
from scipy import stats

group_a = [78, 82, 85, 90, 88]
group_b = [70, 74, 80, 76, 72]

t_stat, p_value = stats.ttest_ind(group_a, group_b)

print(f"t-statistic: {t_stat:.3f}")
print(f"p-value:     {p_value:.3f}")

if p_value < 0.05:
    print("Reject H₀ — significant difference")
else:
    print("Fail to reject H₀ — no significant difference")
```

### Types of Errors
| | H₀ is True | H₀ is False |
|--|------------|-------------|
| **Reject H₀** | Type I Error (α) — False Positive | Correct ✅ |
| **Fail to Reject H₀** | Correct ✅ | Type II Error (β) — False Negative |

### Common Tests
| Test | Use Case |
|------|----------|
| One-sample t-test | Compare sample mean to a known value |
| Two-sample t-test | Compare means of two groups |
| Chi-square test | Categorical data — test independence |
| ANOVA | Compare means across 3+ groups |

---

## 8. Linear Regression

> Predicts a **continuous** output from one or more input features by fitting a straight line.

### Simple Linear Regression
```
y = mx + b

Where:
  y = predicted value
  m = slope (coefficient)
  b = intercept
  x = input feature
```

### In Python (scikit-learn)
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Example: predict salary from years of experience
X = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])
y = np.array([30, 35, 40, 45, 50, 55, 60, 65, 70, 75])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Slope:     {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
print(f"R²:        {r2_score(y_test, y_pred):.3f}")
print(f"MSE:       {mean_squared_error(y_test, y_pred):.3f}")
```

### Key Metrics
| Metric | Meaning |
|--------|---------|
| **R²** | How much variance the model explains (0–1, higher = better) |
| **MSE** | Mean Squared Error — average of squared prediction errors |
| **RMSE** | √MSE — in the same units as y |
| **MAE** | Mean Absolute Error — average of absolute errors |

### Assumptions of Linear Regression
- Linear relationship between X and y
- Residuals are normally distributed
- No multicollinearity (for multiple regression)
- Homoscedasticity — constant variance in residuals

---

## 9. Logistic Regression

> Predicts a **binary** outcome (0 or 1) — used for classification, not regression despite the name.

### How it Works
```
Instead of predicting a value, it predicts a probability using the sigmoid function:

σ(z) = 1 / (1 + e^(-z))

Where z = mx + b (the linear equation)
Output: probability between 0 and 1
If probability ≥ 0.5 → class 1
If probability <  0.5 → class 0
```

### In Python (scikit-learn)
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

### Evaluation Metrics for Classification
| Metric | Formula | Meaning |
|--------|---------|---------|
| **Accuracy** | correct / total | Overall correctness |
| **Precision** | TP / (TP + FP) | Of predicted positives, how many were correct |
| **Recall** | TP / (TP + FN) | Of actual positives, how many were found |
| **F1 Score** | 2 × (P × R) / (P + R) | Balance of precision and recall |

### Linear vs Logistic Regression
| | Linear Regression | Logistic Regression |
|--|-------------------|---------------------|
| Output | Continuous value | Probability (0–1) → class |
| Use case | Predict salary, price, temperature | Predict spam/not spam, disease/no disease |
| Loss function | MSE | Log loss (binary cross-entropy) |
| Decision boundary | N/A | Sigmoid at 0.5 threshold |

---

## 10. Web Scraping with Selenium

> **Selenium** is a Python library that controls a real browser — useful when a website requires JavaScript to render content (BeautifulSoup can't handle that).

### Setup
```python
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Launch Chrome (headed — you see the browser)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

# Launch Chrome headless (faster, no visible window)
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
```

### Core Methods
```python
driver.get("https://example.com")          # navigate to URL
driver.find_element(By.TAG_NAME, "h1")     # find one element
driver.find_elements(By.TAG_NAME, "a")     # find all matching elements
element.get_attribute("href")              # get an attribute
element.text                               # get visible text
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll
driver.back()                              # go back
driver.quit()                              # close browser
```

### Locators (By)
| Locator | Example |
|---------|---------|
| `By.TAG_NAME` | `find_elements(By.TAG_NAME, "a")` |
| `By.XPATH` | `find_element(By.XPATH, "//meta[@name='description']")` |
| `By.CSS_SELECTOR` | `find_element(By.CSS_SELECTOR, "article img")` |
| `By.ID` | `find_element(By.ID, "main-content")` |
| `By.CLASS_NAME` | `find_element(By.CLASS_NAME, "article-title")` |

### WebDriverWait — Explicit Waits
```python
# Wait up to 10 seconds for an element to appear before erroring
wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.TAG_NAME, "h1"))
)
element = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='next']"))
)
```

> 💡 Always use `WebDriverWait` instead of `time.sleep()` where possible — it's faster and more reliable.

### Saving to CSV
```python
import pandas as pd

data = [
    {"Title": "...", "Description": "...", "Image_URL": "...", "Article_URL": "..."},
]

df = pd.DataFrame(data)
df.drop_duplicates(subset=["Article_URL"], inplace=True)
df.to_csv("output.csv", index=False, encoding="utf-8-sig")
```

---

## 11. Project — Times of Oman Scraper

> Built a multi-phase scraper that collects news articles from [timesofoman.com](https://timesofoman.com).

### Phase 1 — Collect Article Links
```python
# Crawl category pages to collect up to 1,000 unique article URLs
CATEGORY_URL = "https://timesofoman.com/category/oman/page/"
TARGET_COUNT  = 1000

seen_urls = []
page_num  = 1

while len(seen_urls) < TARGET_COUNT:
    driver.get(f"{CATEGORY_URL}{page_num}")

    # Wait for article links to appear
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '/article/')]")
    ))

    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/article/')]")

    for link in links:
        url = link.get_attribute("href")
        if url and url not in seen_urls:
            seen_urls.append(url)
        if len(seen_urls) >= TARGET_COUNT:
            break

    page_num += 1
```

### Phase 2 — Deep Scrape Each Article
```python
# For each URL: extract title, description, image, save progressively to CSV

import csv

with open("times_of_oman_1000_news.csv", "w", newline='', encoding="utf-16") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Description", "Image_URL", "Article_URL"])
    writer.writeheader()

    for i, url in enumerate(seen_urls, 1):
        driver.get(url)

        # Title
        try:
            title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        except:
            title = ""

        # Description from meta tag
        try:
            description = driver.find_element(
                By.XPATH, "//meta[@name='description']"
            ).get_attribute("content")
        except:
            description = ""

        # First article image (skip logos)
        image_url = ""
        try:
            imgs = driver.find_elements(By.CSS_SELECTOR, "article img")
            for img in imgs:
                src = img.get_attribute("src")
                if src and "logo" not in src.lower():
                    image_url = src
                    break
        except:
            pass

        writer.writerow({
            "Title": title,
            "Description": description,
            "Image_URL": image_url,
            "Article_URL": url
        })

        # Breathe every 50 articles
        if i % 50 == 0:
            time.sleep(2)
```

### Lessons Learned
- **Write to CSV progressively** — if the script crashes at article 900, you don't lose everything
- **Polite delays** (`time.sleep`) prevent rate-limiting and bans
- **Headless mode** is ~2× faster when you don't need to watch the browser
- **`drop_duplicates()`** before saving — category pages can surface the same article multiple times
- **`encoding="utf-16"`** handles Arabic and special characters safely in Windows CSV

---

## 12. Notes & Tasks

| # | Note |
|---|------|
| 📝 | Statistics and ML are inseparable — every model assumption links back to a statistical concept |
| 📝 | p-value < 0.05 → reject H₀ — but low p-value doesn't mean large effect |
| 📝 | R² tells you fit quality; doesn't tell you if the model is useful |
| 📝 | Logistic regression is a classifier — don't let the name confuse you |
| 📝 | Selenium = real browser; use it when JavaScript renders the content |
| 📝 | `WebDriverWait` over `time.sleep` — explicit wait is faster and more robust |
| 📝 | Always save to CSV progressively in long scraping jobs |
| 📝 | `encoding="utf-16"` for Arabic / non-ASCII content in Windows |
| 📝 | `--headless` Chrome option makes scraping faster when you don't need to see the browser |
| 🔧 | **Task:** Practice t-tests and chi-square tests on a real dataset from Kaggle |
| 🔧 | **Task:** Build a linear regression from scratch using only NumPy (no sklearn) |
| 🔧 | **Task:** Extend the Times of Oman scraper to handle pagination edge cases |
| 🔧 | **Task:** Add a retry mechanism to the scraper for failed article requests |
| 🔧 | **Task:** Explore `requests` + `BeautifulSoup` for static pages — faster than Selenium when JS isn't needed |

---

*📅 Notes taken: June 3, 2026*
