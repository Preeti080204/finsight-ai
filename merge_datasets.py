import pandas as pd
import os
import re
from categorize import categorize_transaction

base_path = "data/processed/"

# ======================
# LOAD DATA
# ======================

bank = pd.read_csv(base_path + "bank_clean.csv")
paysim = pd.read_csv(base_path + "paysim_clean.csv")
synthetic = pd.read_csv(base_path + "synthetic_clean.csv")
kaggle = pd.read_csv(base_path + "fraud_data.csv")
fraud = pd.read_csv(base_path + "transactions_fraud_clean.csv")

# ======================
# ENSURE SCHEMA
# ======================

def ensure_schema(df):
    if "metadata" not in df.columns:
        df["metadata"] = "NA"
    return df


# 🔥 FIX DATE PER DATASET (IMPORTANT)
def fix_date(df, source):

    if source == "paysim":
        # PaySim uses "step" instead of date
        if "step" in df.columns:
            df["date"] = pd.to_datetime("2020-01-01") + pd.to_timedelta(df["step"], unit="h")

    elif source == "kaggle":
        if "trans_date_trans_time" in df.columns:
            df["date"] = pd.to_datetime(df["trans_date_trans_time"], errors="coerce")
        elif "timestamp" in df.columns:
            df["date"] = pd.to_datetime(df["timestamp"], errors="coerce")

    else:
        df["date"] = pd.to_datetime(df.get("date", None), errors="coerce")

    return df


def standardize(df, source):
    df = fix_date(df, source)

    required_cols = [
        "transaction_id",
        "user_id",
        "date",
        "amount",
        "balance",
        "description",
        "category",
        "metadata"
    ]

    for col in required_cols:
        if col not in df.columns:
            if col == "date":
                df[col] = pd.NaT
            else:
                df[col] = "NA"

    df["source"] = source
    return df[required_cols + ["source"]]


# Apply
bank = standardize(ensure_schema(bank), "bank")
paysim = standardize(ensure_schema(paysim), "paysim")
synthetic = standardize(ensure_schema(synthetic), "synthetic")
kaggle = standardize(ensure_schema(kaggle), "kaggle")
fraud = standardize(ensure_schema(fraud), "fraud")

# ======================
# MERGE
# ======================

df_all = pd.concat([bank, paysim, synthetic, kaggle, fraud], ignore_index=True)

print("Before cleaning:", df_all.shape)

# ======================
# FINAL DATE FIX (CRITICAL)
# ======================

df_all["date"] = pd.to_datetime(df_all["date"], errors="coerce")

print("Missing dates after final conversion:", df_all["date"].isna().sum())

# Now safely drop
df_all = df_all.dropna(subset=["date"])
# ======================
# CLEANING
# ======================



# Amount fix
df_all["amount"] = pd.to_numeric(df_all["amount"], errors="coerce")
df_all = df_all.dropna(subset=["amount"])

df_all["transaction_type"] = df_all["amount"].apply(
    lambda x: "credit" if x > 0 else "debit"
)
df_all["amount"] = df_all["amount"].abs()

# ======================
# FEATURES
# ======================

df_all["day_of_week"] = df_all["date"].dt.day_name()
df_all["is_weekend"] = df_all["day_of_week"].isin(["Saturday", "Sunday"]).astype(int)
df_all["hour"] = df_all["date"].dt.hour


def get_hour_bucket(h):
    if 5 <= h < 12:
        return "morning"
    elif 12 <= h < 17:
        return "afternoon"
    elif 17 <= h < 22:
        return "evening"
    else:
        return "night"


df_all["hour_bucket"] = df_all["hour"].apply(get_hour_bucket)

# ======================
# 🔥 MERCHANT EXTRACTION
# ======================

def extract_merchant(desc):
    desc = str(desc).lower()

    # Remove numbers + noise
    desc = re.sub(r'\d+', '', desc)

    # Common keywords cleanup
    noise_words = [
        "txn", "payment", "transfer", "debit", "credit",
        "pos", "upi", "ref", "id", "no", "from", "to"
    ]

    words = re.sub(r"[^a-z ]", " ", desc).split()
    words = [w for w in words if w not in noise_words]

    # Remove very short junk
    words = [w for w in words if len(w) > 2]

    if not words:
        return "unknown"

    # Handle "cash" separately
    if "cash" in words:
        return "cash_transaction"

    return words[0]

df_all["description"] = df_all["description"].astype(str)

df_all["merchant"] = [
    extract_merchant(desc) for desc in df_all["description"]
]

df_all["category"] = df_all.apply(categorize_transaction, axis=1)
# ======================
# FINAL CLEAN
# ======================

df_all = df_all.drop_duplicates()
df_all = df_all.sort_values(by=["user_id", "date"]).reset_index(drop=True)

# ======================
# FINAL COLUMNS
# ======================

final_cols = [
    "transaction_id",
    "user_id",
    "date",
    "amount",
    "transaction_type",
    "description",
    "merchant",
    "category",
    "balance",
    "day_of_week",
    "is_weekend",
    "hour",
    "hour_bucket",
    "metadata",
    "source"
]

df_all = df_all[final_cols]

# ======================
# CHECK
# ======================

print("\nFinal shape:", df_all.shape)
print("\nTop merchants:\n", df_all["merchant"].value_counts().head(10))

# ======================
# SAVE
# ======================

os.makedirs("data/final", exist_ok=True)
df_all.to_csv("data/final/unified_transactions.csv", index=False)
print(df_all["category"].value_counts())

print("\nFINAL DATASET SAVED")