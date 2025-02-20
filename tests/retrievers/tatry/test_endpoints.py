import pytest
import responses

from tatry.exceptions import RetrieverAPIError
from tatry.models.auth import ValidateResponse
from tatry.models.retrieve import BatchQueryResult, DocumentResponse
from tatry.models.sources import Source


def test_retrieve(mock_responses, tatry_client):
    """Test retrieve endpoint."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/retrieve",
        json={
            "documents": [
                {
                    "id": "doc1",
                    "content": "Test content",
                    "metadata": {
                        "source": "test",
                        "published_date": "2024-01-01",
                        "citation": "Test Document",
                    },
                    "relevance_score": 0.95,
                }
            ],
            "total": 1,
        },
        status=200,
    )

    response = tatry_client.retrieve("test query")
    assert isinstance(response, DocumentResponse)
    assert len(response.documents) == 1
    assert response.documents[0].id == "doc1"
    assert response.documents[0].relevance_score == 0.95


def test_batch_retrieve(mock_responses, tatry_client):
    """Test batch retrieve endpoint."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/retrieve/batch",
        json={
            "results": [
                {
                    "query_id": 0,
                    "documents": [
                        {
                            "id": "doc1",
                            "content": "Test content 1",
                            "metadata": {
                                "source": "test",
                                "published_date": "2024-01-01",
                                "citation": "Test Document 1",
                            },
                            "relevance_score": 0.95,
                        }
                    ],
                },
                {
                    "query_id": 1,
                    "documents": [
                        {
                            "id": "doc2",
                            "content": "Test content 2",
                            "metadata": {
                                "source": "test",
                                "published_date": "2024-01-01",
                                "citation": "Test Document 2",
                            },
                            "relevance_score": 0.85,
                        }
                    ],
                },
            ]
        },
        status=200,
    )

    queries = [
        {"query": "test 1", "max_results": 1},
        {"query": "test 2", "max_results": 1},
    ]
    results = tatry_client.batch_retrieve(queries)

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(result, BatchQueryResult) for result in results)
    assert results[0].query_id == 0
    assert results[1].query_id == 1


def test_validate_api_key(mock_responses, tatry_client):
    """Test key validation endpoint."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/auth/validate",
        json={
            "status": "success",
            "data": {
                "valid": True,
                "permissions": ["read", "write"],
                "organization_id": "org_123",
                "rate_limits": {"requests_per_minute": 100, "requests_per_hour": 1000},
            },
        },
        status=200,
    )

    response = tatry_client.validate_api_key()
    assert isinstance(response, ValidateResponse)
    assert response.data.valid
    assert "read" in response.data.permissions
    assert response.data.organization_id == "org_123"


def test_list_sources(mock_responses, tatry_client):
    """Test list sources endpoint."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/sources",
        json={
            "status": "success",
            "data": {
                "sources": [
                    {
                        "id": "source1",
                        "name": "Test Source",
                        "type": "free",
                        "status": "active",
                        "description": "Test description",
                        "coverage": ["general"],
                        "update_frequency": "daily",
                    }
                ],
                "total": 1,
            },
        },
        status=200,
    )

    sources = tatry_client.list_sources()
    assert isinstance(sources, list)
    assert len(sources) == 1
    assert isinstance(sources[0], Source)
    assert sources[0].id == "source1"
    assert sources[0].status == "active"


def test_batch_retrieve_empty_queries(mock_responses, tatry_client):
    """Test batch retrieve with empty queries list."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/retrieve/batch",
        json={"results": []},
        status=200,
    )

    results = tatry_client.batch_retrieve([])
    assert isinstance(results, list)
    assert len(results) == 0


def test_submit_feedback_with_metadata(mock_responses, tatry_client):
    """Test submit_feedback with metadata."""
    metadata = {"browser": "test", "version": "1.0"}

    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/feedback",
        match=[
            responses.matchers.json_params_matcher(
                {"type": "bug", "description": "test bug", "metadata": metadata}
            )
        ],
        json={
            "status": "success",
            "data": {
                "id": "fb_1",
                "received_at": "2024-01-01T00:00:00Z",
                "message": "Thank you for your feedback",
            },
        },
        status=200,
    )

    response = tatry_client.submit_feedback(
        feedback_type="bug", description="test bug", metadata=metadata
    )
    assert response.status == "success"
    assert response.data.id == "fb_1"


def test_batch_retrieve_empty(mock_responses, tatry_client):
    """Test batch_retrieve with empty list."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/retrieve/batch",
        json={"results": []},
    )

    results = tatry_client.batch_retrieve([])
    assert len(results) == 0


def test_submit_feedback_full(mock_responses, tatry_client):
    """Test submit_feedback with all parameters."""
    metadata = {"browser": "test", "version": "1.0"}

    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/feedback",
        match=[
            responses.matchers.json_params_matcher(
                {"type": "bug", "description": "test", "metadata": metadata}
            )
        ],
        json={
            "status": "success",
            "data": {
                "id": "fb_1",
                "received_at": "2024-01-01T00:00:00Z",
                "message": "Thanks",
            },
        },
    )

    response = tatry_client.submit_feedback(
        feedback_type="bug", description="test", metadata=metadata
    )
    assert response.data.id == "fb_1"


def test_submit_feedback_no_metadata(mock_responses, tatry_client):
    """Test submit_feedback without metadata."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/feedback",
        match=[
            responses.matchers.json_params_matcher(
                {"type": "bug", "description": "test", "metadata": {}}
            )
        ],
        json={
            "status": "success",
            "data": {
                "id": "fb_2",
                "received_at": "2024-01-01T00:00:00Z",
                "message": "Thanks",
            },
        },
    )

    response = tatry_client.submit_feedback(feedback_type="bug", description="test")
    assert response.data.id == "fb_2"


def test_batch_retrieve_empty_list(mock_responses, tatry_client):
    """Test batch_retrieve with empty list."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/retrieve/batch",
        json={"results": []},
    )

    results = tatry_client.batch_retrieve([])
    assert isinstance(results, list)
    assert len(results) == 0


def test_get_source_invalid_id(mock_responses, tatry_client):
    """Test get_source with invalid ID."""
    mock_responses.add(
        mock_responses.GET,
        "https://api.tatry.dev/v1/sources/invalid",
        json={"error": "Source not found"},
        status=404,
    )

    with pytest.raises(RetrieverAPIError) as exc:
        tatry_client.get_source("invalid")
    assert exc.value.status_code == 404


def test_retrieve_with_max_results(mock_responses, tatry_client):
    """Test retrieve with custom max_results."""
    mock_responses.add(
        mock_responses.POST,
        "https://api.tatry.dev/v1/retrieve",
        match=[
            responses.matchers.json_params_matcher(
                {"query": "test", "max_results": 5, "sources": []}
            )
        ],
        json={"documents": [], "total": 0},
    )

    response = tatry_client.retrieve("test", max_results=5)
    assert isinstance(response, DocumentResponse)
