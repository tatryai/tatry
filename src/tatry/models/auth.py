from datetime import datetime
from typing import List

from pydantic import BaseModel


class RateLimits(BaseModel):
    requests_per_minute: int
    requests_per_hour: int


class ValidateData(BaseModel):
    valid: bool
    permissions: List[str]
    organization_id: str
    rate_limits: RateLimits


class ValidateResponse(BaseModel):
    status: str
    data: ValidateData


class APIKey(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    last_used_at: datetime


class ListKeysData(BaseModel):
    keys: List[APIKey]
    total: int


class ListKeysResponse(BaseModel):
    status: str
    data: ListKeysData
