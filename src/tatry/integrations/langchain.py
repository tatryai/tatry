from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

# Import LangChain's base retriever
try:
    from langchain.schema import BaseRetriever as LangChainBaseRetriever
    from langchain.schema import Document as LangChainDocument
except ImportError:
    raise ImportError(
        "LangChain is not installed. Please install it with `pip install langchain`."
    )

from ..retrievers.tatry import TatryRetriever as TatryImpl


class TatryRetriever(LangChainBaseRetriever, BaseModel):
    """
    Tatry retriever for LangChain.

    This class adapts the TatryRetriever to the LangChain interface.
    """

    api_key: str = Field(..., description="API key for Tatry API")
    base_url: str = Field("https://api.tatry.dev", description="Base URL for Tatry API")
    timeout: int = Field(30, description="Timeout for API requests in seconds")
    max_retries: int = Field(
        3, description="Maximum number of retries for API requests"
    )
    sources: List[str] = Field(
        default_factory=list, description="List of source IDs to search"
    )
    max_results: int = Field(10, description="Maximum number of results to return")

    _client: Optional[TatryImpl] = None

    model_config = {
        "arbitrary_types_allowed": True,  # Allow the TatryImpl type
    }

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._client = TatryImpl(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=self.max_retries,
        )

    @model_validator(mode="after")
    def initialize_client(self) -> "TatryRetriever":
        """Initialize the client if not already initialized."""
        if self._client is None:
            self._client = TatryImpl(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )
        return self

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
            max_results=self.max_results,
            sources=self.sources,
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
