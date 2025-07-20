"""
11-llama-stack-tool-custom-tool.py
----------------------------------
Demonstrates how to register and use a custom Python function as a tool with a Llama Stack Agent.
"""

from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction
from llama_stack_client import AgentEventLogger  # For streaming/logging agent events
from termcolor import cprint  # For colored terminal output

# Initialize the client with Together AI endpoint and API key
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

def convert_temperature(value: float, unit: str) -> float:
    """
    Converts a temperature value between Celsius and Fahrenheit.

    :param value: The temperature to convert
    :param unit: Either 'C' to convert from Celsius to Fahrenheit, or 'F' to convert from Fahrenheit to Celsius.
    :return: Converted temperature
    """
    if unit.upper() == 'C':
        return (value * 9/5) + 32
    elif unit.upper() == 'F':
        return (value - 32) * 5/9
    else:
        raise ValueError("Invalid unit. Must be 'C' or 'F'.")

# Initialize the agent with the custom tool
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="""
    You are a weather assistant. Use the temperature conversion tool to convert values.
    Always call the tool instead of calculating manually.
    """,
    tools=[convert_temperature]
)

# Create a session for the agent
session_id = agent.create_session("temp-session")

# Demonstration: Ask the agent to convert temperature
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "Convert 100 degrees Celsius to Fahrenheit"}],
    stream=True
)

# Stream and print the agent's response
for log in AgentEventLogger().log(response):
    log.print()

# Enter interactive loop for more conversions
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        cprint("Ending conversation. Goodbye!", "blue")
        break
    response = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": user_input}],
        stream=True
    )
    for log in AgentEventLogger().log(response):
        log.print()