from ecologits.status_messages import ModelNotRegisteredError
from ecologits.tracers.utils import ImpactsOutput
from ecologits.estimations.video import video_impacts
from ecologits.model_repository import Providers
from ecologits.tracers.utils import llm_impacts
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_providers():
    response = client.get("/v1beta/providers")
    assert response.status_code == 200
    assert "providers" in response.json()
    assert response.json() == {"providers": [provider.value for provider in Providers]}


def test_get_models_valid_provider():
    response = client.get("/v1beta/models/openai")
    assert response.status_code == 200
    assert "models" in response.json()
    assert isinstance(response.json()["models"], list)


def test_get_models_invalid_provider():
    response = client.get("/v1beta/models/invalid_provider")
    assert response.status_code == 404
    assert response.json() == {"detail": "Provider not found"}


def test_get_video_providers():
    response = client.get("/v1beta/video-providers")
    assert response.status_code == 200
    assert "providers" in response.json()
    assert "openai" in response.json()["providers"]
    assert "google" in response.json()["providers"]


def test_get_video_models_valid_provider():
    response = client.get("/v1beta/video-models/google")
    assert response.status_code == 200
    assert "models" in response.json()
    assert {
        "provider": "google",
        "model_name": "google/veo-3.1",
        "capabilities": {
            "resolutions": [[1280, 720], [1920, 1080]],
            "frames_count": [97, 145, 193],
            "audio_generation": True,
        },
    } in response.json()["models"]


def test_get_video_models_invalid_provider():
    response = client.get("/v1beta/video-models/invalid_provider")
    assert response.status_code == 404
    assert response.json() == {"detail": "Video provider not found"}


def test_find_electricity_mix_zones_valid():
    """Test the GET /electricity-mix-zones/{zone} endpoint with a valid zone"""
    response = client.get("/v1beta/electricity-mix-zones/WOR")
    assert response.status_code == 200

    response_data = response.json()
    assert "electricity_mix" in response_data
    assert response_data["electricity_mix"] is not None
    assert "zone" in response_data["electricity_mix"]
    assert response_data["electricity_mix"]["zone"] == "WOR"


def test_find_electricity_mix_zones_invalid():
    """Test the GET /electricity-mix-zones/{zone} endpoint with an invalid zone"""
    response = client.get("/v1beta/electricity-mix-zones/INVALID")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Electricity mix zone 'INVALID' is not supported by EcoLogits"
    }


def test_find_electricity_mix_zones_other_valid_zones():
    """Test the GET /electricity-mix-zones/{zone} endpoint with other valid zones"""
    valid_zones = ["WOR", "USA", "FRA"]

    for zone in valid_zones:
        response = client.get(f"/v1beta/electricity-mix-zones/{zone}")
        assert response.status_code == 200

        response_data = response.json()
        assert "electricity_mix" in response_data
        assert response_data["electricity_mix"]["zone"] == zone


def test_post_estimations():
    """Test the POST /estimations endpoint"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "output_token_count": 300,
        "request_latency": 1.5,
        "electricity_mix_zone": "WOR",
    }

    # Get the expected impacts directly from llm_impacts
    expected_impacts = llm_impacts(
        provider=payload["provider"],
        model_name=payload["model_name"],
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
        electricity_mix_zone=payload["electricity_mix_zone"],
    )

    # Call the API endpoint
    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] is not None

    # Compare the impacts data - convert expected_impacts to dict for comparison
    expected_impacts_dict = expected_impacts.model_dump()
    assert response_data["impacts"] == expected_impacts_dict


def test_post_estimations_default_electricity_mix():
    """Test the POST /estimations endpoint without datacenter_location"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "output_token_count": 150,
        "request_latency": 0.8,
    }

    # Get the expected impacts directly from llm_impacts
    expected_impacts = llm_impacts(
        provider=payload["provider"],
        model_name=payload["model_name"],
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
    )

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] is not None

    # Compare the impacts data - convert expected_impacts to dict for comparison
    expected_impacts_dict = expected_impacts.model_dump()
    assert response_data["impacts"] == expected_impacts_dict


