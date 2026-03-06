import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1 import api_router

# Import all models to ensure SQLAlchemy relationships are configured
from . import models  # noqa: F401

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def log_oauth_settings() -> None:
    logger = logging.getLogger("uvicorn.error")
    logger.info("Loaded OAuth settings:")
    logger.info("GOOGLE_CLIENT_ID=%s", settings.GOOGLE_CLIENT_ID)
    logger.info("GOOGLE_CLIENT_SECRET=%s", settings.GOOGLE_CLIENT_SECRET)
    logger.info("GOOGLE_REDIRECT_URI=%s", settings.GOOGLE_REDIRECT_URI)
    logger.info("GOOGLE_GMAIL_REDIRECT_URI=%s", settings.GOOGLE_GMAIL_REDIRECT_URI)



@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Trading Notes API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
