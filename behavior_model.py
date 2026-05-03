import pandas as pd

# Load data
df = pd.read_csv("data/final/unified_transactions.csv", low_memory=False)

# 🔥 DEBUG MODE (FAST)
#df = df.sample(200000, random_state=42)

# -------------------
# CLEAN COLUMN NAMES (IMPORTANT)
# -------------------
df.columns = df.columns.str.strip()

# Ensure user_id exists
if "user_id" not in df.columns:
    raise ValueError(f"user_id not found. Available columns: {df.columns}")

# -------------------
# USER PROFILE
# -------------------

user_profile = (
    df.groupby("user_id")["amount"]
    .agg(avg_amount="mean", max_amount="max", min_amount="min")
    .reset_index()
)

# -------------------
# CATEGORY SPENDING
# -------------------

spending_pattern = (
    df.groupby(["user_id", "category"])["amount"]
    .mean()
    .unstack(fill_value=0)
    .reset_index()
)

category_profile = (
    df.groupby(["user_id", "category"])["amount"]
    .agg(["mean", "std"])
    .reset_index()
)

category_profile.columns = ["user_id", "category", "cat_avg", "cat_std"]

category_profile.to_csv("data/final/category_profile.csv", index=False)
# -------------------
# MERGE
# -------------------

user_profile = pd.merge(user_profile, spending_pattern, on="user_id", how="left")

# -------------------
# OUTPUT
# -------------------

print(user_profile.head())
print("\nColumns:\n", user_profile.columns)
user_profile.to_csv("data/final/user_profile.csv", index=False)