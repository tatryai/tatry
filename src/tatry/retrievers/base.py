from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..models.auth import ValidateResponse
from ..models.retrieve import BatchQueryResult, DocumentResponse
from ..models.sources import Source
from ..models.utils import FeedbackResponse, HealthResponse


class BaseRetriever(ABC):
    """Base class defining the retriever interface."""

    @abstractmethod
    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            **kwargs: Additional arguments to pass to the request
        """
        pass

    @abstractmethod
    def retrieve(
        self, query: str, max_results: int = 10, sources: List[str] = []
    ) -> DocumentResponse:
        """Search for documents using a query."""
        pass

    @abstractmethod
    def batch_retrieve(self, queries: List[Dict]) -> List[BatchQueryResult]:
        """Perform multiple searches in one request."""
        pass

    @abstractmethod
    def validate_api_key(self) -> ValidateResponse:
        """Validate the API key."""
        pass

    @abstractmethod
    def list_sources(self) -> List[Source]:
        """List all available sources."""
        pass

    @abstractmethod
    def get_source(self, source_id: str) -> Source:
        """Get information about a specific source."""
        pass

    @abstractmethod
    def submit_feedback(
        self, feedback_type: str, description: str, metadata: Optional[Dict] = None
    ) -> FeedbackResponse:
        """Submit feedback."""
        pass

    @abstractmethod
    def check_health(self) -> HealthResponse:
        """Check service health."""
        pass
