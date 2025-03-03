"""Tatry + Groq RAG test"""

import os

from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq  # Groq because it's free

from tatry.integrations.langchain import TatryRetriever

# API keys
TATRY_API_KEY = os.environ.get("TATRY_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialize retriever and LLM
retriever = TatryRetriever(api_key=TATRY_API_KEY, max_results=3)
llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192", temperature=0.1)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
)

query = "What are the latest treatments for type 2 diabetes?"

result = qa_chain.invoke({"query": query})

# Display results
print("\n=== ANSWER ===")
print(result["result"])

print("\n=== SOURCE DOCUMENTS ===")
for i, doc in enumerate(result["source_documents"]):
    print(f"\nDocument {i+1}:")
    print(f"Content: {doc.page_content[:150]}...")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
