"""
Simplified AvatarKit API - Internal Use Only
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="AvatarKit API (Internal)",
    version="1.0.0",
    description="Internal avatar generation API",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from app.routers import avatar, generate

app.include_router(avatar.router, prefix="/api/v1")
app.include_router(generate.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"name": "AvatarKit API (Internal)", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
