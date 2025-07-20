"""
12-llama-stack-tool-rag.py
-------------------------
Demonstrates how to register a vector database and insert documents for RAG (Retrieval-Augmented Generation) using Llama Stack.
"""

from llama_stack_client import RAGDocument  # For document representation
from llama_stack_client import LlamaStackClient  # Llama Stack client
import os  # For environment variable access

# Define a unique ID for your vector database
vector_db_id = "my_knowledge_base"

# Initialize the client with Together AI endpoint and API key
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# List available embedding models and their dimensions
models = client.models.list()
for m in models:
    if m.model_type == "embedding":
        print(m.identifier, m.metadata["embedding_dimension"])

# Register a new vector database for RAG
client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
    provider_id="faiss"
)

# Prepare documents to insert into the vector database
documents = [
    RAGDocument(
        document_id="doc_001",
        content="Alpaca 7 is the first Artificial General Intelligence or AGI model",
        mime_type="text/plain",
        metadata={"source": "docs/intro"}
    ),
    RAGDocument(
        document_id="doc_002",
        content="AGI refers to a type of artificial intelligence that has the ability to understand, learn, and apply knowledge across a wide range of tasks, much like a human being.",
        mime_type="text/plain",
        metadata={"source": "docs/api-overview"}
    )
]

# (Continue with document insertion and search logic as needed)
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=50
)

results = client.tool_runtime.rag_tool.query(
    vector_db_ids=[vector_db_id],
    content="What is Alpaca 7?"
)

for item in results.content:
    print(item)