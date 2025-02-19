from typing import List, Optional

from pydantic import BaseModel


class SourceMetadata(BaseModel):
    content_quality_score: float
    total_documents: int
    languages: List[str]


class Source(BaseModel):
    id: str
    name: str
    type: str
    status: str
    description: str
    coverage: List[str]
    update_frequency: str
    metadata: Optional[SourceMetadata] = None


class ListSourcesData(BaseModel):
    sources: List[Source]
    total: int


class ListSourcesResponse(BaseModel):
    status: str
    data: ListSourcesData


class GetSourceResponse(BaseModel):
    status: str
    data: Source
