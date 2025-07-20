"""
06-llama-stack-streaming-completion.py
-------------------------------------
Demonstrates streaming chat completion using the Llama Stack client and event logger.
"""

# Specify the model to use
model_id = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

# Define sampling parameters for generation
sampling = {
    "strategy": {
        "type": "top_p",
        "temperature": 0.7,
        "top_p": 0.9
    },
    "max_tokens": 100,
    "repetition_penalty": 1.1,
    "stop": ["\nUser:", "\nSystem:"]
}

# Define the chat messages
messages = [
    {"role": "system", "content": "You are a friendly AI assistant."},
    {"role": "user", "content": "Tell me a joke about smartphones."},
]

# Make a streaming chat completion request
response = client.inference.chat_completion(
    model_id=model_id,
    messages=messages,
    sampling_params=sampling,
    stream=True
)

from llama_stack_client import InferenceEventLogger

# Stream and print each event as it arrives
for log in InferenceEventLogger().log(response):
    log.print()