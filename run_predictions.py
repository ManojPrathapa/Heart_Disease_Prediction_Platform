import pandas as pd
import requests
import time
from datetime import datetime
import google.cloud.logging
import sys

if len(sys.argv) < 2:
    print("Usage: python3 run_predictions.py <EXTERNAL_IP>")
    sys.exit(1)

IP = sys.argv[1]
URL = f"http://{IP}/predict"

# Initialize GCP Logging client natively
client = google.cloud.logging.Client()
logger = client.logger("oppe2-heart-predictions")

# Generate 100-row random dataset from the source data (excluding the target column)
df = pd.read_csv('data/data.csv')
target_col = df.columns[-1]
df_features = df.drop(columns=[target_col])
df_sample = df_features.sample(n=100, random_state=42)

print(f"Starting 100 per-sample predictions to {URL}...")

success_count = 0
for index, row in df_sample.iterrows():
    payload = row.to_dict()
    
    # 1. Make the prediction request
    try:
        response = requests.post(URL, json=payload, timeout=5)
        response.raise_for_status()
        prediction = response.json().get("predictions", [None])[0]
        
        # 2. Structure the log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input_features": payload,
            "predicted_output": prediction
        }
        
        # 3. Send to GCP Cloud Logging
        logger.log_struct(log_entry)
        
        print(f"Request {success_count+1}/100 | Output: {prediction}")
        success_count += 1
        
    except Exception as e:
        print(f"Failed on row {index}: {e}")
        
    time.sleep(0.05) # Small delay to ensure sequential logging

print("\n" + "="*50)
print(f"Successfully processed and logged {success_count} predictions!")
print("Logs have been exported to GCP Cloud Logging under 'oppe2-heart-predictions'.")
print("="*50 + "\n")
