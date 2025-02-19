from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from ..models.retrieve import BatchQueryResult, DocumentResponse
from ..models.auth import ValidateResponse, APIKey
from ..models.sources import Source
from ..models.utils import UsageResponse, FeedbackResponse, HealthResponse


class BaseRetriever(ABC):
    """Base class defining the retriever interface."""

    @abstractmethod
    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make an HTTP request to the API."""
        pass

    @abstractmethod
    def retrieve(self, query: str, max_results: int = 10) -> DocumentResponse:
        """Search for documents using a query."""
        pass

    @abstractmethod
    def batch_retrieve(self, queries: List[Dict]) -> List[BatchQueryResult]:
        """Perform multiple searches in one request."""
        pass

    @abstractmethod
    def validate_key(self) -> ValidateResponse:
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
        self,
        feedback_type: str,
        description: str,
        metadata: Optional[Dict] = None
    ) -> FeedbackResponse:
        """Submit feedback."""
        pass

    @abstractmethod
    def check_health(self) -> HealthResponse:
        """Check service health."""
        pass