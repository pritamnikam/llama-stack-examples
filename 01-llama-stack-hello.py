"""
01-llama-stack-hello.py
----------------------
Demonstrates basic usage of the Llama Stack client:
- Lists available models
- Sends a simple chat completion request
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Import the Llama Stack client

# Initialize the client with base URL and API key
client = LlamaStackClient(
    base_url="http://0.0.0.0:8321", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

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