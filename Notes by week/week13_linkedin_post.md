**Week 13 of the Nafath AI & Data Science Bootcamp**

🧠 Introduction to Machine Learning

This week I took my first real step into ML — moving from writing explicit rules to building models that learn patterns from data.

📚 Topics covered:
- What is ML? Traditional Programming vs ML paradigm
- Types of ML: Supervised (regression + classification) and Unsupervised (clustering + dimensionality reduction)
- Full ML Workflow: Collect → EDA → Feature Engineering → Choose Model → Train → Evaluate → Tune → Deploy
- Bias-Variance Tradeoff, Train/Test Split, Cross-Validation

📊 Models & algorithms explored:
- Linear Regression — simple and multiple, evaluated with R², MSE, RMSE, MAE
- Gradient Descent — optimizing loss iteratively via gradients (`SGDRegressor`)
- Regularization — Ridge (L2) shrinks coefficients, Lasso (L1) zeroes them for automatic feature selection
- Logistic Regression — sigmoid function for binary classification (`predict()`, `predict_proba()`)
- K-Nearest Neighbors (KNN) — distance-based, majority vote
- K-Means Clustering — unsupervised grouping, elbow method for choosing K
- PCA — dimensionality reduction with `explained_variance_ratio_`
- Support Vector Machines (SVM) — maximum-margin hyperplane, kernels (linear, rbf, poly)
- Decision Trees — Gini/MSE split criteria, feature importances

🔧 Key takeaways:
- KNN and SVM are distance-based → always scale features first
- Decision Trees split on thresholds → no scaling needed
- Lasso performs feature selection by zeroing coefficients; Ridge does not
- Overfitting = high train accuracy, low test accuracy → regularize or simplify

All notes and code: https://github.com/Ahad0052/Nafath

Special thanks to Kulsoom Shoukat Ali and Dr. Sultan AL-Yahyai for their guidance!

#Python #DataScience #MachineLearning #AI #ScikitLearn #Bootcamp #GitHub #100DaysOfCode #Nafath #LearningInPublic
