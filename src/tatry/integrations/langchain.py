"""
LangChain integration for the Tatry retriever.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

try:
    from langchain.callbacks.manager import CallbackManagerForRetrieverRun
    from langchain.schema import BaseRetriever as LangChainBaseRetriever
    from langchain.schema import Document

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

    class LangChainBaseRetriever:
        pass

    class Document:
        pass

    class CallbackManagerForRetrieverRun:
        pass


from ..retrievers.tatry import TatryRetriever as CoreTatryRetriever


class TatryRetriever(LangChainBaseRetriever, BaseModel):
    """Tatry retriever integration with LangChain."""

    tatry_client: CoreTatryRetriever = Field(default=None)
    max_results: int = Field(default=10)
    sources: List[str] = Field(default_factory=list)
    api_key: str = Field(default=None)
    timeout: Optional[int] = Field(default=None)
    max_retries: Optional[int] = Field(default=None)
    base_url: str = Field(default="https://api.tatry.dev")

    def __init__(self, **data):
        """
        Initialize a Tatry LangChain Retriever.
        """
        if not LANGCHAIN_AVAILABLE:
            raise ImportError(
                "Could not import langchain. Please install it with "
                "`pip install tatry[langchain]`."
            )

        super().__init__(**data)

        if self.tatry_client is None and self.api_key is not None:
            self.tatry_client = CoreTatryRetriever(
                api_key=self.api_key,
                timeout=self.timeout,
                max_retries=self.max_retries,
                base_url=self.base_url,
            )

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
    ) -> List[Document]:
        """
        Get documents relevant to a query.

        Args:
            query: Query string
            run_manager: Callback manager for the retriever run

        Returns:
            List of Documents
        """
        if self.tatry_client is None:
            raise ValueError(
                "Tatry client is not initialized. Please provide an API key."
            )

        response = self.tatry_client.retrieve(
            query=query,
            max_results=self.max_results,
            sources=self.sources,
        )

        documents = []
        for doc in response.documents:
            metadata = {
                "id": doc.id,
                "source": doc.metadata.source,
                "published_date": doc.metadata.published_date,
                "citation": doc.metadata.citation,
                "relevance_score": doc.relevance_score,
            }
            documents.append(Document(page_content=doc.content, metadata=metadata))

        return documents
