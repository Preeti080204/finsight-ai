import pandas as pd

# -------------------
# LOAD DATA
# -------------------

df = pd.read_csv("data/final/unified_transactions.csv", low_memory=False)
profile = pd.read_csv("data/final/user_profile.csv")
cat_profile = pd.read_csv("data/final/category_profile.csv")

# -------------------
# DEBUG (FAST RUN)
# -------------------

#df = df.sample(200000, random_state=1)
# -------------------
# FILTER USERS WITH HISTORY
# -------------------

user_counts = df["user_id"].value_counts()
valid_users = user_counts[user_counts >= 5].index
df = df[df["user_id"].isin(valid_users)]

# -------------------
# GLOBAL BASELINE
# -------------------

global_avg = df.groupby("category")["amount"].mean().to_dict()

# -------------------
# MERGE PROFILES
# -------------------

df = df.merge(profile, on="user_id", how="left")
df = df.merge(cat_profile, on=["user_id", "category"], how="left")


# -------------------
# TAX / COMPLIANCE RULES
# -------------------

def tax_flag(row):
    amount = row["amount"]
    category = row["category"]

    # Rule 1: High value transaction
    if amount > 1000:
        return "High-value transaction — may require tax reporting"

    # Rule 2: Large cash usage
    if category == "cash" and amount > 500:
        return "Large cash transaction — check compliance limits"

    # Rule 3: Possible income
    if row["transaction_type"] == "credit" and amount > 800:
        return "Large credit detected — may be taxable income"

    return "No tax impact"
# -------------------
# ANOMALY DETECTION
# -------------------

def detect_anomaly(row):
    amount = row["amount"]
    cat_avg = row["cat_avg"]
    std = row["cat_std"]
    category = row["category"]

    # Fallback if weak user data
    if pd.isna(cat_avg) or cat_avg == 0:
        cat_avg = global_avg.get(category, amount)

    # -------------------
    # TRANSFER LOGIC
    # -------------------
    if category == "transfer":
        if pd.notna(cat_avg) and amount > 1.5 * cat_avg:
            return "high_spending", (
                f"You made a transfer of Rs.{amount:.2f}, "
                f"which is unusually high compared to your average Rs.{cat_avg:.2f}"
            )
        return "normal", (
            f"This transfer of Rs.{amount:.2f} is within your normal range "
            f"(avg Rs.{cat_avg:.2f})"
        )

    # -------------------
    # Z-SCORE (STRONG CHECK)
    # -------------------
    if pd.notna(std) and std > 0:
        z = (amount - cat_avg) / std

        if z > 1.5:
            return "high_spending", (
                f"You spent Rs.{amount:.2f} on {category}, "
                f"which is {round(z,2)} standard deviations above your normal"
            )

        if z < -1.5:
            return "low_spending", (
                f"You spent Rs.{amount:.2f} on {category}, "
                f"which is {round(abs(z),2)} standard deviations below your normal"
            )

    # -------------------
    # RATIO FALLBACK
    # -------------------
    ratio = amount / cat_avg

    if ratio > 1.5:
        return "high_spending", (
            f"You spent Rs.{amount:.2f} on {category}, "
            f"which is {round(ratio,2)}x higher than your usual Rs.{cat_avg:.2f}"
        )

    if ratio < 0.7:
        return "low_spending", (
            f"You spent Rs.{amount:.2f} on {category}, "
            f"which is only {round(ratio,2)}x of your usual Rs.{cat_avg:.2f}"
        )

    return "normal", (
        f"This transaction of Rs.{amount:.2f} in {category} is within your normal range "
        f"(avg Rs.{cat_avg:.2f})"
    )

# -------------------
# APPLY
# -------------------

df[["anomaly", "reason"]] = df.apply(
    lambda row: pd.Series(detect_anomaly(row)), axis=1
)
# Default
df["tax_flag"] = "No tax impact"

# 🔥 Dynamic threshold (IMPORTANT LINE)
threshold = df["amount"].quantile(0.90)

# Apply rules
df.loc[df["amount"] > threshold,
       "tax_flag"] = "High-value transaction - may require tax reporting"

df.loc[(df["category"] == "cash") & (df["amount"] > threshold * 0.5),
       "tax_flag"] = "Large cash transaction - check compliance limits"

df.loc[(df["transaction_type"] == "credit") & (df["amount"] > threshold * 0.7),
       "tax_flag"] = "Large credit detected - may be taxable income"

# -------------------
# COMBINED INSIGHT
# -------------------

df["final_insight"] = df["reason"] + " | " + df["tax_flag"]
# -------------------
# OUTPUT
# -------------------

print(df[[
    "user_id",
    "amount",
    "category",
    "anomaly",
    "final_insight"
]].head())

print("\nAnomaly distribution:\n", df["anomaly"].value_counts())

print("\n=== HIGH SPENDING ===")
print(df[df["anomaly"] == "high_spending"].head(10))

print("\n=== LOW SPENDING ===")
print(df[df["anomaly"] == "low_spending"].head(10))