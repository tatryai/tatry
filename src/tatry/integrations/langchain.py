from typing import List

try:
    from langchain.schema.document import Document as LangChainDocument
    from langchain.schema.retriever import BaseRetriever as LangChainBaseRetriever
except ImportError:
    try:
        from langchain.schema import BaseRetriever as LangChainBaseRetriever
        from langchain.schema import Document as LangChainDocument
    except ImportError:
        raise ImportError(
            "LangChain is not installed. Please install it with `pip install langchain`."
        )

from ..retrievers.tatry import TatryRetriever as TatryImpl


class TatryRetriever(LangChainBaseRetriever):
    """
    Tatry retriever for LangChain.

    This class adapts the TatryRetriever to the LangChain interface.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tatry.dev",
        timeout: int = 30,
        max_retries: int = 3,
        sources: List[str] = None,
        max_results: int = 10,
    ):
        """
        Initialize the TatryRetriever.

        Args:
            api_key: API key for Tatry API
            base_url: Base URL for Tatry API
            timeout: Timeout for API requests in seconds
            max_retries: Maximum number of retries for API requests
            sources: List of source IDs to search
            max_results: Maximum number of results to return
        """
        LangChainBaseRetriever.__init__(self)

        self._config = {
            "api_key": api_key,
            "base_url": base_url,
            "timeout": timeout,
            "max_retries": max_retries,
            "sources": sources or [],
            "max_results": max_results,
        }

        self._client = TatryImpl(
            api_key=self._config["api_key"],
            base_url=self._config["base_url"],
            timeout=self._config["timeout"],
            max_retries=self._config["max_retries"],
        )

    def _get_relevant_documents(self, query: str) -> List[LangChainDocument]:
        """
        Get documents relevant to the query.

        Args:
            query: Query string

        Returns:
            List of relevant documents
        """
        response = self._client.retrieve(
            query=query,
            max_results=self._config["max_results"],
            sources=self._config["sources"],
        )

        documents = []
        for doc in response.documents:
            metadata = {
                "source": doc.metadata.source,
                "published_date": doc.metadata.published_date,
                "citation": doc.metadata.citation,
                "relevance_score": doc.relevance_score,
                "id": doc.id,
            }

            documents.append(
                LangChainDocument(
                    page_content=doc.content,
                    metadata=metadata,
                )
            )

        return documents
