try:
    from ._version import version as __version__
except ImportError:
    __version__ = "1.0.2"

from .retrievers.tatry import TatryRetriever
from .exceptions import (
    RetrieverError,
    RetrieverAPIError,
    RetrieverAuthError,
    RetrieverConfigError,
    RetrieverTimeoutError,
    RetrieverConnectionError,
)

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