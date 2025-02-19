from typing import List

from ..client import TatryRetriever
from ..models.retrieve import BatchQueryResult, BatchResponse, DocumentResponse


class RetrieveAPI:
    def __init__(self, client: TatryRetriever):
        self.client = client

    def retrieve(self, query: str, max_results: int = 10) -> DocumentResponse:
        """
        Search for documents using a query.

        Args:
            query (str): The search query
            max_results (int, optional): Maximum number of results to return.
            Defaults to 10

        Returns:
            DocumentResponse: Search results
        """
        response = self.client._request(
            "POST",
            "/v1/retrieve",
            json={"query": query, "max_results": max_results},
        )
        return DocumentResponse(**response)

    def batch_retrieve(
        self,
        queries: List[dict],
    ) -> List[BatchQueryResult]:
        """
        Perform multiple searches in one request.

        Args:
            queries (List[dict]): List of search queries with parameters

        Returns:
            List[BatchQueryResult]: List of search results
        """
        response = self.client._request(
            "POST",
            "/v1/retrieve/batch",
            json={"queries": queries},
        )
        batch_response = BatchResponse(**response)
        return batch_response.results
