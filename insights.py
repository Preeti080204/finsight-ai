import pandas as pd

# -------------------
# SAFE LOADING (NO MEMORY CRASH)
# -------------------

chunks = []
sample_size_per_chunk = 5000  # small + safe

for chunk in pd.read_csv(
    "data/final/unified_transactions.csv",
    usecols=["user_id", "date", "amount", "category"],
    chunksize=50000   # controlled memory
):
    # Drop nulls early (important)
    chunk = chunk.dropna(subset=["date", "amount", "category"])

    # Convert types safely
    chunk["amount"] = pd.to_numeric(chunk["amount"], errors="coerce")
    chunk = chunk.dropna(subset=["amount"])

    # Sample SMALL portion from each chunk
    if len(chunk) > sample_size_per_chunk:
        chunk = chunk.sample(sample_size_per_chunk, random_state=42)

    chunks.append(chunk)

# Combine safely
df = pd.concat(chunks, ignore_index=True)

print("Loaded rows:", len(df))

# -------------------
# PROCESSING
# -------------------

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

df["month"] = df["date"].dt.to_period("M")

# -------------------
# GROUPING (FAST NOW)
# -------------------

monthly_total = df.groupby(["user_id", "month"])["amount"].sum().reset_index()

category_spend = df.groupby(["user_id", "month", "category"])["amount"].sum().reset_index()

df_summary = category_spend.merge(
    monthly_total,
    on=["user_id", "month"],
    suffixes=("_cat", "_total")
)

# -------------------
# TREND ANALYSIS
# -------------------

monthly_total = monthly_total.sort_values(by=["user_id", "month"])

monthly_total["prev_month_spend"] = monthly_total.groupby("user_id")["amount"].shift(1)

monthly_total["change_pct"] = (
    (monthly_total["amount"] - monthly_total["prev_month_spend"]) /
    monthly_total["prev_month_spend"]
) * 100


def generate_trend(row):
    if pd.isna(row["change_pct"]):
        return ""

    change = row["change_pct"]

    if change > 10:
        return f"Your spending increased by {round(change,1)}% compared to last month."

    elif change < -10:
        return f"Your spending decreased by {round(abs(change),1)}% compared to last month."

    return "Your spending remained stable compared to last month."


monthly_total["trend"] = monthly_total.apply(generate_trend, axis=1)

# -------------------
# FAST STORY GENERATION (NO APPLY)
# -------------------

# Get top category per user-month
top_category = df_summary.sort_values(
    ["user_id", "month", "amount_cat"],
    ascending=[True, True, False]
).drop_duplicates(subset=["user_id", "month"])

# Merge with trend
final_df = top_category.merge(
    monthly_total[["user_id", "month", "trend"]],
    on=["user_id", "month"],
    how="left"
)

# Generate story (vectorized)
final_df["story"] = (
    "You spent Rs." + final_df["amount_total"].round(2).astype(str)
    + " this month. Most of your spending was on "
    + final_df["category"]
    + " (Rs." + final_df["amount_cat"].round(2).astype(str) + "). "
    + final_df["trend"].fillna("")
)

# -------------------
# OUTPUT
# -------------------

print("\n=== SAMPLE STORIES ===\n")
print(final_df["story"].head(10))