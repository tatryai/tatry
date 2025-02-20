import pytest
import requests

from tatry.exceptions import (
    RetrieverAPIError,
    RetrieverAuthError,
    RetrieverConfigError,
    RetrieverConnectionError,
    RetrieverTimeoutError,
)
from tatry.retrievers.tatry.endpoints import TatryImplementation


class ClientImplementation(TatryImplementation):
    """Test implementation of TatryClient with minimal overrides."""

    pass


@pytest.fixture
def test_client():
    """Fixture providing test client instance."""
    return ClientImplementation(api_key="test_key")


def test_client_initialization(test_client):
    """Test basic client initialization."""
    assert test_client.config.api_key == "test_key"
    assert test_client.config.timeout == 30
    assert test_client.config.max_retries == 3


def test_client_custom_config():
    """Test client with custom configuration."""
    client = ClientImplementation(
        api_key="test_key", timeout=60, max_retries=5, base_url="https://custom.api.com"
    )
    assert client.config.timeout == 60
    assert client.config.max_retries == 5
    assert client.config.base_url == "https://custom.api.com"


def test_client_invalid_api_key():
    """Test client initialization with invalid API key."""
    with pytest.raises(RetrieverConfigError):
        ClientImplementation(api_key="")

    with pytest.raises(RetrieverConfigError):
        ClientImplementation(api_key=None)


def test_request_auth_error(mock_responses, test_client):
    """Test handling of authentication errors."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        json={"error": "Invalid API key"},
        status=401,
    )

    with pytest.raises(RetrieverAuthError) as exc:
        test_client._request("GET", "/v1/test")
    assert exc.value.status_code == 401


def test_request_timeout(mock_responses, test_client):
    """Test handling of timeout errors."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        body=requests.exceptions.Timeout(),
    )

    with pytest.raises(RetrieverTimeoutError):
        test_client._request("GET", "/v1/test")


def test_request_connection_error(mock_responses, test_client):
    """Test handling of connection errors."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        body=requests.exceptions.ConnectionError(),
    )

    with pytest.raises(RetrieverConnectionError):
        test_client._request("GET", "/v1/test")


def test_request_retry_success(mock_responses, test_client):
    """Test successful retry after failures."""
    # First two calls fail with connection error
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        body=requests.exceptions.ConnectionError(),
    )
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        body=requests.exceptions.ConnectionError(),
    )
    # Third call succeeds
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        json={"status": "success"},
        status=200,
    )

    response = test_client._request("GET", "/v1/test")
    assert response == {"status": "success"}


def test_request_retry_exhausted(mock_responses, test_client):
    """Test when all retries are exhausted."""
    # All three calls fail
    for _ in range(3):
        mock_responses.add(
            mock_responses.GET,
            "https://api.tatry.dev/v1/test",
            body=requests.exceptions.ConnectionError(),
        )

    with pytest.raises(RetrieverConnectionError):
        test_client._request("GET", "/v1/test")


def test_request_invalid_json(mock_responses, test_client):
    """Test handling of invalid JSON response."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        body="Invalid JSON",
        status=200,
    )

    with pytest.raises(RetrieverAPIError):
        test_client._request("GET", "/v1/test")


def test_request_non_json_response(mock_responses, test_client):
    """Test handling of non-JSON response."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/test",
        body="Not a JSON response",
        status=200,
    )

    with pytest.raises(RetrieverAPIError) as exc:
        test_client._request("GET", "/v1/test")
    assert "Request failed" in str(exc.value)
