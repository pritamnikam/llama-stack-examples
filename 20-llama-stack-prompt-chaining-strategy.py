"""
20-llama-stack-prompt-chaining-strategy.py
------------------------------------------
Demonstrates prompt chaining: a workflow where multiple LLM calls are sequenced,
each building on the previous, to solve a multi-step problem (summarize, simplify, translate, etc).
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction

# Pattern 1: Prompt chaining
# Prompt chaining is the simplest and most reliable agent workflow. It sequences multiple LLM calls, with each step building directly on the previous one.
# This approach avoids complex orchestration and is especially effective when:
# - The overall task can be broken down into a sequence of simple subtasks
# - Each subtask has a clear and unambiguous goal
# - Deterministic flow is more important than flexibility

# Initialize the client
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

document = """
        The Llama Stack architecture provides a modular interface layer between application
        code and infrastructure components such as inference engines, vector databases, 
        safety filters, and telemetry systems. Its goal is to decouple logic from runtime, 
        enabling flexible deployment across local, cloud, and edge environments.
        """

agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="You are a helpful assistant capable of formatting report data."
)

session_id = agent.create_session("fact-check-prompt_chain_demo")

prompts = [
    f"Summarize the following paragraph in 2-3 sentences:\n{document}",
    "Now rewrite the summary in plain English, avoiding any jargon.",
    "Translate the result into Spanish. Use a natural tone.",
    "Rewrite the Spanish version to sound more casual and conversational."
]

for i, prompt in enumerate(prompts):
    response = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    print(f"Turn {i+1}:\n{response.output_message.content}\n")