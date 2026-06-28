# 🐍 Week 13 — Introduction to Machine Learning
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [What is Machine Learning?](#1-what-is-machine-learning)
2. [Types of Machine Learning](#2-types-of-machine-learning)
3. [Model Selection & Overfitting](#3-model-selection--overfitting)
4. [Linear Regression](#4-linear-regression)
5. [Gradient Descent](#5-gradient-descent)
6. [Regularization — Lasso & Ridge](#6-regularization--lasso--ridge)
7. [Logistic Regression](#7-logistic-regression)
8. [Errors in ML & Evaluation Metrics](#8-errors-in-ml--evaluation-metrics)
9. [K-Nearest Neighbors (KNN)](#9-k-nearest-neighbors-knn)
10. [Clustering & K-Means](#10-clustering--k-means)
11. [Dimensionality Reduction](#11-dimensionality-reduction)
12. [Support Vector Machines (SVM)](#12-support-vector-machines-svm)
13. [Decision Trees](#13-decision-trees)
14. [Notes & Tasks](#14-notes--tasks)

---

## 1. What is Machine Learning?

> **Machine Learning** is the study of algorithms that improve automatically through experience — giving computers the ability to learn without being explicitly programmed.

### The Core Idea
```
Traditional Programming:  Data + Rules     → Answers
Machine Learning:          Data + Answers  → Rules
```

### When to Use ML
- Too many rules for a human to write (spam detection, image recognition)
- Rules change over time (fraud detection, recommendations)
- The environment is complex and unpredictable

---

## 2. Types of Machine Learning

### Supervised Learning
> The model learns from **labelled** data — input/output pairs.

| Task | Example | Algorithms |
|------|---------|------------|
| Regression | Predict house price | Linear Regression, Ridge, Lasso |
| Classification | Spam or not spam | Logistic Regression, KNN, SVM, Decision Tree |

### Unsupervised Learning
> The model finds **patterns** in unlabelled data.

| Task | Example | Algorithms |
|------|---------|------------|
| Clustering | Group customers by behaviour | K-Means |
| Dimensionality Reduction | Compress features | PCA |

### ML Workflow
```
1. Collect & clean data
2. Exploratory Data Analysis (EDA)
3. Feature engineering
4. Choose model
5. Train (fit on training data)
6. Evaluate (test on unseen data)
7. Tune hyperparameters
8. Deploy
```

---

## 3. Model Selection & Overfitting

### The Bias-Variance Tradeoff
| Problem | Cause | Fix |
|---------|-------|-----|
| **Underfitting** (high bias) | Model too simple | Use a more complex model |
| **Overfitting** (high variance) | Model too complex / memorized training data | Regularization, more data, simpler model |

### Train/Test Split
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 80% train, 20% test
    random_state=42     # reproducible split
)
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)   # 5-fold CV
print(scores.mean())
```

> 💡 **Rule of thumb:** If training accuracy is high but test accuracy is low → overfitting. If both are low → underfitting.

---

## 4. Linear Regression

> Predicts a **continuous** output by fitting a line (or hyperplane) through the data.

### Simple Linear Regression
```
y = mx + b

Where:
  y = predicted value (dependent variable)
  x = input feature (independent variable)
  m = slope (coefficient)
  b = intercept
```

### Multiple Linear Regression
```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

data = {
    "Hours":       [1,2,3,4,5,6,7,8,9,10],
    "Assignments": [1,2,3,3,4,5,6,6,7,8],
    "Score":       [50,55,60,65,70,78,85,90,92,95]
}
df = pd.DataFrame(data)

X = df[["Hours", "Assignments"]]
y = df["Score"]

model = LinearRegression()
model.fit(X, y)

print("Coefficients:", model.coef_)     # [m1, m2]
print("Intercept:",    model.intercept_) # b
```

### Key Metrics
| Metric | Formula | Meaning |
|--------|---------|---------|
| **R²** | 1 - SS_res/SS_tot | Variance explained (0–1, higher = better) |
| **MSE** | mean((y - ŷ)²) | Average squared error |
| **RMSE** | √MSE | Same units as y |
| **MAE** | mean(\|y - ŷ\|) | Average absolute error |

```python
from sklearn.metrics import mean_squared_error, r2_score

y_pred = model.predict(X_test)
print("R²:  ", r2_score(y_test, y_pred))
print("MSE: ", mean_squared_error(y_test, y_pred))
```

### House Price Prediction (Real Dataset)
```python
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
X, y = housing.data, housing.target

# Feature scaling before linear regression
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)
```

---

## 5. Gradient Descent

> An optimization algorithm that finds the **minimum of a loss function** by iteratively moving in the direction of the steepest descent (negative gradient).

### How It Works
```
For each epoch:
  1. Predict ŷ using current weights
  2. Compute error = ŷ - y
  3. Compute gradients (partial derivatives of loss w.r.t. weights)
  4. Update weights: w = w - lr × gradient
  5. Repeat until convergence
```

### From Scratch in Python
```python
import numpy as np

np.random.seed(42)
X = 2 * np.random.rand(100)
y = 4 + 3 * X + np.random.randn(100)   # true: y = 4 + 3x + noise

m, b = 0.0, 0.0     # init weights
lr    = 0.1         # learning rate
N     = len(X)

for epoch in range(50):
    y_pred = m * X + b
    error  = y_pred - y

    # Gradients
    dm = (2/N) * np.dot(error, X)
    db = (2/N) * np.sum(error)

    # Update
    m -= lr * dm
    b -= lr * db

    loss = (error**2).mean()
    print(f"Epoch {epoch+1:02d} | m={m:.4f}, b={b:.4f}, loss={loss:.4f}")
```

### SGD Regressor (sklearn)
```python
from sklearn.linear_model import SGDRegressor

sgd = SGDRegressor(max_iter=1000, learning_rate="constant", eta0=0.01)
sgd.fit(X_train, y_train)
```

### Key Hyperparameters
| Parameter | Effect |
|-----------|--------|
| **Learning rate (α)** | Too high → diverges; too low → slow convergence |
| **Epochs** | Number of passes over the training data |
| **Batch size** | Full batch (GD), 1 sample (SGD), mini-batch (MBGD) |

---

## 6. Regularization — Lasso & Ridge

> Regularization adds a **penalty** to the loss function to prevent overfitting by keeping weights small.

### Ridge Regression (L2)
```
Loss = MSE + α × Σ(w²)
```
- Shrinks coefficients toward zero but never exactly to zero
- Good when all features contribute somewhat

```python
from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
print("Coefficients:", ridge.coef_)
```

### Lasso Regression (L1)
```
Loss = MSE + α × Σ|w|
```
- Can shrink coefficients **exactly to zero** → automatic feature selection
- Good when many features are irrelevant

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
print("Coefficients:", lasso.coef_)   # some will be 0.0
```

### Effect of Alpha
```python
import matplotlib.pyplot as plt
import numpy as np

alphas = np.linspace(0.01, 5, 50)
ridge_coefs = [Ridge(alpha=a).fit(X, y).coef_[0] for a in alphas]
lasso_coefs = [Lasso(alpha=a).fit(X, y).coef_[0] for a in alphas]

plt.plot(alphas, ridge_coefs, label="Ridge")
plt.plot(alphas, lasso_coefs, label="Lasso")
plt.xlabel("alpha"); plt.ylabel("Coefficient Value")
plt.legend(); plt.show()
# As alpha increases: Ridge shrinks gradually, Lasso hits zero
```

### Comparison
| | Ridge (L2) | Lasso (L1) |
|--|-----------|-----------|
| Penalty | Σw² | Σ\|w\| |
| Coefficients reach zero? | No (approach zero) | Yes (exact zero) |
| Feature selection | No | Yes |
| Best for | Correlated features | Sparse features, many irrelevant |

---

## 7. Logistic Regression

> Despite the name, this is a **classification** algorithm. It predicts the probability that an input belongs to a class.

### The Sigmoid Function
```
σ(z) = 1 / (1 + e^(-z))

Where z = mx + b (the linear equation)
Output: 0 to 1 (probability)
Decision: if σ(z) ≥ 0.5 → class 1, else class 0
```

### Insurance Prediction Example
```python
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("insurance_data.csv")   # columns: age, bought_insurance

X_train, X_test, y_train, y_test = train_test_split(
    df[["age"]], df.bought_insurance, train_size=0.8
)

model = LogisticRegression()
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))       # e.g. 0.833
print("Probabilities:", model.predict_proba(X_test))   # [[P(0), P(1)], ...]
print("Predictions:", model.predict(X_test))           # [0 or 1, ...]
print("Coefficient:", model.coef_)    # slope (m)
print("Intercept:",   model.intercept_)  # bias (b)
```

### Manual Sigmoid Check
```python
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def predict(age):
    # Using learned m and b
    z = model.coef_[0][0] * age + model.intercept_[0]
    return sigmoid(z)

print(predict(35))   # < 0.5 → won't buy
print(predict(43))   # > 0.5 → will buy
```

---

## 8. Errors in ML & Evaluation Metrics

### Regression Metrics
| Metric | Code |
|--------|------|
| MSE | `mean_squared_error(y_test, y_pred)` |
| RMSE | `np.sqrt(mean_squared_error(...))` |
| MAE | `mean_absolute_error(y_test, y_pred)` |
| R² | `r2_score(y_test, y_pred)` |

### Classification Metrics
```python
from sklearn.metrics import (accuracy_score, precision_score,
                              recall_score, f1_score,
                              confusion_matrix, classification_report)

print("Accuracy: ", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:   ", recall_score(y_test, y_pred))
print("F1:       ", f1_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

### Confusion Matrix
```
            Predicted 0    Predicted 1
Actual 0  [ TN           FP ]
Actual 1  [ FN           TP ]
```

| Metric | Formula | When to prioritize |
|--------|---------|-------------------|
| **Accuracy** | (TP+TN)/total | Balanced classes |
| **Precision** | TP/(TP+FP) | Cost of false positive is high (spam filter) |
| **Recall** | TP/(TP+FN) | Cost of false negative is high (cancer detection) |
| **F1** | 2×(P×R)/(P+R) | Imbalanced classes |

### Macro vs Micro Averaging (Multi-class)
| Average | Description |
|---------|-------------|
| **Macro** | Compute metric per class, then take unweighted mean — all classes equal weight |
| **Micro** | Aggregate TP, FP, FN across all classes, then compute — weights by class size |

```python
# Multi-class example
print(classification_report(y_test, y_pred))
# Shows per-class precision/recall/F1 + macro avg + weighted avg
```

---

## 9. K-Nearest Neighbors (KNN)

> Classifies a point by looking at the **K nearest points** in the training data and taking a majority vote.

### How It Works
```
1. Choose K (number of neighbors)
2. For each new point:
   a. Compute distance to all training points (usually Euclidean)
   b. Select K nearest neighbors
   c. Assign the majority class (classification) or mean value (regression)
```

### iPhone Purchase Prediction
```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# Features: age, salary | Target: purchased (0/1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Note: ALWAYS scale before KNN — it's distance-based
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

print("Accuracy:", knn.score(X_test_scaled, y_test))
```

### Choosing K
- Small K → noisy, overfits
- Large K → smooth, underfits
- Common: use cross-validation to find best K

---

## 10. Clustering & K-Means

> **Unsupervised** — groups similar data points together without labels.

### K-Means Algorithm
```
1. Choose K (number of clusters)
2. Randomly initialize K centroids
3. Assign each point to the nearest centroid
4. Recompute centroids as mean of assigned points
5. Repeat steps 3–4 until convergence
```

### Simple K-Means (One Feature)
```python
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

X = np.array([[1],[1.5],[3],[5],[3.5],[4.5],[3.5]])

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X)

print("Labels:",    kmeans.labels_)
print("Centroids:", kmeans.cluster_centers_)
```

### Student Social Network Clustering
```python
# Features: age, estimated_salary
# No labels — purely unsupervised

kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

plt.scatter(X[:,0], X[:,1], c=kmeans.labels_, cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1],
            marker='*', s=200, c='red', label='Centroids')
plt.show()
```

### Evaluation — Inertia & Elbow Method
```python
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

plt.plot(range(1,11), inertias, 'bo-')
plt.xlabel("K"); plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()
# The 'elbow' point suggests the optimal K
```

---

## 11. Dimensionality Reduction

> Reduces the number of features while preserving as much information as possible.

### Why Reduce Dimensions?
- Removes irrelevant/redundant features
- Speeds up training
- Reduces overfitting
- Enables visualization (reduce to 2D or 3D)

### PCA — Principal Component Analysis
```python
from sklearn.decomposition import PCA

# Reduce to 2 components for visualization
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)

print("Explained variance ratio:", pca.explained_variance_ratio_)
# e.g. [0.72, 0.15] → first 2 components explain 87% of variance
```

---

## 12. Support Vector Machines (SVM)

> Finds the **maximum-margin hyperplane** that best separates two classes.

### Key Concepts
- **Support Vectors** — the data points closest to the decision boundary
- **Margin** — the distance between the hyperplane and the nearest support vectors
- **Kernel trick** — maps data to higher dimensions to make non-linear data linearly separable

### Linear SVM
```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

svm = SVC(kernel='linear', C=1.0)
svm.fit(X_train_scaled, y_train)

print("Accuracy:", svm.score(X_test_scaled, y_test))
```

### Social Network Ads (RBF Kernel)
```python
# Non-linear data → use RBF (Radial Basis Function) kernel
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train_scaled, y_train)
```

### Kernel Types
| Kernel | When to use |
|--------|------------|
| `linear` | Linearly separable data |
| `rbf` | Non-linear (most common default) |
| `poly` | Polynomial decision boundary |

---

## 13. Decision Trees

> A tree-like model that makes decisions by splitting data on features — interpretable and requires no scaling.

### How It Works
```
At each node:
  1. Find the feature + threshold that best splits the data
  2. Split: left (condition true) / right (condition false)
  3. Repeat until max_depth or leaf is pure

Split criteria: Gini impurity (classification) or MSE (regression)
```

### Decision Tree Classifier
```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

print("Accuracy:", clf.score(X_test, y_test))
print("Feature importances:", clf.feature_importances_)

# Visualize
plt.figure(figsize=(12, 6))
plot_tree(clf, feature_names=feature_names, class_names=["No","Yes"],
          filled=True, rounded=True)
plt.show()
```

### Advantages vs Disadvantages
| Advantage | Disadvantage |
|-----------|-------------|
| Easy to interpret | Prone to overfitting |
| No scaling needed | Sensitive to small data changes |
| Handles mixed types | Can create complex trees |

---

## 14. Notes & Tasks

| # | Note |
|---|------|
| 📝 | Always scale features before KNN and SVM — they are distance-based |
| 📝 | Decision Trees don't need scaling — they split on thresholds, not distances |
| 📝 | Logistic Regression is a **classifier**, not a regressor, despite the name |
| 📝 | Gradient descent finds the minimum iteratively — learning rate matters |
| 📝 | Lasso does feature selection by zeroing out coefficients; Ridge doesn't |
| 📝 | K-Means requires you to pick K in advance — use the elbow method |
| 📝 | PCA components lose interpretability — you trade meaning for dimensionality |
| 📝 | Macro avg = unweighted mean across classes; Micro avg = weighted by class size |
| 📝 | Overfitting: high train accuracy, low test accuracy → regularize or simplify |
| 📝 | XAI = Explainable AI — research topic on making ML models interpretable |
| 🔧 | **Task:** Build a multi-feature logistic regression on the HR analytics dataset |
| 🔧 | **Task:** Implement cross-validation for model selection |
| 🔧 | **Task:** Try `GridSearchCV` to tune hyperparameters automatically |
| 🔧 | **Task:** Explore `RandomForestClassifier` as an extension of Decision Trees |
| 🔧 | **Task:** Apply PCA before training and compare accuracy |

---

*📅 Notes taken: June 28, 2026*
