import pytest
from responses import RequestsMock

from tatry.client import API_URL
from tatry.models.retrieve import BatchQueryResult, DocumentResponse


@pytest.fixture
def mock_responses():
    with RequestsMock() as rsps:
        yield rsps


def test_retrieve_basic(client, mock_responses):
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/retrieve",
        json={
            "documents": [
                {
                    "id": "doc_1",
                    "content": "Sample content",
                    "metadata": {
                        "source": "wikipedia",
                        "published_date": "2024-02-18",
                        "title": "Sample Document",
                    },
                    "relevance_score": 0.95,
                }
            ],
            "total": 1,
        },
        status=200,
    )

    response = client.retrieve.retrieve("test query")
    assert isinstance(response, DocumentResponse)
    assert len(response.documents) == 1
    assert response.documents[0].id == "doc_1"
    assert response.documents[0].relevance_score == 0.95


def test_batch_retrieve(client, mock_responses):
    mock_responses.add(
        mock_responses.POST,
        f"{API_URL}/v1/retrieve/batch",
        json={
            "results": [
                {
                    "query_id": 0,
                    "documents": [
                        {
                            "id": "doc_1",
                            "content": "First query content",
                            "metadata": {
                                "source": "wikipedia",
                                "published_date": "2024-02-18",
                                "title": "First Document",
                            },
                            "relevance_score": 0.9,
                        }
                    ],
                },
                {
                    "query_id": 1,
                    "documents": [
                        {
                            "id": "doc_2",
                            "content": "Second query content",
                            "metadata": {
                                "source": "arxiv",
                                "published_date": "2024-02-18",
                                "title": "Second Document",
                            },
                            "relevance_score": 0.8,
                        }
                    ],
                },
            ]
        },
        status=200,
    )

    queries = [
        {"query": "first query", "max_results": 1},
        {"query": "second query", "max_results": 1},
    ]
    results = client.retrieve.batch_retrieve(queries)
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(result, BatchQueryResult) for result in results)
    assert results[0].query_id == 0
    assert results[1].query_id == 1
    assert len(results[0].documents) == 1
    assert len(results[1].documents) == 1
    assert results[0].documents[0].metadata.source == "wikipedia"
    assert results[1].documents[0].metadata.source == "arxiv"
