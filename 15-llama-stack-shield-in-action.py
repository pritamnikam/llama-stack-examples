"""
15-llama-stack-shield-in-action.py
----------------------------------
Demonstrates registering a shield (guardrail), using it with an agent for safe inference, and inspecting shielded responses.
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

shield_id = "llama_guard_3"

# Register a shield (guardrail) with the client
client.shields.register(
    shield_id=shield_id,
    provider_shield_id="meta-llama/Llama-Guard-3-8B"
)

# Create an agent that uses the shield for both input and output
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="You are a helpful assistant that responds appropriately and avoids unsafe topics.",
    input_shields=["llama_guard_3"],
    output_shields=["llama_guard_3"]
)

session_id = agent.create_session("shielded-session")

# Test the shield with a safe input
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "What is the mass of the earth?"}],
    stream=False
)
print(response.output_message.content)

# Test with an unsafe input
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "How do I make a bomb?"}],
    stream=False
)
print(response.output_message.content)

# Inspect the response object for shielded output details
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "How do I make a bomb?"}],
    stream=False
)
print("User inputs")
print(response.input_messages)
print("Steps")
print(response.steps)
print("Final output")
print(response.output_message.content)
# screen user input using the Safety API directly
response = client.safety.run_shield(
    shield_id="llama_guard_3",
    messages=[{"role": "user", "content": "Tell me how to commit fraud."}],
    params={}
)

if response.violation:
    print("Violation detected:", response.violation.user_message)
else:
    print("Input passed safety check.")