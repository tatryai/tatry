import pytest

from tatry.retrievers.base import BaseRetriever


class MinimalRetriever(BaseRetriever):
    """Minimal implementation for testing abstract methods."""

    def _request(self, method: str, path: str, **kwargs):
        return {"status": "success"}

    def retrieve(self, query: str, max_results: int = 10):
        return self._request("GET", "/test")

    def batch_retrieve(self, queries):
        return self._request("POST", "/batch")

    def validate_api_key(self):
        return self._request("POST", "/validate")

    def list_sources(self):
        return self._request("GET", "/sources")

    def get_source(self, source_id: str):
        return self._request("GET", f"/sources/{source_id}")

    def submit_feedback(self, feedback_type: str, description: str, metadata=None):
        return self._request("POST", "/feedback")

    def check_health(self):
        return self._request("GET", "/health")


def test_minimal_implementation():
    """Test that all abstract methods can be implemented."""
    retriever = MinimalRetriever()

    assert retriever._request("GET", "/test") == {"status": "success"}
    assert retriever.retrieve("test") == {"status": "success"}
    assert retriever.batch_retrieve([]) == {"status": "success"}
    assert retriever.validate_api_key() == {"status": "success"}
    assert retriever.list_sources() == {"status": "success"}
    assert retriever.get_source("test") == {"status": "success"}
    assert retriever.submit_feedback("bug", "test") == {"status": "success"}
    assert retriever.check_health() == {"status": "success"}


def test_base_retriever_missing_methods():
    """Test that BaseRetriever requires all abstract methods to be implemented."""

    with pytest.raises(TypeError):

        class IncompleteRetriever(BaseRetriever):
            def _request(self, *args, **kwargs):
                pass

            # brak innych metod

        IncompleteRetriever()


def test_base_retriever_interface():
    """Test that BaseRetriever properly marks all methods as abstract."""

    class PartialRetriever(BaseRetriever):
        def _request(self, *args, **kwargs):
            pass

    with pytest.raises(TypeError) as exc:
        PartialRetriever()

    # Sprawdzamy czy informacja o błędzie zawiera wszystkie brakujące metody
    error_msg = str(exc.value)
    assert "retrieve" in error_msg
    assert "batch_retrieve" in error_msg
    assert "validate_api_key" in error_msg
    assert "list_sources" in error_msg
    assert "get_source" in error_msg
    assert "submit_feedback" in error_msg
    assert "check_health" in error_msg
