
from fastapi import FastAPI
from app.upload import router
from .database import init_db
from .history import router as history_router

app = FastAPI(
    title="InfraSentry AI",
    description="AI-Powered Infrastructure Security Intelligence Platform"
)

# Initialize the SQLite database
init_db()

app.include_router(router, prefix="/api")
app.include_router(history_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to InfraSentry AI"}
