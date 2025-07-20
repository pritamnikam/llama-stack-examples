"""
10-llama-stack-tool-code-interpreter.py
--------------------------------------
Demonstrates using the WolframAlpha tool with a Llama Stack Agent for factual and calculation-based queries.
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction
from llama_stack_client import AgentEventLogger  # For streaming/logging agent events
from termcolor import cprint  # For colored terminal output

# Initialize the client with WolframAlpha API key (replace with your actual key)
client = LlamaStackClient(
    base_url="http://localhost:8321",
    provider_data={
        "wolfram_alpha_api_key": "your_wolfram_key_here"
    }
)

# Create an agent with the WolframAlpha tool enabled
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="""
    You are a factual assistant. Use the WolframAlpha tool to answer questions involving data,
    facts, or calculations. Never guess—always call the tool when in doubt.
    """,
    tools=["builtin::wolfram_alpha"]
)

# Create a session for the agent
session_id = agent.create_session("fact-check-session")

# Demonstration: Ask a factual question
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "What is the square root of 625?"}],
    stream=True
)

# Stream and print the agent's response
for log in AgentEventLogger().log(response):
    log.print()

# Enter interactive loop for more questions
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        cprint("Ending conversation. Goodbye!", "blue")
        break
    # (Additional turn logic would go here)
    response = agent.create_turn(
        session_id=session_id,
        messages=[
            {"role": "user", "content": user_input}
        ],
        stream=True
    )
    
    for log in AgentEventLogger().log(response):
        log.print()