"""
07-llama-stack-multi-turn-conversation-and-context.py
----------------------------------------------------
Implements a multi-turn conversation loop with context retention using the Llama Stack client.
"""

from llama_stack_client import InferenceEventLogger  # For logging streaming events
from termcolor import cprint  # For colored terminal output

# Specify the model to use
model_id = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

# Initialize conversation with a system prompt
messages = [
    {"role": "system", "content": "You are a friendly AI assistant."}
]

while True:
    # Get user input
    user_input = input("You: ")
    if user_input.lower() == "exit":
        cprint("Ending conversation. Goodbye!", "blue")
        break
    # Add user message to conversation history
    messages.append({"role": "user", "content": user_input})

    # Make a streaming chat completion request
    response = client.inference.chat_completion(
        model_id=model_id,
        messages=messages,
        stream=True
    )

    buffer = ""  # Collect assistant's response

    # Stream and print each event as it arrives
    for log in InferenceEventLogger().log(response):
        buffer += log.content
        log.print()

    # Add assistant's response to conversation history
    messages.append({
        "role": "assistant",
        "content": buffer,
        "stop_reason": "end_of_turn"
    })