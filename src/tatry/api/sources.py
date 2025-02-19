from typing import List

from ..client import TatryRetriever
from ..models.sources import GetSourceResponse, ListSourcesResponse, Source


class SourcesAPI:
    def __init__(self, client: TatryRetriever):
        self.client = client

    def list_sources(self) -> List[Source]:
        """
        List all available sources.

        Returns:
            List[Source]: List of available sources
        """
        response = self.client._request("GET", "/v1/sources")
        list_response = ListSourcesResponse(**response)
        return list_response.data.sources

    def get_source(self, source_id: str) -> Source:
        """
        Get detailed information about a specific source.

        Args:
            source_id (str): ID of the source to get

        Returns:
            Source: Detailed source information

        Raises:
            TatryAPIError: If the source doesn't exist
        """
        response = self.client._request("GET", f"/v1/sources/{source_id}")
        source_response = GetSourceResponse(**response)
        return source_response.data
