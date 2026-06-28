import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

# ── 1. Generate synthetic data ──────────────────────────────────────────────
np.random.seed(0)
X = np.sort(2 * np.random.rand(100, 1) - 1, axis=0)          # 100 points in [-1, 1]
y = 2 * X**2 + X + np.random.randn(100, 1) * 0.1             # quadratic + noise

# ── 2. Plot raw data ────────────────────────────────────────────────────────
plt.figure(figsize=(8, 5))
plt.scatter(X, y, color="blue", edgecolors="black", s=40, label="Data points")
plt.title("Synthetic Dataset", fontsize=14)
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.show()

# ── 3. Linear Regression (baseline) ─────────────────────────────────────────
lin_reg = LinearRegression()
lin_reg.fit(X, y)
y_pred_lin = lin_reg.predict(X)

plt.figure(figsize=(8, 5))
plt.scatter(X, y, color="blue", edgecolors="black", s=40, label="Data points")
plt.plot(X, y_pred_lin, color="red", linewidth=2,
         label=f"Linear fit  (MSE={mean_squared_error(y, y_pred_lin):.4f})")
plt.title("Linear Regression", fontsize=14)
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.show()

print("=== Linear Regression ===")
print(f"  MSE : {mean_squared_error(y, y_pred_lin):.4f}")
print(f"  coef_: {lin_reg.coef_}")
print(f"  intercept_: {lin_reg.intercept_}")

# ── 4. Polynomial Regression (degree 3) ─────────────────────────────────────
degree = 3
poly_features = PolynomialFeatures(degree=degree, include_bias=False)
X_poly = poly_features.fit_transform(X)

poly_reg = LinearRegression()
poly_reg.fit(X_poly, y)
y_pred_poly = poly_reg.predict(X_poly)

# Smooth curve for plotting
X_plot = np.linspace(-1, 1, 300).reshape(-1, 1)
X_plot_poly = poly_features.transform(X_plot)
y_plot_poly = poly_reg.predict(X_plot_poly)

plt.figure(figsize=(8, 5))
plt.scatter(X, y, color="blue", edgecolors="black", s=40, label="Data points")
plt.plot(X_plot, y_plot_poly, color="red", linewidth=2,
         label=f"Polynomial fit (deg={degree}, MSE={mean_squared_error(y, y_pred_poly):.4f})")
plt.title(f"Polynomial Regression (degree={degree})", fontsize=14)
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.tight_layout()
plt.show()

print(f"\n=== Polynomial Regression (degree={degree}) ===")
print(f"  MSE : {mean_squared_error(y, y_pred_poly):.4f}")
print(f"  coef_: {poly_reg.coef_}")
print(f"  intercept_: {poly_reg.intercept_}")

# ── 5. Side-by-side comparison ──────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(X, y, color="blue", edgecolors="black", s=40, label="Data")
axes[0].plot(X, y_pred_lin, color="red", linewidth=2, label="Linear")
axes[0].set_title("Linear Regression", fontsize=13)
axes[0].set_xlabel("X")
axes[0].set_ylabel("y")
axes[0].legend()

axes[1].scatter(X, y, color="blue", edgecolors="black", s=40, label="Data")
axes[1].plot(X_plot, y_plot_poly, color="red", linewidth=2, label=f"Poly deg={degree}")
axes[1].set_title(f"Polynomial Regression (degree={degree})", fontsize=13)
axes[1].set_xlabel("X")
axes[1].set_ylabel("y")
axes[1].legend()

plt.suptitle("Linear vs Polynomial Regression Comparison", fontsize=15, y=1.02)
plt.tight_layout()
plt.show()
