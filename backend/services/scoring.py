import pandas as pd

def compute_baseline(df):
    df["date"] = pd.to_datetime(df["date"])

    avg_amount = df["amount"].mean()
    std_amount = df["amount"].std()

    category_avg = df.groupby("category")["amount"].mean().to_dict()

    return avg_amount, std_amount, category_avg


def amount_score(amount, avg, std):
    if std == 0:
        return 0
    z = (amount - avg) / std
    return min(max(z / 3, 0), 1)


def category_score(amount, category, category_avg):
    if category not in category_avg:
        return 0
    avg = category_avg[category]
    return min(max((amount - avg) / (avg + 1), 0), 1)


def frequency_score(df, current_date):
    recent = df[df["date"] > current_date - pd.Timedelta(days=7)]
    freq = len(recent)
    return min(freq / 10, 1)


def final_score(a, f, c):
    return round(0.5*a + 0.3*f + 0.2*c, 3)


def apply_scoring(df):
    avg_amount, std_amount, category_avg = compute_baseline(df)

    scores = []
    explanations_all = []

    for _, row in df.iterrows():
        a = amount_score(row["amount"], avg_amount, std_amount)
        c = category_score(row["amount"], row["category"], category_avg)
        f = frequency_score(df, pd.to_datetime(row["date"]))

        score = final_score(a, f, c)

        # 🔥 NEW: explanation
        explanation = generate_explanation(row, avg_amount, category_avg)

        scores.append(score)
        explanations_all.append(explanation)

    df["score"] = scores
    df["explanations"] = explanations_all

    return df

def generate_explanation(row, avg_amount, category_avg):
    explanations = []

    amount = row["amount"]
    category = row["category"]

    # Overall deviation
    if avg_amount > 0:
        percent = ((amount - avg_amount) / avg_amount) * 100
        if percent > 50:
            explanations.append(
                f"Amount is {round(percent)}% higher than your average spending (₹{round(avg_amount)})"
            )

    # Category deviation
    if category in category_avg:
        cat_avg = category_avg[category]
        if cat_avg > 0:
            percent_cat = ((amount - cat_avg) / cat_avg) * 100
            if percent_cat > 50:
                explanations.append(
                    f"This is {round(percent_cat)}% higher than your usual {category.lower()} spending (₹{round(cat_avg)})"
                )

    return explanations

def compute_health_score(df):
    income = df[df["category"] == "Income"]["amount"].sum()
    spending = df[df["category"] != "Income"]["amount"].sum()

    # 1. Savings ratio
    if income > 0:
        savings_ratio = (income - spending) / income
    else:
        savings_ratio = 0

    savings_score = max(min(savings_ratio, 1), 0)

    # 2. Spending stability (low std = good)
    std = df["amount"].std()
    mean = df["amount"].mean()

    if mean > 0:
        stability = 1 - min(std / mean, 1)
    else:
        stability = 0

    # 3. Risk (based on anomaly scores)
    risk = df["score"].mean()
    risk_score = 1 - risk  # lower risk = better

    # Final weighted score
    health = (
        0.5 * savings_score +
        0.3 * stability +
        0.2 * risk_score
    )

    return round(health * 100, 2)

def generate_recommendations(df):
    recommendations = []

    income = df[df["category"] == "Income"]["amount"].sum()
    spending = df[df["category"] != "Income"]["amount"].sum()

    # -----------------------------
    # 1. Savings check
    # -----------------------------
    if income > 0:
        savings_rate = (income - spending) / income

        if savings_rate < 0.2:
            recommendations.append(
                "Your savings rate is low. Try reducing non-essential expenses."
            )

    # -----------------------------
    # 2. Category overspending
    # -----------------------------
    category_spend = df[df["category"] != "Income"].groupby("category")["amount"].sum()

    for cat, amt in category_spend.items():
        if income > 0 and (amt / income) > 0.3:
            recommendations.append(
                f"High spending detected in {cat}. Consider reducing it."
            )

    # -----------------------------
    # 3. High anomaly risk
    # -----------------------------
    avg_score = df["score"].mean()

    if avg_score > 0.5:
        recommendations.append(
            "Multiple high-risk transactions detected. Review your recent activity."
        )

    # -----------------------------
    # fallback
    # -----------------------------
    if not recommendations:
        recommendations.append("Your financial behavior looks healthy. Keep it up.")

    return recommendations