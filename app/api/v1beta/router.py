import json
from importlib import resources

from ecologits.electricity_mix_repository import electricity_mixes
from ecologits.estimations.video import video_impacts
from ecologits.model_repository import Providers, models
from ecologits.status_messages import ModelNotRegisteredError
from ecologits.tracers.utils import ImpactsOutput, llm_impacts
from fastapi import APIRouter, Body, HTTPException

from app.api.v1beta.responses import (
    ELECTRICITY_MIX_RESPONSES,
    ESTIMATIONS_RESPONSES,
    MODELS_RESPONSES,
    PROVIDERS_RESPONSES,
    VIDEO_ESTIMATIONS_RESPONSES,
    VIDEO_MODELS_RESPONSES,
    VIDEO_PROVIDERS_RESPONSES,
)

api_router_v1beta = APIRouter(prefix="/v1beta")


def _load_video_models() -> list[dict]:
    video_models = resources.files("ecologits").joinpath("data/video_models.json")
    return json.loads(video_models.read_text())["models"]


def _public_video_model(model: dict) -> dict:
    return {
        "provider": model["provider"],
        "model_name": model["model_name"],
        "capabilities": model["capabilities"],
    }


@api_router_v1beta.get(
    "/providers",
    response_model=dict,
    tags=["Catalog"],
    summary="List all supported providers",
    responses=PROVIDERS_RESPONSES,
)
def get_providers():
    try:
        providers_list = [provider.value for provider in Providers]
        return {
            "providers": providers_list,
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve providers")


@api_router_v1beta.get(
    "/models/{provider_name}",
    response_model=dict,
    tags=["Catalog"],
    summary="List models for a provider",
    description=(
        "Models may include **warning** and **error** indicators "
        "([details](https://ecologits.ai/latest/tutorial/warnings_and_errors/))."
    ),
    responses=MODELS_RESPONSES,
)
def get_models(provider_name: str):
    try:
        provider = Providers[provider_name]
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
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve models")


@api_router_v1beta.get(
    "/video-providers",
    response_model=dict,
    tags=["Video catalog"],
    summary="List all supported video generation providers",
    responses=VIDEO_PROVIDERS_RESPONSES,
)
def get_video_providers():
    try:
        providers_list = list(
            dict.fromkeys(model["provider"] for model in _load_video_models())
        )
        return {
            "providers": providers_list,
        }
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve video providers"
        )


@api_router_v1beta.get(
    "/video-models/{provider_name}",
    response_model=dict,
    tags=["Video catalog"],
    summary="List video generation models for a provider",
    responses=VIDEO_MODELS_RESPONSES,
)
def get_video_models(provider_name: str):
    try:
        filter_model = [
            _public_video_model(model)
            for model in _load_video_models()
            if model["provider"] == provider_name
        ]
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve video models")

    if not filter_model:
        raise HTTPException(status_code=404, detail="Video provider not found")

    return {
        "models": filter_model,
    }


@api_router_v1beta.get(
    "/electricity-mix-zones/{zone}",
    response_model=dict,
    tags=["Electricity mix"],
    summary="Get electricity mix for a zone",
    description=(
        "Use ISO 3166-1 alpha-3 codes (`USA`, `FRA`, `DEU`) "
        "(or `WOR` for World average)."
    ),
    responses=ELECTRICITY_MIX_RESPONSES,
)
def get_electricity_mix_zones(zone: str):
    try:
        electricity_mix = electricity_mixes.find_electricity_mix(zone)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve electricity mix zone"
        )

    if electricity_mix is None:
        raise HTTPException(
            status_code=404,
            detail=f"Electricity mix zone '{zone}' is not supported by EcoLogits",
        )

    return {"electricity_mix": electricity_mix}


@api_router_v1beta.post(
    "/estimations",
    response_model=dict,
    tags=["Estimations"],
    summary="Estimate environmental impacts of an LLM request",
    responses=ESTIMATIONS_RESPONSES,
)
def post_estimations(
    provider: str = Body(
        ...,
        embed=True,
        examples=["openai"],
        description="Provider identifier (use `GET /v1beta/providers` to list valid values).",
    ),
    model_name: str = Body(
        ...,
        embed=True,
        examples=["gpt-4o-mini"],
        description="Model identifier as registered in EcoLogits (use `GET /v1beta/models/{provider}` to list valid values).",
    ),
    output_token_count: int = Body(
        ...,
        embed=True,
        examples=[300],
        description="Number of tokens generated by the model.",
    ),
    request_latency: float | None = Body(
        default=None,
        embed=True,
        examples=[1.5],
        description="Measured request latency in seconds.",
    ),
    electricity_mix_zone: str | None = Body(
        default=None,
        embed=True,
        examples=["WOR"],
        description="ISO 3166-1 alpha-3 zone code for the electricity mix. Defaults to `WOR` (world average). (use `GET /v1beta/electricity-mix-zones/{zone}` to check zone availability)",
    ),
):
    try:
        impacts = llm_impacts(
            provider=provider,
            model_name=model_name,
            output_token_count=output_token_count,
            # Use high request latency if not provided, to default the latency estimation made with
            # the TPS and TTFT data from OpenRouter.
            # TODO: remove the high value when the estimations module in EcoLogits (Python) is ready
            request_latency=request_latency if request_latency is not None else 1e6,
            electricity_mix_zone=electricity_mix_zone,
        )
        return {"impacts": impacts}

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to Estimate impacts")


@api_router_v1beta.post(
    "/video-estimations",
    response_model=dict,
    tags=["Video estimations"],
    summary="Estimate environmental impacts of a video generation request",
    responses=VIDEO_ESTIMATIONS_RESPONSES,
)
def post_video_estimations(
    model_name: str = Body(
        ...,
        embed=True,
        examples=["google/veo-3.1"],
        description="Video model identifier as registered in EcoLogits (use `GET /v1beta/video-models/{provider}` to list valid values).",
    ),
    resolution: str = Body(
        ...,
        embed=True,
        examples=["720p", "1080p", "1920x1080"],
        description="Generated video resolution.",
    ),
    duration: float = Body(
        ...,
        embed=True,
        examples=[4],
        description="Generated video duration in seconds.",
    ),
    with_audio: bool = Body(
        default=True,
        embed=True,
        description="Whether the generated video includes audio.",
    ),
    datacenter_location: str | None = Body(
        default=None,
        embed=True,
        examples=["USA"],
        description="ISO 3166-1 alpha-3 datacenter zone code. Uses the provider default when omitted.",
    ),
):
    try:
        impacts = video_impacts(
            model_name=model_name,
            resolution=resolution,
            duration=duration,
            with_audio=with_audio,
            datacenter_location=datacenter_location,
        )
        return {"impacts": impacts}

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to estimate video impacts")
