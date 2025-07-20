"""
09-llama-stack-list-tools.py
---------------------------
Lists all available tools registered with the Llama Stack client.
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Import the Llama Stack client

# Initialize the client with API key
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# List and print all available tools
print("Available Tools:")
tools = client.tools.list()
for tool in tools:
    print(f"- {tool.toolgroup_id} - {tool.identifier} - {tool.description}")