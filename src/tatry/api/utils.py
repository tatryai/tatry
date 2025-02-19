from typing import Optional

from ..client import TatryRetriever
from ..models.utils import (
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    UsageResponse,
)


class UtilsAPI:
    def __init__(self, client: TatryRetriever):
        self.client = client

    def get_usage(self, month: Optional[str] = None) -> UsageResponse:
        """
        Get usage statistics.

        Args:
            month (str, optional): Month in YYYY-MM format

        Returns:
            UsageResponse: Usage statistics
        """
        params = {"month": month} if month else None
        response = self.client._request("GET", "/v1/usage", params=params)
        return UsageResponse(**response)

    def submit_feedback(
        self,
        feedback_type: str,
        description: str,
        metadata: Optional[dict] = None,
    ) -> FeedbackResponse:
        """
        Submit feedback about the API.

        Args:
            feedback_type (str): Type of feedback (bug/feature/other)
            description (str): Detailed feedback description
            metadata (dict, optional): Additional context

        Returns:
            FeedbackResponse: Feedback submission response
        """
        feedback = FeedbackRequest(
            type=feedback_type,
            description=description,
            metadata=metadata,
        )
        response = self.client._request(
            "POST",
            "/v1/feedback",
            json=feedback.model_dump(),
        )
        return FeedbackResponse(**response)

    def check_health(
        self,
    ) -> HealthResponse:
        """
        Check the health of the API.

        Returns:
            dict: Health check response
        """

        response = self.client._request("GET", "/v1/health")
        return HealthResponse(**response)
