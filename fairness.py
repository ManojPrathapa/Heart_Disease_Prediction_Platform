import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from fairlearn.metrics import MetricFrame, selection_rate

# Load data
df = pd.read_csv('data/data.csv')
target_col = df.columns[-1]
X = df.drop(columns=[target_col])
y = df[target_col]

# Convert categorical string columns to numeric
X = pd.get_dummies(X, drop_first=True)

# Train the baseline Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)
y_pred = model.predict(X)

# Define 'age' as the sensitive attribute. 
# Binning into age groups makes the Fairlearn MetricFrame output readable.
sensitive_attr = pd.cut(df['age'], bins=[0, 45, 60, 120], labels=['Young (<=45)', 'Middle (46-60)', 'Senior (>60)'])

# Calculate metrics using Fairlearn MetricFrame
metrics = {
    'accuracy': accuracy_score,
    'selection_rate': selection_rate  # Percentage of positive predictions (heart disease = 1)
}

metric_frame = MetricFrame(
    metrics=metrics,
    y_true=y,
    y_pred=y_pred,
    sensitive_features=sensitive_attr
)

print("\n" + "="*60)
print("FAIRLEARN METRICS BY AGE GROUP")
print("="*60)
print(metric_frame.by_group)
print("\n[FAIRNESS CONCLUSION]")
max_diff = metric_frame.difference(method='between_groups')['selection_rate']
print(f"The maximum difference in positive prediction rates between age groups is: {max_diff:.4f}")
print("="*60 + "\n")
