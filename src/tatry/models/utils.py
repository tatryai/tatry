from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class TimeRange(BaseModel):
    month: str


class QueryUsage(BaseModel):
    total: int
    by_source: Dict[str, int]


class DocumentUsage(BaseModel):
    total: int
    by_source: Dict[str, int]


class Usage(BaseModel):
    queries: QueryUsage
    documents: DocumentUsage


class UsageData(BaseModel):
    time_range: TimeRange
    usage: Usage


class UsageResponse(BaseModel):
    status: str
    data: UsageData


class FeedbackRequest(BaseModel):
    type: str
    description: str
    metadata: Optional[Dict] = None


class FeedbackData(BaseModel):
    id: str
    received_at: datetime
    message: str


class FeedbackResponse(BaseModel):
    status: str
    data: FeedbackData


class HealthResponse(BaseModel):
    status: str
    data: Dict[str, str]
