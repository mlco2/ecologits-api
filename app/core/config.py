import os
from typing import List

class Settings:
    # API Configuration
    app_name: str = "Ecologits API"
    app_version: str = "1.0.0"
    description: str = "API to use the Ecologits solution for AI environmental impact tracking"
    
    # CORS Configuration
    allowed_origins: List[str] = ["*"]
    allowed_methods: List[str] = ["*"]
    allowed_headers: List[str] = ["*"]
    
    # API Configuration
    api_v1_prefix: str = "/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    # Environment-based overrides
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", self.app_name)
        self.app_version = os.getenv("APP_VERSION", self.app_version)

settings = Settings()
