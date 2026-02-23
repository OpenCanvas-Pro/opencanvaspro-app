# 📘 Glossary — OpenCanvas Pro

![Glossary](https://img.shields.io/badge/Glossary-ML%20Terminology-blue)
![Education](https://img.shields.io/badge/Education-Technical%20Reference-green)
![Autonomous ML](https://img.shields.io/badge/Context-Autonomous%20ML-purple)

**Last Updated — 23 February 2026**

This glossary provides key terminology used within OpenCanvas Pro and modern machine learning workflows.

---

## Artificial Intelligence (AI)

A field of computing that seeks to create systems capable of performing tasks that would normally require human intelligence, such as pattern recognition, decision-making, and prediction.

---

## Machine Learning

A subfield of AI in which models learn patterns from data, without being explicitly programmed for each rule.

In OpenCanvas Pro, Machine Learning is applied automatically (AutoML).

---

## AutoML (Automated Machine Learning)

- Data preparation
- Algorithm selection
- Hyperparameter tuning
- Metric evaluation

➡️ The goal is to **reduce complexity and time** while maintaining quality.

---

## Algorithm

A set of mathematical rules used to learn patterns in data.

Common examples:

Random Forest
XGBoost
LightGBM
Logistic Regression
AutoML automatically tests various algorithms.

---

## Target Variable

The column that the model attempts to predict.

Examples:

Survivors (Titanic)
Price
Churn (Subscription Cancellation Rate)
Fraud

---

## Dataset

A set of structured data, usually in tabular format (rows and columns), used to train and test models.

Supported Formats:

- CSV
- Parquet
  
---

## Training

The process by which the model learns patterns from historical data.

Typically involves:

Training data
Validation data
Performance metrics

---

## Prediction (Inference)

Using the trained model to generate predictions on **new data**, never seen during training.

---

## Classification

Type of problem where the model predicts categories.

###🔹 Binary Classification
Two possible classes.

Examples:

- Yes / No
- Fraud / Non-fraud
- 0 / 1

###🔹 Multiclass Classification
More than two classes.

Examples:

- Type of flower
- Product category
- Risk class (low, medium, high)

---

## 📈 Regression

Type of problem where the model predicts continuous numerical values.

Examples:

- Property prices
- Demand
- Agricultural production
- Temperature

---

### 🧠 Clustering

A type of unsupervised learning where the model identifies natural groups in the data, without a target variable.

Examples:

- Customer segmentation
- Behavioral patterns
- Geographic clustering

---

### 🚨 Anomaly Detection
Identification of data that deviates from the expected pattern.

Examples:

- Fraud
- Sensor failures
- Atypical behaviors

---

### ⏱️ Time Series
Problems where the data has a temporal order.

Examples:

- Monthly sales
- Energy consumption
- Financial forecasts
-  Agricultural production over time

---

### 📏 Metrics
Indicators used to assess the quality of the model.

Classification
- Accuracy
- Precision
- Recall
- F1-Score

- AUC
- Regression
- R²
- MAE
- RMSE
- MAPE

---

## Preprocessing

Steps to prepare the data before training, such as:

- handling missing values
- excluding irrelevant columns (IDs, data leaks)
- type conversion
- feature engineering

---

## Feature (Attribute)

Column used as input by the model to learn patterns.

---

## Feature Engineering

Creation or transformation of features to improve model performance.

Example:

- Extract year/month from a date
- Create derived indicators

---

## Data Contract

Structured metadata describing dataset transformations and integrity.

---

## 🧾 Kaggle Submission

File in the format required by Kaggle competitions, usually containing:

- an ID column
- a prediction column
  
OpenCanvas Pro automatically generates Kaggle-ready files.

---

## 🔐 Cloud Dependency

Technical dependence on a specific cloud provider, making it difficult to migrate or reuse templates.

➡️ OpenCanvas Pro avoids cloud dependency by design.

---

© 2026 OpenCanvas Pro — All rights reserved.
