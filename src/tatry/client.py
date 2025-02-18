from typing import Optional, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import Config
from .exceptions import TatryAPIError, TatryAuthError, TatryConfigError, TatryTimeoutError
from .api.retrieve import RetrieveAPI
from .api.sources import SourcesAPI
from .api.utils import UtilsAPI
from .api.auth import AuthAPI

API_URL = "https://api.tatry.dev"

class TatryRetriever:
    """
    Main client for interacting with the Tatry API.
    
    Args:
        api_key (str): Your API key for authentication
        timeout (int, optional): Request timeout in seconds. Defaults to 30
        max_retries (int, optional): Maximum number of retries for failed requests. Defaults to 3
        
    Raises:
        TatryConfigError: If API key is empty or invalid
    """
    def __init__(
        self,
        api_key: str,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
    ):
        if not api_key or not isinstance(api_key, str):
            raise TatryConfigError("API key is required")
            
        self.config = Config(
            api_key=api_key,
            base_url=API_URL,
            timeout=timeout or 30,
            max_retries=max_retries or 3,
        )
        
        self.session = self._create_session()
        
        # Initialize API resources
        self.retrieve = RetrieveAPI(self)
        self.sources = SourcesAPI(self)
        self.utils = UtilsAPI(self)
        self.auth = AuthAPI(self)

    def _create_session(self) -> requests.Session:
        """Create and configure requests session."""
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        return session

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            path (str): API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Dict[str, Any]: Parsed JSON response
            
        Raises:
            TatryAPIError: If the API returns an error
            TatryAuthError: If authentication fails
            TatryTimeoutError: If the request times out
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
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise TatryAuthError("Authentication failed", status_code=401)
            raise TatryAPIError(
                f"API request failed: {str(e)}",
                status_code=e.response.status_code,
                response=e.response,
            )
        except requests.exceptions.Timeout as e:
            raise TatryTimeoutError(f"Request timed out: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise TatryAPIError(f"Request failed: {str(e)}")