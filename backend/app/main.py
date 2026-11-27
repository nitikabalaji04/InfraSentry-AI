from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.upload import router
from .database import init_db
from .history import router as history_router
from .analytics import router as analytics_router

app = FastAPI(
    title="InfraSentry AI",
    description="AI-Powered Infrastructure Security Intelligence Platform"
)

# Allow frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)

# Initialize the SQLite database
init_db()

# Register API routers
app.include_router(router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")


@app.get("/")
def home():
    return {"message": "Welcome to InfraSentry AI"}


@app.get("/health")
def health():
    return {"status": "healthy"}