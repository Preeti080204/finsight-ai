from fastapi import APIRouter, UploadFile, File, Query
from database import SessionLocal
from models import Transaction, Feedback, UserProfile, User
from pydantic import BaseModel
from typing import List
from services.scoring import apply_scoring, compute_health_score, generate_recommendations
import pandas as pd

router = APIRouter()


# -----------------------------
# DATA ENDPOINT
# -----------------------------
@router.get("/data")
def get_data(user_id: int):
    db = SessionLocal()

    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()

    data = [{
        "id": t.id,
        "date": t.date,
        "desc": t.desc,
        "amount": t.amount,
        "category": t.category
    } for t in transactions]

    db.close()
    return data


# -----------------------------
# SCHEMA
# -----------------------------
class TransactionInput(BaseModel):
    date: str
    desc: str
    amount: float
    category: str


# -----------------------------
# BUILD USER PROFILE
# -----------------------------
@router.post("/build-profile")
def build_profile(transactions: List[TransactionInput], user_id: int = Query(...)):
    db = SessionLocal()

    txns = [t.dict() for t in transactions]

    income = [t["amount"] for t in txns if t["category"] == "Income"]
    spending = [t["amount"] for t in txns if t["category"] != "Income"]

    avg_income = sum(income) / len(income) if income else 0
    avg_spending = sum(spending) / len(spending) if spending else 0

    profile = UserProfile(
        avg_income=avg_income,
        avg_spending=avg_spending,
        user_id=user_id
    )

    db.add(profile)
    db.commit()
    db.close()

    return {
        "avg_income": avg_income,
        "avg_spending": avg_spending
    }


# -----------------------------
# FEEDBACK (FIXED)
# -----------------------------
@router.post("/feedback")
def save_feedback(data: dict):
    db = SessionLocal()

    try:
        transaction_id = data.get("transaction_id")
        label = data.get("label")

        if transaction_id is None or label is None:
            return {"error": "Missing transaction_id or label"}

        fb = Feedback(
            transaction_id=transaction_id,
            label=label,
        )

        db.add(fb)
        db.commit()

        return {"message": "Feedback saved"}

    except Exception as e:
        print("FEEDBACK ERROR:", str(e))
        return {"error": str(e)}

    finally:
        db.close()


# -----------------------------
# FEEDBACK LOGIC
# -----------------------------
def adjust_score(score, feedback_label):
    if feedback_label == "normal":
        return max(score * 0.4, 0)
    elif feedback_label == "suspicious":
        return min(score * 1.6, 1)
    return score


# -----------------------------
# ANALYSIS ENGINE (FIXED)
# -----------------------------
@router.post("/analyze")
def analyze(transactions: List[TransactionInput], user_id: int = Query(...)):
    db = SessionLocal()

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id
    ).order_by(UserProfile.id.desc()).first()

    df = pd.DataFrame([t.dict() for t in transactions])

    # 🔥 FIX: ensure ID exists
    if "id" not in df.columns:
        df["id"] = range(1, len(df) + 1)

    df = apply_scoring(df)

    recommendations = generate_recommendations(df)
    health_score = compute_health_score(df)

    results = []

    for _, row in df.iterrows():
        txn_id = int(row["id"]) if "id" in row else 0

        reasons = row.get("explanations", [])

        if profile and row["amount"] > profile.avg_income * 2:
            reasons.append("Amount significantly higher than your usual income")

        if row["category"] == "Transfer":
            reasons.append("Frequent transfers detected")

        if profile and row["category"] != "Income" and row["amount"] > profile.avg_spending * 2:
            reasons.append("Spending much higher than your normal pattern")

        score = row["score"]

        feedbacks = db.query(Feedback).filter(
            Feedback.transaction_id == txn_id
        ).all()

        for fb in feedbacks:
            score = adjust_score(score, fb.label)

        results.append({
            "id": txn_id,
            "transaction": row.to_dict(),
            "score": round(score, 2),
            "reasons": reasons,
            "health_score": health_score,
            "recommendations": recommendations
        })

    db.close()
    return results


# -----------------------------
# FILE UPLOAD
# -----------------------------
@router.post("/upload")
async def upload_file(file: UploadFile = File(...), user_id: int = Query(...)):
    db = SessionLocal()

    print("UPLOAD HIT")

    db.query(Transaction).filter(Transaction.user_id == user_id).delete()
    db.commit()

    try:
        contents = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(contents))
    except Exception:
        return {"error": "Upload a valid CSV file"}

    df.columns = [c.lower() for c in df.columns]

    if "description" in df.columns:
        df = df.rename(columns={"description": "desc"})

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    def categorize(desc, amount):
        d = desc.lower()

        if amount > 0:
            return "Income"
        elif "swiggy" in d or "zomato" in d:
            return "Food"
        elif "uber" in d:
            return "Transport"
        elif "amazon" in d:
            return "Shopping"
        elif "netflix" in d:
            return "Entertainment"
        elif "electric" in d:
            return "Bills"
        else:
            return "Other"

    df["category"] = df.apply(lambda row: categorize(row["desc"], row["amount"]), axis=1)

    transactions = df[["date", "desc", "amount", "category"]].to_dict(orient="records")

    for t in transactions:
        txn = Transaction(**t, user_id=user_id)
        db.add(txn)

    db.commit()
    db.close()

    return {
        "message": "Saved to DB",
        "transactions": transactions
    }


# -----------------------------
# AUTH
# -----------------------------
@router.post("/signup")
def signup(data: dict):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == data["username"]).first()
    if existing:
        db.close()
        return {"error": "User already exists"}

    user = User(
        username=data["username"],
        password=data["password"]
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "User created"}


@router.post("/login")
def login(data: dict):
    db = SessionLocal()

    user = db.query(User).filter(
        User.username == data["username"],
        User.password == data["password"]
    ).first()

    db.close()

    if not user:
        return {"error": "Invalid credentials"}

    return {
        "message": "Login successful",
        "user_id": user.id
    }