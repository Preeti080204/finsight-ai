import pandas as pd
import os

# Load dataset (optimized dtypes)
df = pd.read_csv(
    "data/raw/paysim.csv",
    dtype={
        "type": "category",
        "nameOrig": "category",
        "nameDest": "category"
    }
)

# 🔥 FIX: clean column names (important)
df.columns = df.columns.str.strip().str.lower()

print(df.columns)

# Create transaction_id
df["transaction_id"] = "paysim_" + df.index.astype(str)

# User ID
df["user_id"] = df["nameorig"]

# Convert step → date
df["date"] = pd.to_datetime("2024-01-01") + pd.to_timedelta(df["step"], unit="h")

# ✅ FAST amount logic (vectorized)
df["amount"] = df["amount"]
df.loc[df["type"].isin(["CASH_OUT", "PAYMENT", "TRANSFER"]), "amount"] *= -1

# Balance
df["balance"] = df["newbalanceorig"]

# Description (vectorized, fast)
df["description"] = df["type"].str.lower() + " to " + df["namedest"].str[:5]

# Category
df["category"] = df["type"].str.lower()

# Select required columns
df = df[[
    "transaction_id",
    "user_id",
    "date",
    "amount",
    "balance",
    "description",
    "category"
]]

# Sort properly (important for behavior modeling)
df = df.sort_values(by=["user_id", "date"]).reset_index(drop=True)

# Remove duplicates
df = df.drop_duplicates()
print("Duplicates:", df.duplicated().sum())


# Save output
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/paysim_clean.csv", index=False)