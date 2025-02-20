from typing import Dict, List, Optional

from ...models.auth import ValidateResponse
from ...models.retrieve import BatchQueryResult, DocumentResponse
from ...models.sources import Source
from ...models.utils import FeedbackResponse, HealthResponse
from .client import TatryClient


class TatryImplementation(TatryClient):
    """Implementation of Tatry API endpoints."""

    def retrieve(
        self, query: str, max_results: int = 10, sources: List[str] = []
    ) -> DocumentResponse:
        response = self._request(
            "POST",
            "/v1/retrieve",
            json={"query": query, "max_results": max_results, "sources": sources},
        )
        return DocumentResponse.model_validate(response)

    def batch_retrieve(self, queries: List[Dict]) -> List[BatchQueryResult]:
        response = self._request(
            "POST",
            "/v1/retrieve/batch",
            json={"queries": queries},
        )
        return [
            BatchQueryResult.model_validate(result) for result in response["results"]
        ]

    def validate_api_key(self) -> ValidateResponse:
        response = self._request("POST", "/v1/auth/validate")
        return ValidateResponse.model_validate(response)

    def list_sources(self) -> List[Source]:
        response = self._request("GET", "/v1/sources")
        return [Source.model_validate(source) for source in response["data"]["sources"]]

    def get_source(self, source_id: str) -> Source:
        response = self._request("GET", f"/v1/sources/{source_id}")
        return Source.model_validate(response["data"])

    def submit_feedback(
        self, feedback_type: str, description: str, metadata: Optional[Dict] = None
    ) -> FeedbackResponse:
        data = {
            "type": feedback_type,
            "description": description,
            "metadata": metadata or {},
        }
        response = self._request("POST", "/v1/feedback", json=data)
        return FeedbackResponse.model_validate(response)

    def check_health(self) -> HealthResponse:
        response = self._request("GET", "/v1/health")
        return HealthResponse.model_validate(response)
