from fastapi import APIRouter, HTTPException, Body
from ecologits.model_repository import Providers
from ecologits.tracers.utils import llm_impacts

api_router = APIRouter()

@api_router.get("/providers", response_model=dict, summary="Get all providers")
def get_providers():
    try:
        providers_list = [provider.value for provider in Providers]
        return {
            "providers": providers_list,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve providers")

@api_router.post(
    "/estimations",
    response_model=dict,
    summary="Estimate the impacts of an LLM generation requests"
)
def post_estimations(
    provider: str = Body(..., embed=True, examples=["openai"], description="Name of the provider."),
    model_name: str = Body(..., embed=True, examples=["gpt-4o-mini"], description="Name of the LLM used."),
    output_token_count: int = Body(..., embed=True, examples=[300], description="Number of generated tokens."),
    request_latency: float = Body(..., embed=True, examples=[1.5], description="Measured request latency in seconds."),
    electricity_mix_zone: str = Body("WOR", embed=True, examples=["WOR"], description="ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).")
):
    try:
        impacts = llm_impacts(
            provider=provider,
            model_name=model_name,
            output_token_count=output_token_count,
            request_latency=request_latency,
            electricity_mix_zone=electricity_mix_zone,
        )
        return {"impacts": impacts}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to Estimate impacts")