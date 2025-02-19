from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for the Tatry client."""

    api_key: str
    base_url: str = "http://localhost:8080"
    timeout: int = 30
    max_retries: int = 3
