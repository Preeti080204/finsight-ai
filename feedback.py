import pandas as pd

# Example feedback storage
feedback_data = []

# Simulated user correction
feedback_data.append({
    "transaction_id": "synthetic_861",
    "correct_category": "food",
    "is_anomaly": False
})

df_feedback = pd.DataFrame(feedback_data)

df_feedback.to_csv("data/final/feedback.csv", index=False)

print("Feedback saved")