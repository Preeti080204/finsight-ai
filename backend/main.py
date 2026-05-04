from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base
from routes import router

app = FastAPI()


# CORS (open for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://finsight-ai-swart.vercel.app",  # your frontend
        "http://localhost:5173",                 # local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Create tables
Base.metadata.create_all(bind=engine)