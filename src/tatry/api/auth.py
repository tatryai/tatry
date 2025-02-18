from typing import List, Optional
from ..models.auth import ValidateResponse, APIKey

class AuthAPI:
    def __init__(self, client):
        self.client = client

    def validate_key(self) -> ValidateResponse:
        """
        Validate the current API key.
        
        Returns:
            ValidateResponse: Validation result including permissions and rate limits
            
        Raises:
            TatryAuthError: If the API key is invalid
        """
        response = self.client._request("POST", "/v1/auth/validate")
        return ValidateResponse(**response)

    def list_keys(
        self,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[APIKey]:
        """
        List all API keys for the organization.
        
        Args:
            status (str, optional): Filter keys by status (active/inactive)
            limit (int, optional): Maximum number of keys to return
            offset (int, optional): Number of keys to skip
            
        Returns:
            List[APIKey]: List of API keys
        """
        params = {}
        if status:
            params["status"] = status
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        response = self.client._request("GET", "/v1/auth/keys", params=params)
        return [APIKey(**key) for key in response["data"]["keys"]]