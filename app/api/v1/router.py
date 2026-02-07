from fastapi import APIRouter, HTTPException, Body
from ecologits.model_repository import Providers, models
from ecologits.electricity_mix_repository import electricity_mixes
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

@api_router.get(
    "/models/{providerName}", 
    response_model=dict, 
    summary="Get all models",
    description="<p>The returned models may include warning and error indicators. For detailed information about interpreting these warning and error values, please refer to the documentation: <br/><a href='https://ecologits.ai/latest/tutorial/warnings_and_errors/'>https://ecologits.ai/latest/tutorial/warnings_and_errors/</a></p>"
)
def get_models(providerName: str):
    try:
        provider = Providers[providerName]
    except KeyError:
        raise HTTPException(status_code=404, detail="Provider not found")

    try:
        filter_model = []
        for model in models.list_models():
            if model.provider == provider:
                filter_model.append(model)
        return {
            "models": filter_model,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve models")

@api_router.get(
    "/electricity-mix-zones/{zone}", 
    response_model=dict, 
    summary="Get electricity mix data for a zone",
    description="<p>Retrieve the electricity mix data for a specified zone using ISO 3166-1 alpha-3 country codes or special regional codes.</p><p><strong>Supported zone types:</strong></p><ul><li>Country codes: Use standard ISO 3166-1 alpha-3 codes (e.g., USA, FRA, DEU)</li><li>Regional codes: <code>EEE</code> for Europe, <code>WOR</code> for World average</li></ul><p><strong>Response:</strong> Returns the electricity mix composition data for the zone, or <code>404</code> if the zone is not supported by ecologits.</p><p>The electricity mix data includes the breakdown of energy sources used for electricity generation in the specified region, which is essential for accurate carbon impact calculations.</p>"
)
def get_electricity_mix_zones(zone: str):
    try:
        electricity_mix = electricity_mixes.find_electricity_mix(zone)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve electricity mix zone")
    
    if electricity_mix == None:
        raise HTTPException(status_code=404, detail=f"Electricity mix zone '{zone}' is not supported by ecologits")
    
    return {"electricity_mix": electricity_mix}

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
    electricity_mix_zone: str | None = Body(default=None, embed=True, examples=["WOR"], description="ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).")
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