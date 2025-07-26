"""
23-llama-stack-building-chatbot.py
----------------------------------
Demonstrates building a conversational chatbot agent with Llama Stack, safety shields,
tool use (Wolfram Alpha, web search), and a streaming interactive loop.
"""

from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger
from termcolor import cprint
import os

# Step 1: Setting the stage and connecting to our LLM

client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY'],
        "tavily_search_api_key": os.environ['TAVILY_SEARCH_API_KEY'],
        "wolfram_alpha_api_key": os.environ['WOLFRAM_ALPHA_API_KEY'],
    }
)

# Step 2: Registering a safety shield

shield_id = "llama_guard_3"

client.shields.register(
    shield_id=shield_id,
    provider_shield_id="meta-llama/Llama-Guard-3-8B"
)

# Step 3: Defining the agent and its tools

instructions = """
You are a helpful, intelligent AI assistant.
You have access to the following tools:

- Wolfram Alpha — Use this for math, science, data analysis, and precise computations. Always use Wolfram for mathematical questions.  
- Tavily Web Search — Use this to retrieve current events, niche topics, or up-to-date and real-time information from the web.

Guidelines:
- Your knowledge cut off is January 2023, use web search for any new information.
- Be accurate, clear, and concise.
- Use tools confidently and appropriately—never guess.
- If you’re unsure and tools don’t help, say so transparently.

Your goal is to provide high-quality answers that are well-reasoned, trustworthy, and useful.
"""

agent = Agent(
    client=client,
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    instructions=instructions,
    tools=["builtin::wolfram_alpha", "builtin::websearch"],
    input_shields=["llama_guard_3"],
    output_shields=["llama_guard_3"]
)

# Step 4: Creating the main chat loop

session_id = agent.create_session("chat-session")

while True:
    user_input = input("You: ")
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