import pytest
from responses import RequestsMock
from tatry import TatryAuthError, TatryRetriever
from tatry.client import API_URL
from tatry.models.auth import ValidateResponse, APIKey
import responses.matchers

@pytest.fixture
def mock_responses():
    with RequestsMock() as rsps:
        yield rsps

def test_validate_key(client, mock_responses):
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/auth/validate",
        json={
            "status": "success",
            "data": {
                "valid": True,
                "permissions": ["read", "write"],
                "organization_id": "org_123",
                "rate_limits": {
                    "requests_per_minute": 100,
                    "requests_per_hour": 1000
                }
            }
        },
        status=200,
    )
    
    response = client.auth.validate_key()
    assert isinstance(response, ValidateResponse)
    assert response.status == "success"
    assert response.data.valid == True
    assert "read" in response.data.permissions
    assert response.data.organization_id == "org_123"

def test_validate_invalid_key(mock_responses):
    client = TatryRetriever(api_key="invalid_key")
    
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/auth/validate",
        json={"error": "Invalid API key"},
        status=401,
    )
    
    with pytest.raises(TatryAuthError):
        client.auth.validate_key()

def test_list_keys(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/auth/keys",
        json={
            "status": "success",
            "data": {
                "keys": [
                    {
                        "id": "key_123",
                        "name": "Production API Key",
                        "status": "active",
                        "created_at": "2024-01-01T00:00:00Z",
                        "last_used_at": "2024-02-12T00:00:00Z"
                    }
                ],
                "total": 1
            }
        },
        status=200,
    )
    
    keys = client.auth.list_keys()
    assert isinstance(keys, list)
    assert len(keys) == 1
    assert isinstance(keys[0], APIKey)
    assert keys[0].id == "key_123"
    assert keys[0].status == "active"

    
def test_list_keys_with_params(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/auth/keys",
        match=[
            responses.matchers.query_param_matcher({
                "status": "active",
                "limit": "10",
                "offset": "20"
            })
        ],
        json={
            "status": "success",
            "data": {
                "keys": [
                    {
                        "id": "key_123",
                        "name": "Production API Key",
                        "status": "active",
                        "created_at": "2024-01-01T00:00:00Z",
                        "last_used_at": "2024-02-12T00:00:00Z"
                    }
                ],
                "total": 1
            }
        },
        status=200,
    )
    
    keys = client.auth.list_keys(
        status="active",
        limit=10,
        offset=20
    )
    assert isinstance(keys, list)
    assert len(keys) == 1
    assert isinstance(keys[0], APIKey)
    assert keys[0].id == "key_123"
    assert keys[0].status == "active"