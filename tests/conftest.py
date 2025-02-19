import pytest

from tatry import TatryRetriever


@pytest.fixture
def client():
    """Create a test client with mock API key."""
    return TatryRetriever(api_key="test_api_key")


@pytest.fixture
def mock_responses():
    from responses import RequestsMock

    with RequestsMock() as rsps:
        yield rsps
