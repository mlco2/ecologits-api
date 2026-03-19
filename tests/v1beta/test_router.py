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
    """Test the POST /estimations endpoint without electricity_mix_zone (should use default)"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "output_token_count": 150,
        "request_latency": 0.8,
        # electricity_mix_zone not provided, should default to "WOR"
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


def test_post_estimations_missing_required_fields():
    """Test the POST /estimations endpoint with missing required fields"""
    payload = {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        # Missing output_token_count and request_latency
    }

    response = client.post("/v1beta/estimations", json=payload)
    assert response.status_code == 422  # Unprocessable Entity for validation errors
