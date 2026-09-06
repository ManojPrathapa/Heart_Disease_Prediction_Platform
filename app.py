from fastapi import FastAPI, Request
import joblib
import pandas as pd

app = FastAPI()
model = joblib.load('model.joblib')
columns = joblib.load('columns.joblib')

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    # Handle single dictionary or list of dictionaries
    if isinstance(data, dict):
        data = [data]
        
    df = pd.DataFrame(data)
    
    # Process categorical variables exactly like training
    df = pd.get_dummies(df, drop_first=True)
    
    # Align input features with the exact columns the model expects
    for col in columns:
        if col not in df.columns:
            df[col] = 0
    df = df[columns] # Reorder to match training
    
    predictions = model.predict(df).tolist()
    return {"predictions": predictions}
