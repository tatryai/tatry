import pytest
from responses import RequestsMock

from tatry.client import API_URL
from tatry.models.sources import Source, SourceMetadata


@pytest.fixture
def mock_responses():
    with RequestsMock() as rsps:
        yield rsps


def test_list_sources(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/sources",
        json={
            "status": "success",
            "data": {
                "sources": [
                    {
                        "id": "wikipedia",
                        "name": "Wikipedia",
                        "type": "free",
                        "status": "active",
                        "description": "Wikipedia content source",
                        "coverage": ["general", "academic"],
                        "update_frequency": "daily",
                    },
                    {
                        "id": "arxiv",
                        "name": "arXiv",
                        "type": "free",
                        "status": "active",
                        "description": "Open access scientific papers",
                        "coverage": ["academic", "research"],
                        "update_frequency": "daily",
                    },
                ],
                "total": 2,
            },
        },
        status=200,
    )

    sources = client.sources.list_sources()
    assert isinstance(sources, list)
    assert len(sources) == 2
    assert all(isinstance(source, Source) for source in sources)
    assert sources[0].id == "wikipedia"
    assert sources[1].id == "arxiv"


def test_get_source(client, mock_responses):
    mock_responses.add(
        mock_responses.GET,
        f"{API_URL}/v1/sources/wikipedia",
        json={
            "status": "success",
            "data": {
                "id": "wikipedia",
                "name": "Wikipedia",
                "type": "free",
                "status": "active",
                "description": "Wikipedia content source",
                "coverage": ["general", "academic"],
                "update_frequency": "daily",
                "metadata": {
                    "content_quality_score": 0.95,
                    "total_documents": 6500000,
                    "languages": ["en", "es", "fr", "de"],
                },
            },
        },
        status=200,
    )

    source = client.sources.get_source("wikipedia")
    assert isinstance(source, Source)
    assert source.id == "wikipedia"
    assert source.name == "Wikipedia"
    assert source.type == "free"
    assert isinstance(source.metadata, SourceMetadata)
    assert source.metadata.content_quality_score == 0.95
    assert source.metadata.total_documents == 6500000
    assert "en" in source.metadata.languages
