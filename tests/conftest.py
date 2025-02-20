import pytest
from responses import RequestsMock


@pytest.fixture
def mock_responses():
    """Fixture providing mocked responses."""
    with RequestsMock() as rsps:
        yield rsps
