from typing import Any, Dict, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from ...config import Config
from ...exceptions import (
    RetrieverAPIError,
    RetrieverAuthError,
    RetrieverConfigError,
    RetrieverConnectionError,
    RetrieverTimeoutError,
)
from ..base import BaseRetriever


class TatryClient(BaseRetriever):
    """Base HTTP client for Tatry API."""

    def __init__(
        self,
        api_key: str,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        base_url: str = "https://api.tatry.dev",
    ):
        if not api_key or not isinstance(api_key, str):
            raise RetrieverConfigError("API key is required")

        self.config = Config(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout or 30,
            max_retries=max_retries or 3,
        )
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        return session

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            **kwargs: Additional arguments passed to requests.request

        Returns:
            Dict[str, Any]: JSON response from the API
        """
        url = f"{self.config.base_url}{path}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise RetrieverAuthError(
                    "Authentication failed", status_code=401, response=e.response
                )
            raise RetrieverAPIError(
                f"API request failed: {str(e)}",
                status_code=e.response.status_code,
                response=e.response,
            )
        except requests.exceptions.Timeout as e:
            raise RetrieverTimeoutError(f"Request timed out: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            raise RetrieverConnectionError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise RetrieverAPIError(f"Request failed: {str(e)}")
