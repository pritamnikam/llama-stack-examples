"""
16-llama-stack-telemetry.py
---------------------------
Demonstrates Llama Stack telemetry: logging, streaming, and querying spans for observability and debugging.
"""

# Telemetry makes Llama Stack applications observable. Whether we're debugging one bad response or evaluating system performance at scale, having structured, queryable logs gives us the visibility we need to build reliable, responsive AI systems.

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction
from llama_stack_client import AgentEventLogger  # For streaming/logging agent events
from rich.pretty import pprint  # For pretty-printing telemetry output

# Initialize the client
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# Create an agent with shields and WolframAlpha tool
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="You are a calculator assistant that uses WolframAlpha to solve problems.",
    tools=["builtin::wolfram_alpha"],
    input_shields=["llama_guard_3"],
    output_shields=["llama_guard_3"]
)

session_id = agent.create_session("telemetry-demo")

# Streaming response and logging events
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "What is the square root of 169?"}],
    stream=True
)
for log in AgentEventLogger().log(response):
    log.print()

# For telemetry data, use non-streaming mode to ensure logs are recorded
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "What is the square root of 169?"}],
    stream=False
)

# Query telemetry spans for the session
spans = client.telemetry.query_spans(
    attribute_filters=[{"key": "session_id", "op": "eq", "value": session_id}],
    attributes_to_return=["input", "output"],
)
pprint(spans)

print("Printing the agent traces:")
for span in spans:
    pprint(span.attributes)