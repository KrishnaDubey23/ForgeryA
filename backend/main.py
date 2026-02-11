import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, uploads, predictions, admin


load_dotenv()

STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage/uploads"))
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Aadhaar Forgery Detection API",
    description="FastAPI backend for AI-powered Aadhaar document & image forgery detection.",
    version="1.0.0",
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(predictions.router)
app.include_router(admin.router)


@app.get("/health")
async def health():
    return {"status": "ok", "message": "Backend is running"}




if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

