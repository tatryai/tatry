from typing import List, Optional
from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    source: str
    published_date: str
    title: str

class Document(BaseModel):
    id: str
    content: str
    metadata: DocumentMetadata
    relevance_score: float

class DocumentResponse(BaseModel):
    documents: List[Document]
    total: int

class BatchQueryResult(BaseModel):
    query_id: int
    documents: List[Document]

class BatchResponse(BaseModel):
    results: List[BatchQueryResult]