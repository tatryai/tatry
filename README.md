# Tatry

Python client for the Tatry Content Retrieval API

## Installation

Install from PyPI:

```bash
pip install tatry
```

To include LangChain integration:

```bash
pip install tatry[langchain]
```

## Basic Usage

```python
from tatry import TatryRetriever

# Initialize the client
retriever = TatryRetriever(api_key="your-api-key")

# Search for documents
results = retriever.retrieve(
    query="example query",
    max_results=5,
    sources=["source1", "source2"]
)

# Access the results
for doc in results.documents:
    print(f"Document ID: {doc.id}")
    print(f"Content: {doc.content}")
    print(f"Relevance: {doc.relevance_score}")
    print(f"Source: {doc.metadata.source}")
    print(f"Published Date: {doc.metadata.published_date}")
    print("---")
```

## Features

- Simple and intuitive interface for retrieving relevant content
- Support for multiple sources in a single query
- Batch retrieval for efficiently processing multiple queries
- Comprehensive error handling
- Rate limiting and retry capabilities
- Detailed document metadata

## LangChain Integration

Tatry can be seamlessly integrated with LangChain:

```python
from tatry.integrations.langchain import TatryRetriever

# Initialize the retriever
retriever = TatryRetriever(
    api_key="your-api-key",
    max_results=5,
    sources=["source1", "source2"]
)

# Use it in any LangChain pipeline
documents = retriever.get_relevant_documents("your query")

# Example with a RetrievalQA chain
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever
)

result = qa.run("What is the capital of France?")
```

## API Endpoints

The client supports the following API endpoints:

### Document Retrieval

```python
# Simple retrieve
response = retriever.retrieve(query="example", max_results=10)

# Batch retrieve
queries = [
    {"query": "example 1", "max_results": 5},
    {"query": "example 2", "max_results": 10, "sources": ["source1"]}
]
batch_response = retriever.batch_retrieve(queries)
```



### Authentication

```python
# Validate your API key
validation = retriever.validate_api_key()
```

## Error Handling

The client includes various exception types to help you handle errors:

```python
from tatry import (
    RetrieverError,
    RetrieverAPIError,
    RetrieverAuthError,
    RetrieverConfigError,
    RetrieverTimeoutError,
    RetrieverConnectionError,
)

try:
    retriever.retrieve("example")
except RetrieverAuthError:
    print("Authentication failed")
except RetrieverTimeoutError:
    print("Request timed out")
except RetrieverConnectionError:
    print("Connection error")
except RetrieverAPIError as e:
    print(f"API error: {e.status_code}")
    print(f"Details: {e.details}")
except RetrieverError:
    print("Generic error")
```

## Development

To set up the development environment:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

