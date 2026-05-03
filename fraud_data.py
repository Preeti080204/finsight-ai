import pandas as pd
import os

df = pd.read_csv("data/raw/fraud_data.csv")

df.columns = df.columns.str.strip().str.lower()

# Core fields
df["transaction_id"] = "kaggle_" + df["transactionid"]
df["user_id"] = df["accountid"]
df["date"] = pd.to_datetime(df["transactiondate"], errors="coerce")

# Amount logic
df["amount"] = df["transactionamount"]
df.loc[df["transactiontype"].str.lower().isin(["debit", "withdrawal"]), "amount"] *= -1

# Balance
df["balance"] = df["accountbalance"]

# Description
df["description"] = df["transactiontype"] + " via " + df["channel"]

# Category
df["category"] = df["transactiontype"].str.lower()

# 🔥 Metadata (ALL extra features preserved)
df["metadata"] = (
    "loc:" + df["location"] +
    "|dev:" + df["deviceid"] +
    "|ip:" + df["ip address"] +
    "|merch:" + df["merchantid"] +
    "|channel:" + df["channel"] +
    "|age:" + df["customerage"].astype(str) +
    "|login:" + df["loginattempts"].astype(str)
)

# Final dataset
df = df[[
    "transaction_id",
    "user_id",
    "date",
    "amount",
    "balance",
    "description",
    "category",
    "metadata"
]]

df = df.sort_values(by=["user_id", "date"]).reset_index(drop=True)
df = df.drop_duplicates()

print(df.head())
print(df.info())

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/fraud_data.csv", index=False)