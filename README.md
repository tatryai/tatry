# Tatry

A Python client for interacting with the Tatry API to retrieve documents based on search queries.

## Installation

```bash
pip install tatry
```

## Quick Start

```python
from tatry import TatryRetriever

# Initialize the client
retriever = TatryRetriever(
    api_key="your_api_key"
)

# Validate your API key
validation = retriever.validate_api_key()
print(f"API key valid: {validation.data.valid}")
print(f"Permissions: {validation.data.permissions}")

# Perform a simple search
results = retriever.retrieve(
    query="climate change impact on agriculture",
    max_results=5,
    sources=["source_id_1", "source_id_2"]  # optional
)

# Print retrieved documents
for doc in results.documents:
    print(f"Document ID: {doc.id}")
    print(f"Score: {doc.relevance_score}")
    print(f"Source: {doc.metadata.source}")
    print(f"Content: {doc.content[:100]}...")
    print("-" * 50)
```

## API Reference

### Validation

#### `validate_api_key()`

Validates the API key and returns information about associated permissions and rate limits.

**Returns:**
- `ValidateResponse` object containing:
  - `status`: API response status
  - `data`: Validation data including:
    - `valid`: Boolean indicating if the key is valid
    - `permissions`: List of permissions granted to this key
    - `organization_id`: Organization ID for the key

**Example:**
```python
validation = retriever.validate_api_key()
if validation.data.valid:
    print("API key is valid")
    print(f"Permissions: {validation.data.permissions}")
else:
    print("Invalid API key")
```

### Document Retrieval

#### `retrieve(query, max_results=10, sources=[])`

Searches for documents using a text query.

**Parameters:**
- `query`: String containing the search query
- `max_results`: Maximum number of results to return (default: 10)
- `sources`: Optional list of source IDs to restrict the search to

**Returns:**
- `DocumentResponse` object containing:
  - `documents`: List of matching `Document` objects
  - `total`: Total number of matches found

**Example:**
```python
results = retriever.retrieve(
    query="renewable energy developments",
    max_results=5,
    sources=["news_source", "academic_papers"]
)

print(f"Found {results.total} documents")
for doc in results.documents:
    print(f"{doc.id}: {doc.content[:50]}... (score: {doc.relevance_score})")
```

#### `batch_retrieve(queries)`

Performs multiple searches in a single request.

**Parameters:**
- `queries`: List of query dictionaries, each containing:
  - `query`: The search query string
  - `max_results`: Maximum results to return for this query (optional)
  - `sources`: List of source IDs to search (optional)

**Returns:**
- List of `BatchQueryResult` objects, each containing:
  - `query_id`: The query identifier that was provided
  - `documents`: List of matching `Document` objects

**Example:**
```python
batch_results = retriever.batch_retrieve([
    {"query": "electric vehicles", "max_results": 3},
    {"query": "solar panel efficiency", "max_results": 5, "sources": ["technical_reports"]},
])

for result in batch_results:
    print(f"Query ID: {result.query_id}")
    print(f"Found {len(result.documents)} documents")
    for doc in result.documents:
        print(f"- {doc.metadata.source}: {doc.content[:40]}...")
```

## Error Handling

The library provides several exception types to handle different error scenarios:

```python
try:
    results = retriever.retrieve("my query")
except RetrieverAuthError as e:
    print(f"Authentication failed: {e}")
except RetrieverTimeoutError as e:
    print(f"Request timed out: {e}")
except RetrieverConnectionError as e:
    print(f"Connection issue: {e}")
except RetrieverAPIError as e:
    print(f"API error: {e} (Status: {e.status_code})")
except RetrieverError as e:
    print(f"General error: {e}")
```

## Configuration

When initializing the client, you can configure several parameters:

```python
retriever = TatryRetriever(
    api_key="your_api_key",
    timeout=30,  # Request timeout in seconds
    max_retries=3  # Maximum number of retry attempts
)
```