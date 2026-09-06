# Deliverable 5: Per-Sample Prediction with Logging

## Objective
Generate a 100-row random dataset and log individual predictions to GCP Cloud Logging.

## Results
- **Script**: `run_predictions.py` successfully extracted 100 random samples.
- **Execution**: 97 predictions returned successfully. 3 rows were skipped due to natural `nan` (Not-a-Number) values in the clinical data, demonstrating proper exception handling without API crashes.
- **Observability**: All successful requests were structured as JSON and exported to GCP Cloud Logging under the logName `oppe2-heart-predictions`.
