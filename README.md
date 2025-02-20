# Tatry Python SDK

Official Python SDK for the Tatry Content Retrieval API.


## Installation

```bash
pip install tatry
```

## Quick Start

```python
from tatry import TatryRetriever

# Initialize the retriever
retriever = TatryRetriever(api_key="your_api_key")

# Search for documents
results = retriever.retrieve("quantum computing", max_results=5, ["medical"])
for doc in results.documents:
    print(f"Citation: {doc.metadata.citation}")
    print(f"Content: {doc.content[:200]}...")
    print(f"Relevance: {doc.relevance_score}")
    print("---")
```

## Features

- 🔍 **Content Search**: Search across multiple sources with relevance scoring
- 📚 **Source Management**: Browse and access different content sources
- 📊 **Usage Statistics**: Track your API usage
- 🔒 **Authentication**: Secure API key management
- 💬 **Feedback System**: Submit and track user feedback
- ⚡ **Batch Operations**: Perform multiple searches in one request
- 🛡️ **Type Safety**: Full type hinting support with Pydantic models
- 🔄 **Automatic Retries**: Built-in retry mechanism with exponential backoff

## Authentication

```python
from tatry import TatryRetriever

retriever = TatryRetriever(api_key="your_api_key")

# Validate your API key
validation = retriever.auth.validate_api_key()
print(f"API Key Valid: {validation.data.valid}")
print(f"Permissions: {validation.data.permissions}")
print(f"Rate Limits: {validation.data.rate_limits.requests_per_minute}/min")

# List all API keys
keys = retriever.auth.list_keys(status="active")
for key in keys:
    print(f"Key: {key.id}")
    print(f"Last Used: {key.last_used_at}")
```

## Content Retrieval

### Single Search

```python
# Basic search
results = retriever.retrieve.retrieve("artificial intelligence")

# Search with parameters
results = retriever.retrieve.retrieve(
    query="machine learning frameworks",
    max_results=10
)
```

### Batch Search

```python
# Perform multiple searches at once
queries = [
    {"query": "neural networks", "max_results": 5},
    {"query": "deep learning", "max_results": 3}
]
results = retriever.retrieve.batch_retrieve(queries)
```

## Source Management

```python
# List all available sources
sources = retriever.sources.list_sources()
for source in sources:
    print(f"Source: {source.name}")
    print(f"Type: {source.type}")
    print(f"Coverage: {', '.join(source.coverage)}")

# Get detailed information about a specific source
wikipedia = retriever.sources.get_source("wikipedia")
print(f"Total Documents: {wikipedia.metadata.total_documents}")
print(f"Languages: {', '.join(wikipedia.metadata.languages)}")
```

## Usage Statistics

```python
# Get current month's usage
usage = retriever.utils.get_usage()
print(f"Total Queries: {usage.data.usage.queries.total}")
print(f"Documents Retrieved: {usage.data.usage.documents.total}")

# Get usage for a specific month
usage = retriever.utils.get_usage(month="2024-01")
```

## Feedback System

```python
# Submit feedback
feedback = retriever.utils.submit_feedback(
    feedback_type="feature",
    description="Would love to see more academic sources",
    metadata={"user_type": "researcher"}
)
print(f"Feedback ID: {feedback.data.id}")
```

## Error Handling

```python
from tatry import TatryError, TatryAPIError, TatryAuthError

try:
    results = retriever.retrieve.search("quantum computing")
except TatryAuthError:
    print("Authentication failed")
except TatryAPIError as e:
    print(f"API error: {e.status_code}")
except TatryError as e:
    print(f"General error: {str(e)}")
```

## Configuration

```python
retriever = TatryRetriever(
    api_key="your_api_key",
    timeout=30,                         # Request timeout in seconds
    max_retries=3                      # Maximum retry attempts
)
```

## Development

```bash
# Clone the repository
git clone https://github.com/tatryai/tatry.git
cd tatry

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
