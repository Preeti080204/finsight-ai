import pandas as pd
import json
import os

base_path = "data/raw/"
output_file = "data/processed/transactions_fraud_clean.csv"

# =========================
# LOAD USERS
# =========================
users = pd.read_csv(base_path + "users_data.csv")
users.columns = users.columns.str.strip().str.lower()

if "user_id" in users.columns:
    users_key = "user_id"
elif "id" in users.columns:
    users_key = "id"
else:
    raise Exception("User column not found")

# =========================
# LOAD MCC AS DICT
# =========================
with open(base_path + "mcc_codes.json") as f:
    mcc = json.load(f)

mcc_map = {str(k): v for k, v in mcc.items()}

# =========================
# PREP OUTPUT FILE
# =========================
os.makedirs("data/processed", exist_ok=True)

# delete old file if exists
if os.path.exists(output_file):
    os.remove(output_file)

# =========================
# PROCESS CHUNKS
# =========================
chunks = pd.read_csv(
    base_path + "transactions_data.csv",
    chunksize=200000,
    low_memory=True
)

for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i}...")

    chunk.columns = chunk.columns.str.strip().str.lower()

    # detect user column
    if "user_id" in chunk.columns:
        user_key = "user_id"
    elif "client_id" in chunk.columns:
        user_key = "client_id"
    else:
        continue

    users_renamed = users.rename(columns={users_key: user_key})
    df = chunk.merge(users_renamed, on=user_key, how="left")

    # MCC mapping (NO MERGE)
    if "mcc" in df.columns:
        df["mcc"] = df["mcc"].astype(str)
        df["merchant_category"] = df["mcc"].map(mcc_map)
    else:
        df["merchant_category"] = "unknown"

    df["merchant_category"] = df["merchant_category"].fillna("unknown")

    # transaction_id
    if "id" in df.columns:
        df["transaction_id"] = "tf_" + df["id"].astype(str)
    else:
        df["transaction_id"] = "tf_" + df.index.astype(str)

    df["user_id"] = df[user_key].astype(str)

    
    # 🔥 FIXED DATE GENERATION (CRITICAL)
    # =========================
    df["date"] = pd.to_datetime("2024-01-01") + pd.to_timedelta(df.index + i*200000, unit="m")

    

    # amount
    if "amount" in df.columns:
        df["amount"] = df["amount"]
    elif "transactionamount" in df.columns:
        df["amount"] = df["transactionamount"]
    else:
        df["amount"] = 0

    df["balance"] = 0

    df["description"] = df["merchant_category"] + " transaction"
    df["category"] = df["merchant_category"]
    df["metadata"] = "basic"

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

    # 🔥 WRITE DIRECTLY TO FILE (KEY FIX)
    if i == 0:
        df.to_csv(output_file, index=False, mode="w")
    else:
        df.to_csv(output_file, index=False, mode="a", header=False)

print("DONE: transactions_fraud_clean.csv saved WITHOUT memory crash")