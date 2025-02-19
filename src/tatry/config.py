from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for the Retriever client."""

    api_key: str
    base_url: str
    timeout: int = 30
    max_retries: int = 3
