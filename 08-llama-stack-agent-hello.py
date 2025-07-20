"""
08-llama-stack-agent-hello.py
----------------------------
Demonstrates how to use a Llama Stack Agent with web search capabilities for up-to-date answers.
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction
from llama_stack_client import AgentEventLogger  # For streaming/logging agent events
from termcolor import cprint  # For colored terminal output

# Initialize the Llama Stack client with API keys for Together and Tavily web search
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY'],
        "tavily_search_api_key": os.environ['TAVILY_SEARCH_API_KEY']
    }
)

# Create an agent with web search tool enabled and custom instructions
guidelines = """
    You are a helpful AI assistant with access to web search. 
    This tool allows you to search the web for up-to-date information. 
    Use it whenever you need to answer a question that requires current or specific details.

    ### Guidelines for Using web_search
    - **Use for Current Events**: If the question is about current events, recent news, or topics that might have changed since the last update, always use the web search.
    - **Verify Information**: If you are unsure about the accuracy of the information, especially for factual or statistical queries, use the web search to verify.
"""

agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions=guidelines,
    tools=["builtin::websearch"],
)

# Create a new agent session for chat
session_id = agent.create_session("chat-search-session")

while True:
    # Prompt user for input
    user_input = input("You: ")
    # (Agent interaction and event streaming logic would go here)
    if user_input.lower() == "exit":
        cprint("Ending conversation. Goodbye!", "blue")
        break
    
    response = agent.create_turn(
        session_id=session_id,
        messages=[
            {"role": "user", "content": user_input}
        ],
        stream=True
    )
    
    for log in AgentEventLogger().log(response):
        log.print()