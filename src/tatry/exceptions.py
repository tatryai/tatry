class TatryError(Exception):
    """Base exception for all Tatry client errors."""
    pass

class TatryAPIError(TatryError):
    """Raised when the API returns an error response."""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class TatryAuthError(TatryAPIError):
    """Raised when there are authentication issues."""
    pass

class TatryConfigError(TatryError):
    """Raised when there are configuration issues."""
    pass

class TatryTimeoutError(TatryError):
    """Raised when API requests time out."""
    pass