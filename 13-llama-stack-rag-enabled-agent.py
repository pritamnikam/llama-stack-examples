"""
13-llama-stack-rag-enabled-agent.py
-----------------------------------
Demonstrates a Llama Stack Agent integrated with Retrieval-Augmented Generation (RAG) for knowledge-augmented Q&A.
"""

# The model we are using for inference, Llama 3.2, has a knowledge cutoff date of December 2023.
# Without using RAG, Llama 3.2 will not be able to accurately answer questions about Llama Stack; it might hallucinate instead.

from llama_stack_client import RAGDocument  # For document representation
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction
from llama_stack_client import AgentEventLogger  # For streaming/logging agent events
from termcolor import cprint  # For colored terminal output
import os  # For environment variable access

# Initialize the client with Together AI endpoint and API key
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# Register a vector database for RAG
vector_db_id = "my_knowledge_base"
client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
    provider_id="faiss"
)

# Prepare and load documents into the vector database
urls = [
    "index.md",
    "getting_started/index.md",
    "getting_started/detailed_tutorial.md",
    "concepts/index.md",
    "concepts/evaluation_concepts.md"
]
documents = [
    RAGDocument(
        document_id=f"num-{i}",
        content=f"https://raw.githubusercontent.com/meta-llama/llama-stack/refs/heads/main/docs/source/{url}",
        mime_type="text/plain",
        metadata={},
    )
    for i, url in enumerate(urls)
]

print("Inserting documents into the database")
client.tool_runtime.rag_tool.insert(
    documents=documents,
    vector_db_id=vector_db_id,
    chunk_size_in_tokens=256
)
print("Documents loaded")

# Create an agent with RAG tool enabled
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="""
        You are a helpful and knowledgeable AI assistant integrated with a 
        Retrieval-Augmented Generation (RAG) tool. Your primary responsibility 
        is to answer user questions accurately and comprehensively.

        Whenever a user asks a question related to llama stack, you must use the 
        RAG tool to retrieve the most relevant and up-to-date information before responding.
        If you do not find any relevant information, let the user know.
        
        For other questions outside this domain, use your general knowledge as usual.
        """,
    tools=[
        {
            "name": "builtin::rag/knowledge_search",
            "args": {"vector_db_ids": ["my_knowledge_base"]}
        }
    ]
)

# Create a session for RAG Q&A
session_id = agent.create_session("rag-qa-session")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        cprint("Ending conversation. Goodbye!", "blue")
        break
    # Create a new turn with user input
    response = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )
    # Stream and print the agent's response
    for log in AgentEventLogger().log(response):
        log.print()
        log.print()