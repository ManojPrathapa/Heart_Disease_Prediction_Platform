import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import shap
import numpy as np

# Load data 
df = pd.read_csv('data/data.csv')
target_col = df.columns[-1]
X = df.drop(columns=[target_col])
y = df[target_col]

# Convert categorical string columns to numeric using one-hot encoding
X = pd.get_dummies(X, drop_first=True)

# Train a baseline Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Run SHAP Explainability
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# FIX: Handle SHAP 3D array format (samples, features, classes) for newer SHAP versions
if isinstance(shap_values, list):
    shap_vals = shap_values[1]
elif len(shap_values.shape) == 3:
    shap_vals = shap_values[:, :, 1] # Extract the positive class
else:
    shap_vals = shap_values

# Calculate mean absolute SHAP values for feature importance
mean_abs_shap = np.abs(shap_vals).mean(axis=0)
importance_df = pd.DataFrame({'Feature': X.columns, 'Impact (SHAP)': mean_abs_shap})
importance_df = importance_df.sort_values(by='Impact (SHAP)', ascending=True)

print("\n" + "="*50)
print("SHAP FEATURE IMPORTANCE (From Least to Most Impactful)")
print("="*50)
print(importance_df.to_string(index=False))
print("\n[PLAIN ENGLISH CONCLUSION]")
least_impactful = importance_df.head(3)['Feature'].tolist()
print(f"Based on the SHAP analysis, the factors that have the LEAST impact on predicting heart disease are: {', '.join(least_impactful)}.")
print("="*50 + "\n")
