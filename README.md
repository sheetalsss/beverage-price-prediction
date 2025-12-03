# 🧠 Beverage Price Range Prediction using XGBoost

This project predicts a consumer’s **Price Range** based on demographic and behavioral factors such as age, income, lifestyle, and consumption habits.

---

## 🚀 Project Overview

The goal of this project is to analyze and predict beverage consumption categories using various ML algorithms and identify which model performs best.

The dataset includes:
- Demographics (Age, Gender, Zone, Occupation)
- Behavioral patterns (Consumption Frequency, Brand Awareness, Purchase Channel)
- Preferences (Packaging, Flavor, Health Concern)

After extensive preprocessing and experimentation with multiple models, **XGBoost** achieved the **highest accuracy of 93%**.

---

## 🧩 Models Tested

| Model | Accuracy | Notes |
|:------|:----------|:------|
| 🎯 **XGBoost** | **93%** | Best performer — handled feature complexity & categorical encodings effectively |
| 🧠 Light GBM | 93% | Good, but XG Boost satisfies all criteria | 
| ⚙️ Random Forest | 90% | Good, but slightly overfitted on training data |
| 💡 Logistic Regression | 80% | Baseline benchmark |
| 📈 SVM | 79% | Decent but slower on larger dataset |
| 🔍 Gaussian Naive Bayes | 58% | Struggled with correlated features |

---

## 🧰 Tech Stack

- **Language:** Python 3.13  
- **Libraries:**  
  `pandas`, `numpy`, `scikit-learn`, `xgboost`, `joblib`, `matplotlib`, `seaborn`
- **IDE:** PyCharm / VS Code  
- **Model Persistence:** `model.pkl` and `label_encoder.pkl` (via `joblib`)

---

## 🧪 Data Processing

Key transformations before model training:
1. Converted **age → age_group** (`18-25`, `26-35`, etc.)
2. Label encoded / mapped categorical features:
   - `zone`: `{'Rural':1, 'Semi-Urban':2, 'Urban':3, 'Metro':4}`
   - `income_levels`: `{'<10L':1, '10L - 15L':2, '16L - 25L':3, '26L - 35L':4, '> 35L':5}`
   - `consume_frequency`: `{'0-2 times':1, '3-4 times':2, '5-7 times':3}`
   - `preferable_consumption_size`: `{'Small (250 ml)':0, 'Large (1 L)':1, 'Medium (500 ml)':2}`
   - `awareness_of_other_brands`: `{'0 to 1':1, '2 to 4':2, 'above 4':3}`

3. Derived new features:
   - `cf_ab_score = consume_frequency / (1 + awareness)`
   - `zas_score = zone / (1 + income_levels)`
   - `bsi_1 = brand stability indicator` (based on brand + reason choice)

---

## 🧮 Model Training

```python
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
xgb_model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
xgb_model.fit(X_train, y_train)

# Evaluate
y_pred = xgb_model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"XGBoost Accuracy: {acc*100:.2f}%")

# Save model
joblib.dump(xgb_model, 'model.pkl')
```

## ⚡ Prediction Pipeline
Once trained, predictions are made via the db_helper.py file.
```python
import joblib
import pandas as pd
from data_processing import process_data  # Your preprocessing script

model = joblib.load('model.pkl')
le = joblib.load('label_encoder.pkl')

def predict(age, income_levels, consume_frequency, ...):
    processed_input = process_data(...)
    prediction = model.predict(processed_input)
    label = le.inverse_transform(prediction)[0]
    return label
```

Example run : ``` python db_helper.py ```

## 📊 Results Summary

| Metric | Value |
|:--------|:------|
| **Accuracy** | 93% |
| **Precision** | 0.91 |
| **Recall** | 0.91 |
| **F1 Score** | 0.92 |
