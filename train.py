import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
df = pd.read_csv('data/data.csv')
target_col = df.columns[-1]

# Convert categoricals and save the exact column structure
X = pd.get_dummies(df.drop(columns=[target_col]), drop_first=True)
y = df[target_col]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the model and the expected feature columns
joblib.dump(model, 'model.joblib')
joblib.dump(list(X.columns), 'columns.joblib')
print("Model and columns successfully saved!")
