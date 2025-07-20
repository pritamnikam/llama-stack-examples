"""
04-llama-stack-full-app.py
-------------------------
Full workflow for starting the Llama Stack server, ensuring readiness, and running a sample chat completion request.
"""

import os  # For environment variable access
import subprocess  # For running the server process
import time  # For waiting/retries
import requests  # For health checks
from llama_stack_client import LlamaStackClient  # Llama Stack client
from requests.exceptions import ConnectionError  # For handling connection errors

def run_llama_stack_server_background():
    """
    Launch the Llama Stack server in the background, logging output to a file.
    Returns the subprocess.Popen object for the running server.
    """
    log_file = open("llama_stack_server.log", "w")
    process = subprocess.Popen(
        "uv run --with llama-stack llama stack run together --image-type venv",
        shell=True,
        stdout=log_file,
        stderr=log_file,
        text=True
    )
    print(f"Starting Llama Stack server with PID: {process.pid}")
    return process

def wait_for_server_to_start():
    """
    Poll the server health endpoint until it responds or times out.
    Returns True if the server is ready, False otherwise.
    """
    url = "http://0.0.0.0:8321/v1/health"
    max_retries = 30
    retry_interval = 1
    print("Waiting for server to start", end="")
    for _ in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("\nServer is ready!")
                return True
        except ConnectionError:
            print(".", end="", flush=True)
            time.sleep(retry_interval)
    print(f"\nServer failed to start after {max_retries * retry_interval} seconds")
    return False

def kill_llama_stack_server():
    """
    Kill any running Llama Stack server processes (Linux/Mac only).
    """
    os.system("ps aux | grep -v grep | grep llama_stack.distribution.server.server | awk '{print $2}' | xargs kill -9")

# --- Main workflow ---
# Start the server
server_process = run_llama_stack_server_background()
# Wait for the server to be ready
assert wait_for_server_to_start()

# Initialize the Llama Stack client
client = LlamaStackClient(
    base_url="http://0.0.0.0:8321", 
    provider_data={
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# List and print available models
models = client.models.list()
print("Available Models:")
for model in models:
    print(f"- {model.identifier} ({model.model_type})")

print("\nSending a chat request:")
model_id = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

# Send a chat completion request
response = client.inference.chat_completion(
    model_id=model_id,
    messages=[
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "What is the chemical symbol for water?"},
    ],
)

# Display the assistant's response
print(response.completion_message.content)