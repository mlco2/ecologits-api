from ecologits.model_repository import Providers
from fastapi.testclient import TestClient
from app.main import app
    
client = TestClient(app)

def test_get_providers():
    response = client.get("/v1/providers")
    assert response.status_code == 200
    assert "providers" in response.json()
    assert response.json() == {"providers": [provider.value for provider in Providers]}