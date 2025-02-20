try:
    from ._version import version as __version__
except ImportError:
    __version__ = "1.0.2"

from .exceptions import (
    RetrieverAPIError,
    RetrieverAuthError,
    RetrieverConfigError,
    RetrieverConnectionError,
    RetrieverError,
    RetrieverTimeoutError,
)
from .retrievers.tatry import TatryRetriever

__all__ = [
    "BaseRetriever",
    "TatryRetriever",
    "RetrieverError",
    "RetrieverAPIError",
    "RetrieverAuthError",
    "RetrieverConfigError",
    "RetrieverTimeoutError",
    "RetrieverConnectionError",
]