def test_post_estimations_datacenter_location():
    """Test the POST /estimations endpoint with datacenter_location"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-5",
        "output_token_count": 150,
        "request_latency": 0.8,
        "datacenter_location": "USA",
    }

    expected_impacts = llm_impacts(
        provider=payload["provider"],
        model_name=payload["model_name"],
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
        electricity_mix_zone=payload["datacenter_location"],
    )

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_estimations_datacenter_location_takes_precedence():
    """Test datacenter_location takes precedence over deprecated electricity_mix_zone"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-5",
        "output_token_count": 150,
        "request_latency": 0.8,
        "datacenter_location": "USA",
        "electricity_mix_zone": "WOR",
    }

    expected_impacts = llm_impacts(
        provider=payload["provider"],
        model_name=payload["model_name"],
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
        electricity_mix_zone=payload["datacenter_location"],
    )

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_estimations_deprecated_electricity_mix_zone():
    """Test deprecated electricity_mix_zone still works"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-5",
        "output_token_count": 150,
        "request_latency": 0.8,
        "electricity_mix_zone": "USA",
    }

    expected_impacts = llm_impacts(
        provider=payload["provider"],
        model_name=payload["model_name"],
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
        electricity_mix_zone=payload["electricity_mix_zone"],
    )

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_estimations_provider_qualified_model_name():
    """Test the POST /estimations endpoint with provider inferred from model_name"""
    payload = {
        "model_name": "openai/gpt-5",
        "output_token_count": 150,
        "request_latency": 0.8,
    }

    expected_impacts = llm_impacts(
        provider="openai",
        model_name="gpt-5",
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
    )

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_estimations_provider_and_short_model_name():
    """Test the POST /estimations endpoint with explicit provider and short model name"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-5",
        "output_token_count": 150,
        "request_latency": 0.8,
    }

    expected_impacts = llm_impacts(
        provider=payload["provider"],
        model_name=payload["model_name"],
        output_token_count=payload["output_token_count"],
        request_latency=payload["request_latency"],
    )

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_estimations_unqualified_model_name_without_provider():
    """Test the POST /estimations endpoint when provider cannot be inferred"""
    payload = {
        "model_name": "gpt-5",
        "output_token_count": 150,
        "request_latency": 0.8,
    }
    error = ModelNotRegisteredError(
        message=(
            "Could not infer provider from model_name. Use a provider-qualified "
            "model name such as `openai/gpt-5`, or provide `provider`."
        )
    )
    expected_impacts = ImpactsOutput(errors=[error])

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_estimations_missing_required_fields():
    """Test the POST /estimations endpoint with missing required fields"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        # Missing output_token_count and request_latency
    }

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 422  # Unprocessable Entity for validation errors


def test_post_video_estimations():
    """Test the POST /video-estimations endpoint"""
    payload = {
        "model_name": "google/veo-3.1",
        "resolution": "720p",
        "duration": 4,
        "with_audio": True,
        "datacenter_location": "WOR",
    }

    expected_impacts = video_impacts(
        model_name=payload["model_name"],
        resolution=payload["resolution"],
        duration=payload["duration"],
        with_audio=payload["with_audio"],
        datacenter_location=payload["datacenter_location"],
    )

    response = client.post("/v1beta/video-estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] is not None

    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_video_estimations_default_optional_fields():
    """Test the POST /video-estimations endpoint with optional fields omitted"""
    payload = {
        "model_name": "google/veo-3.1",
        "resolution": "720p",
        "duration": 4,
    }

    expected_impacts = video_impacts(
        model_name=payload["model_name"],
        resolution=payload["resolution"],
        duration=payload["duration"],
        datacenter_location=None,
    )

    response = client.post("/v1beta/video-estimations", json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert "impacts" in response_data
    assert response_data["impacts"] is not None

    assert response_data["impacts"] == expected_impacts.model_dump()


def test_post_video_estimations_missing_required_fields():
    """Test the POST /video-estimations endpoint with missing required fields"""
    payload = {
        "model_name": "google/veo-3.1",
        # Missing resolution and duration
    }

    response = client.post("/v1beta/video-estimations", json=payload)
    assert response.status_code == 422
