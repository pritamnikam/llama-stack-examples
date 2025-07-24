"""
14-llama-stack-shield-list.py
----------------------------
Lists all available shields (safety/guardrail models) registered with the Llama Stack client.
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client

# Initialize the client with Together AI endpoint and API key
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# List all available shields (guardrails)
shields = client.shields.list()
print("Available shields:")
for shield in shields:
    # Print each shield's identifier and provider
    print(f"- {shield.identifier} - {shield.provider_id}") 