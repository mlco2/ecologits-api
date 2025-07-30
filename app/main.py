from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

# Create FastAPI instance with metadata
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Include API router with version prefix
app.include_router(api_router, prefix=settings.api_v1_prefix)
