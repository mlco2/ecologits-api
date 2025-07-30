from fastapi import APIRouter, HTTPException
from ecologits.model_repository import Providers

api_router = APIRouter()

@api_router.get("/providers", response_model=dict, summary="Get all providers")
def get_providers():
    """
    Retrieve a list of all available AI model providers.
    
    Returns:
        dict: A dictionary containing the list of provider names
    """
    try:
        providers_list = [provider.value for provider in Providers]
        return {
            "providers": providers_list,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve providers")