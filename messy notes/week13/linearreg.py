import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

# 1. Generate non-linear dummy data (y = 0.5*x^2 + x + 2 + noise)
np.random.seed(42)
X = np.random.rand(100, 1) * 6 - 3  # 100 points between -3 and 3
y = 0.5 * X**2 + X + 2 + np.random.randn(100, 1) * 0.5

# 2. Split data into training and validation sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Create a Polynomial Regression Pipeline (Degree 2)
# This automatically handles transforming the data and feeding it to the linear model.
degree = 2
poly_model = make_pipeline(
    PolynomialFeatures(degree=degree, include_bias=False),
    LinearRegression()
)

# 4. Train the model
poly_model.fit(X_train, y_train)

# 5. Predict and Evaluate
y_pred = poly_model.predict(X_test)

print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred):.4f}")
print(f"R-squared (R2 Score): {r2_score(y_test, y_pred):.4f}")

# 6. Visualize the results
X_plot = np.linspace(-3, 3, 100).reshape(-1, 1)
y_plot = poly_model.predict(X_plot)

plt.scatter(X_train, y_train, color="blue", label="Training Data", alpha=0.6)
plt.scatter(X_test, y_test, color="green", label="Test Data", alpha=0.6)
plt.plot(X_plot, y_plot, color="red", linewidth=2, label=f"Polynomial Fit (deg={degree})")
plt.xlabel("X")
plt.ylabel("y")
plt.title("Polynomial Regression with Scikit-Learn")
plt.legend()
plt.show()
