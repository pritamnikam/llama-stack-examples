"""
05-llama-stack-constructing-sending-inference-request.py
-------------------------------------------------------
Demonstrates constructing and sending a simple chat completion request using the Llama Stack client.
"""

# Specify the model to use
model_id = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

# Send a chat completion request
response = client.inference.chat_completion(
    model_id=model_id,
    messages=[
        {"role": "system", "content": "You are a friendly AI assistant."},
        {"role": "user", "content": "Tell me a joke about computers."},
    ],
)

# Print the assistant's response
print(response.completion_message.content)