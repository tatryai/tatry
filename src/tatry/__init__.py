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
from .retrievers.base import BaseRetriever
from .retrievers.tatry import TatryRetriever as CoreTatryRetriever

try:
    from .integrations.langchain import TatryRetriever as LangChainTatryRetriever

    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

TatryRetriever = CoreTatryRetriever

__all__ = [
    "BaseRetriever",
    "TatryRetriever",
    "CoreTatryRetriever",
    "RetrieverError",
    "RetrieverAPIError",
    "RetrieverAuthError",
    "RetrieverConfigError",
    "RetrieverTimeoutError",
    "RetrieverConnectionError",
]

if HAS_LANGCHAIN:
    __all__.append("LangChainTatryRetriever")
