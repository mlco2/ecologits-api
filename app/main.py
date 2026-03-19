from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

# OpenAPI tag definitions
tags_metadata = [
    {
        "name": "Estimations",
        "description": "Estimate the environmental impacts of an LLM inference request.",
    },
    {
        "name": "Catalog",
        "description": "Browse the AI providers and models supported by EcoLogits. "
        "Use these endpoints to discover valid values for the estimation request.",
    },
    {
        "name": "Electricity mix",
        "description": "Retrieve the electricity mix composition for a given geographic zone. "
        "This data is used to calculate carbon impacts.",
    },
]

# Create FastAPI instance with metadata
app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_tags=tags_metadata,
    contact={
        "name": "EcoLogits",
        "url": "https://ecologits.ai",
    },
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
