# tests/test_client.py
import pytest
import requests
import responses.matchers
from responses import RequestsMock

from tatry import (
    TatryAPIError,
    TatryAuthError,
    TatryConfigError,
    TatryRetriever,
    TatryTimeoutError,
)
from tatry.client import API_URL


def test_client_initialization():
    client = TatryRetriever(api_key="test_key")
    assert client.config.api_key == "test_key"
    assert client.config.base_url == API_URL
    assert client.config.timeout == 30
    assert client.config.max_retries == 3


def test_client_custom_timeouts():
    client = TatryRetriever(api_key="test_key", timeout=60, max_retries=5)

    assert client.config.api_key == "test_key"
    assert client.config.base_url == API_URL
    assert client.config.timeout == 60
    assert client.config.max_retries == 5


def test_client_missing_api_key():
    with pytest.raises(TatryConfigError) as exc:
        TatryRetriever(api_key="")
    assert str(exc.value) == "API key is required"


def test_client_invalid_api_key_type():
    with pytest.raises(TatryConfigError) as exc:
        TatryRetriever(api_key=123)  # type: ignore
    assert str(exc.value) == "API key is required"


def test_client_none_api_key():
    with pytest.raises(TatryConfigError) as exc:
        TatryRetriever(api_key=None)  # type: ignore
    assert str(exc.value) == "API key is required"


def test_client_session_headers():
    client = TatryRetriever(api_key="test_key")
    headers = client.session.headers

    assert headers["Authorization"] == "Bearer test_key"
    assert headers["Content-Type"] == "application/json"
    assert headers["Accept"] == "application/json"


@pytest.fixture
def mock_responses():
    with RequestsMock() as rsps:
        yield rsps


def test_request_successful(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        json={"status": "success", "data": {"key": "value"}},
        status=200,
    )

    response = client._request("GET", "/v1/test")
    assert response["status"] == "success"
    assert response["data"]["key"] == "value"


def test_request_with_params(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        match=[responses.matchers.query_param_matcher({"param": "value"})],
        json={"status": "success"},
        status=200,
    )

    response = client._request("GET", "/v1/test", params={"param": "value"})
    assert response["status"] == "success"


def test_request_with_json_data(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/test",
        match=[responses.matchers.json_params_matcher({"data": "value"})],
        json={"status": "success"},
        status=200,
    )

    response = client._request("POST", "/v1/test", json={"data": "value"})
    assert response["status"] == "success"


def test_request_auth_error(mock_responses):
    client = TatryRetriever(api_key="invalid_key")
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        json={"error": "Invalid API key"},
        status=401,
    )

    with pytest.raises(TatryAuthError) as exc:
        client._request("GET", "/v1/test")
    assert exc.value.status_code == 401


def test_request_api_error(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        json={"error": "Bad request"},
        status=400,
    )

    with pytest.raises(TatryAPIError) as exc:
        client._request("GET", "/v1/test")
    assert exc.value.status_code == 400


def test_request_api_error_with_empty_response(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET, f"{API_URL}/v1/test", body="", status=500  # Empty response
    )

    with pytest.raises(TatryAPIError) as exc:
        client._request("GET", "/v1/test")
    assert exc.value.status_code == 500


def test_request_timeout(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET, f"{API_URL}/v1/test", body=requests.exceptions.Timeout()
    )

    with pytest.raises(TatryTimeoutError):
        client._request("GET", "/v1/test")


def test_request_connection_error(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        body=requests.exceptions.ConnectionError(),
    )

    with pytest.raises(TatryAPIError) as exc:
        client._request("GET", "/v1/test")
    assert "Request failed" in str(exc.value)


def test_request_invalid_json_response(mock_responses):
    client = TatryRetriever(api_key="test_key")
    mock_responses.add(
        mock_responses.GET, f"{API_URL}/v1/test", body="Invalid JSON", status=200
    )

    with pytest.raises(TatryAPIError) as exc:
        client._request("GET", "/v1/test")
    assert "Request failed" in str(exc.value)


def test_request_retry_success(mock_responses):
    client = TatryRetriever(api_key="test_key")

    # First two requests fail
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        body=requests.exceptions.ConnectionError(),
    )
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/test",
        body=requests.exceptions.ConnectionError(),
    )

    # Third request succeeds
    mock_responses.add(
        mock_responses.GET, f"{API_URL}/v1/test", json={"status": "success"}, status=200
    )

    response = client._request("GET", "/v1/test")
    assert response["status"] == "success"


def test_request_max_retries_exceeded(mock_responses):
    client = TatryRetriever(api_key="test_key", max_retries=2)

    # All requests fail
    for _ in range(3):
        mock_responses.add(
            mock_responses.GET,
            f"{API_URL}/v1/test",
            body=requests.exceptions.ConnectionError(),
        )

    with pytest.raises(TatryAPIError):
        client._request("GET", "/v1/test")


def test_api_resources_initialization():
    client = TatryRetriever(api_key="test_key")

    assert hasattr(client, "retrieve")
    assert hasattr(client, "sources")
    assert hasattr(client, "utils")
    assert hasattr(client, "auth")
