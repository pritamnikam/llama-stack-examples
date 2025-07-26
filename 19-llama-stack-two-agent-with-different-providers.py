"""
19-llama-stack-two-agent-with-different-providers.py
---------------------------------------------------
Demonstrates running two Llama Stack agents with different providers (hosted vs. local/Ollama) side-by-side.
Shows how the same logic can be used with different models/environments, and compares outputs.
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction

# Initialize the client
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# You’ll see two different responses, likely similar in structure but possibly varying in length
# or specificity depending on the models’ capabilities. This confirms that our two agents, powered
# by different providers, are running side-by-side with the same core logic. However, you might 
# notice that the local model is unable to guess the country, whereas the larger hosted model does
# so with ease.
#
# This kind of setup is common in real-world teams, where dev/staging/prod environments use different
# infrastructure but share the same application logic.


agent_hosted = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",  # Served by Together
    instructions="You are a helpful AI assistant"
)

agent_local = Agent(
    client=client,
    model="llama3.2:1b",  # Served by Ollama locally
    instructions="You are a helpful AI assistant"
)

session_hosted = agent_hosted.create_session("hosted-session")
session_local = agent_local.create_session("local-session")

question = "What is the capital of the country whose flag has a red circle on a white background, and which is located in East Asia?"

response_hosted = agent_hosted.create_turn(
    session_id=session_hosted,
    messages=[{"role": "user", "content": question}],
    stream=False
)

response_local = agent_local.create_turn(
    session_id=session_local,
    messages=[{"role": "user", "content": question}],
    stream=False
)

print("Hosted Agent:", response_hosted.output_message.content)
print("\nLocal Agent:", response_local.output_message.content)