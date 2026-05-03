import pandas as pd
import os

file_path = "data/raw/AcctStatement_XXX7829_23042026.csv"

df = pd.read_csv(file_path, encoding="latin1")

print(df.head())
print(df.columns)

df.columns = df.columns.str.strip()

df = df.rename(columns={
    "SRL NO": "transaction_id",
    "Tran Date": "date",
    "PARTICULARS": "description",
    "DR": "debit",
    "CR": "credit",
    "BAL": "balance"
})

df["balance"] = pd.to_numeric(df["balance"], errors="coerce")
df["debit"] = pd.to_numeric(df["debit"], errors="coerce").fillna(0)
df["credit"] = pd.to_numeric(df["credit"], errors="coerce").fillna(0)

df["amount"] = df["credit"] - df["debit"]

df["description"] = (
    df["description"]
    .astype(str)
    .str.lower()
    .str.replace(r"[^a-zA-Z0-9@._ ]", "", regex=True)
)

df["description"] = df["description"].str.replace(r"\d+", "", regex=True)

df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

df["user_id"] = "user_1"
df["category"] = "unknown"

df["transaction_id"] = "bank_" + df["transaction_id"].astype(str)

# ✅ Select final columns
df = df[[
    "transaction_id",
    "user_id",
    "date",
    "amount",
    "balance",
    "description",
    "category"
]]

# ✅ Sort before computing balance_diff
df = df.sort_values(by="date").reset_index(drop=True)

# ✅ Drop duplicates
df = df.drop_duplicates()
print("Duplicates:", df.duplicated().sum())

# ✅ NOW compute balance_diff (correct place)
df["balance_diff"] = df["balance"].diff().fillna(0)

print(df[["amount", "balance_diff"]].head(10))

# ✅ Mismatch check
mismatch = df[abs(df["balance_diff"] - df["amount"]) > 1]
print("Mismatch rows:", len(mismatch))

print(df.head())
print(df.info())

os.makedirs("data/processed", exist_ok=True)
# ✅ Save file
df.to_csv("data/processed/bank_clean.csv", index=False)