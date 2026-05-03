import pandas as pd
import os

df = pd.read_csv("data/raw/synthetic_fraud_dataset.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Fix transaction_id
df["transaction_id"] = "synthetic_" + df["transaction_id"].astype(str)

# User id
df["user_id"] = df["user_id"].astype(str)

# Create date from hour
df["date"] = pd.to_datetime("2024-01-01") + pd.to_timedelta(df.index, unit="h")
# Amount (keep as is)
df["amount"] = df["amount"]

# No balance → placeholder
df["balance"] = 0

# Description
df["description"] = df["transaction_type"] + " " + df["merchant_category"]

# Category
df["category"] = df["transaction_type"]

# Final columns
df = df[[
    "transaction_id",
    "user_id",
    "date",
    "amount",
    "balance",
    "description",
    "category"
]]

# Sort + clean
df = df.sort_values(by=["user_id", "date"]).reset_index(drop=True)
df = df.drop_duplicates()

print(df.head())
print(df.info())

# Save
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/synthetic_clean.csv", index=False)