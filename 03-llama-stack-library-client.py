"""
03-llama-stack-library-client.py
-------------------------------
Demonstrates usage of the Llama Stack as a library client, including initialization and chat completion.
"""

import os  # For environment variable access
from llama_stack.distribution.library_client import LlamaStackAsLibraryClient  # Import the library client

# Initialize the library client with provider and API key
client = LlamaStackAsLibraryClient(
    "together",
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

print("Initializing...")
client.initialize()  # Explicit initialization
print("Ready")

# List and print available models
models = client.models.list()
print("Available Models:")
for model in models:
    print(f"- {model.identifier} ({model.model_type})")

print("\nSending a chat request:")
model_id = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

# Send a chat completion request
response = client.inference.chat_completion(
    model_id=model_id,
    messages=[
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "What is the chemical symbol for water?"},
    ],
)

# Display the assistant's response
print(response.completion_message.content)