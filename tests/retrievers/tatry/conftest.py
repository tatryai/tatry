import pytest

from tatry import TatryRetriever


@pytest.fixture
def tatry_client():
    """Fixture providing a Tatry client with test API key."""
    return TatryRetriever(api_key="test_key")
