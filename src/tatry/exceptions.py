from typing import Any, Dict, Optional


class RetrieverError(Exception):
    """Base exception for all retriever errors."""

    pass


class RetrieverAPIError(RetrieverError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
        details: Optional[Dict] = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response = response
        self.details = details or {}


class RetrieverAuthError(RetrieverAPIError):
    """Raised when there are authentication issues."""

    pass


class RetrieverConfigError(RetrieverError):
    """Raised when there are configuration issues."""

    pass


class RetrieverTimeoutError(RetrieverError):
    """Raised when API requests time out."""

    pass


class RetrieverConnectionError(RetrieverError):
    """Raised when there are connection issues."""

    pass
