
from fastapi import FastAPI
from app.upload import router

app = FastAPI(
    title="InfraSentry AI",
    description="AI-Powered Infrastructure Security Intelligence Platform"
)

app.include_router(router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to InfraSentry AI"}
