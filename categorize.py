def categorize_transaction(row):
    desc = str(row["description"]).lower()
    merchant = str(row["merchant"]).lower()

    # INCOME
    if "salary" in desc:
        return "income"

    # FOOD
    if any(word in desc for word in ["food", "restaurant", "dining", "meal"]):
        return "food"

    # SHOPPING
    if any(word in desc for word in ["shopping", "purchase", "order", "electronics", "clothing"]):
        return "shopping"

    # TRANSPORT
    if any(word in desc for word in ["travel", "uber", "ola", "ride", "fuel"]):
        return "transport"

    # UTILITIES
    if any(word in desc for word in ["bill", "electricity", "water", "gas"]):
        return "utilities"

    # CASH
    if merchant in ["cash_transaction", "atm"] or "cash" in desc:
        return "cash"

    # TRANSFER
    if any(word in desc for word in ["upi", "transfer", "neft", "rtgs", "imps"]):
        return "transfer"

    return "misc"