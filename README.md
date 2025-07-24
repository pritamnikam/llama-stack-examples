# Llama Stack Project - Quickstart

[![CI](https://github.com/pritamnikam/llama-stack-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/pritamnikam/llama-stack-examples/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/pritamnikam/llama-stack-examples/branch/main/graph/badge.svg)](https://codecov.io/gh/pritamnikam/llama-stack-examples)
[![mypy](https://img.shields.io/badge/type_check-mypy-blue.svg)](https://mypy.readthedocs.io/en/stable/)

This project demonstrates various ways to use the Llama Stack for LLM inference, both locally and via Together AI, with examples for streaming, multi-turn conversation, and more. You can run everything locally or use Docker for a fully containerized setup.

---

## Prerequisites
- [uv](https://github.com/astral-sh/uv) (for Python environment management)
- [Ollama](https://ollama.com/) (for local LLM inference)
- Docker (optional, for containerized setup)

---

## Local Setup

### 1. Install `uv`
Install `uv` globally (see [uv installation guide](https://github.com/astral-sh/uv#installation)):
```sh
pip install uv
```

### 2. Initialize Project Environment
```sh
uv venv .venv
uv pip install -r requirements.txt
```

### 3. Install Llama Stack Python SDK
```sh
uv pip install llama-stack
```

### 4. Install and Run Ollama
Install Ollama (see [Ollama install guide](https://ollama.com/download)):
```sh
# Windows (PowerShell)
iwr https://ollama.com/install.ps1 -UseBasicParsing | iex

# macOS
brew install ollama
```

---

## Docker Setup
See the provided `Dockerfile` for a complete containerized environment, including Ollama and all dependencies.

---

## File Commentary

| File Name                                         | Purpose                                                                                         |
|---------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `01-llama-stack-hello.py`                         | Basic example: lists models and sends a simple chat completion request.                         |
| `02-llama-stack-together-ai.py`                   | Connects to the hosted Llama Stack server via Together AI and makes a chat request.             |
| `03-llama-stack-library-client.py`                | Uses Llama Stack as a library client, including explicit initialization.                        |
| `04-llama-stack-full-app.py`                      | Full workflow: starts server, waits for readiness, and runs a sample chat completion.           |
| `05-llama-stack-constructing-sending-inference-request.py` | Shows how to construct and send a chat completion request.                              |
| `06-llama-stack-streaming-completion.py`          | Demonstrates streaming chat completion with event logging.                                      |
| `07-llama-stack-multi-turn-conversation-and-context.py`    | Implements a multi-turn conversation loop with context retention.                      |
| `08-llama-stack-agent-hello.py`                            | Demonstrates an agent with web search capability using Llama Stack and Tavily.         |
| `09-llama-stack-list-tools.py`                             | Lists all available tools registered with the Llama Stack client.                      |
| `10-llama-stack-tool-code-interpreter.py`                  | Uses the WolframAlpha tool with an agent for factual and calculation-based queries.    |
| `11-llama-stack-tool-custom-tool.py`                       | Shows how to register and use a custom Python function as a tool for the agent.        |
| `12-llama-stack-tool-rag.py`                               | Registers a vector DB and inserts documents for Retrieval-Augmented Generation (RAG).  |
| `13-llama-stack-rag-enabled-agent.py`                      | Agent with RAG integration for knowledge-augmented Q&A using a custom vector DB.       |
| `14-llama-stack-shield-list.py`                            | Lists all available shields (guardrail/safety models) in Llama Stack.                  |
| `15-llama-stack-shield-in-action.py`                       | Demonstrates registering and using shields for safe agent inference.                   |
| `16-llama-stack-telemetry.py`                              | Shows telemetry logging, streaming, and querying for observability and debugging.      |
| `17-llama-stack-evaluating-performance.py`                 | Lists scoring functions and demonstrates a basic agent evaluation loop.                |
| `18-llama-stack-llm-as-a-judge.py`                         | Uses an LLM as a judge for factual evaluation of agent responses.                      |
| `requirements.txt`                                | Lists all Python dependencies required for the scripts.                                         |
| `Dockerfile`                                      | Containerizes the project, installs Ollama and all Python dependencies.                         |
| `.gitignore`                                      | Standard Python .gitignore for venvs, logs, etc.                                                |
| `docker-compose.yml`                              | (If present) Compose file for multi-container orchestration.                                    |

---

## Commentary on Each File

All Python scripts are commented with docstrings and inline comments for clarity. See each script for detailed explanations of the workflow and API usage.

- **requirements.txt**: Includes llama-stack, llama-stack-client, termcolor, and requests.
- **Dockerfile**: Sets up a reproducible environment with Ollama and all dependencies.
- **.gitignore**: Ensures virtual environments, logs, and other unnecessary files are not tracked.

---

## Usage

- Review the commentary in each script for details on usage and workflow.
- Set the `TOGETHER_API_KEY` environment variable as required by the scripts.
- Run any script directly with your Python interpreter after activating the virtual environment.
- For multi-turn or streaming examples, follow the prompts in your terminal.

---

## Example Usage

### Run a Script

```sh
python 01-llama-stack-hello.py
```

### Run All Tests

```sh
pytest
```

### Use Docker

```sh
docker build -t llama-stack-examples .
docker run --env TOGETHER_API_KEY=your_key llama-stack-examples
```

## API Reference

| Module/Class           | Purpose                                              |
|-----------------------|------------------------------------------------------|
| LlamaStackClient      | Main entry for Llama Stack API usage                 |
| Agent                 | Abstraction for agent-based LLM workflows            |
| AgentEventLogger      | Handles streaming/logging of agent events            |
| RAGDocument           | Represents a document for RAG vector DB              |
| Shields               | Safety/guardrail integration                         |
| Telemetry             | Observability and tracing of Llama Stack operations  |

## Troubleshooting & FAQs

### Frequently Asked Questions

**Q: Why do I get a `KeyError` or missing API key error?**
A: Make sure you have set your `TOGETHER_API_KEY` (and any other required API keys) as environment variables before running scripts or Docker containers.

**Q: How do I run a different script in Docker?**
A: Use the `SCRIPT` environment variable, e.g.:
```sh
docker run --env TOGETHER_API_KEY=your_key --env SCRIPT=14-llama-stack-shield-list.py llama-stack-examples
```

**Q: Why do I see `ModuleNotFoundError` or missing dependency errors?**
A: Run `pip install -r requirements.txt` to ensure all dependencies are installed.

**Q: How do I check test coverage or type-checking results?**
A: Coverage and type-checking run automatically in CI (see badges above). Locally, run `coverage run -m pytest` and `mypy .`.

**Q: My CI/CD pipeline fails on Docker or permissions. What should I do?**
A: Ensure your GitHub account has access to GitHub Container Registry and your secrets are set correctly.

### Known Issues
- Some scripts require valid API keys and will fail with a `KeyError` or authentication error if not set.
- Output checks in tests are basic; for more robust validation, extend the test suite for specific answers.
- Docker image size may be large due to model and dependencies.
- Not all scripts are intended for unattended/automated runs (some require interactive input).



- Ensure you have set all required API keys as environment variables (e.g., `TOGETHER_API_KEY`).
- If a script fails with a missing dependency, run `pip install -r requirements.txt`.
- For Docker issues, make sure Docker is running and you have sufficient resources allocated.
- If you see permission errors with Docker or GitHub Container Registry, check your credentials and permissions.
- For CI failures, review the GitHub Actions logs for lint/type/coverage errors.

## Advanced Usage & Automation

### Running Tests

- Run all smoke tests with:
  ```sh
  pytest test_llama_stack_examples.py
  ```
- The test suite checks that all example scripts import and run without errors.

### Continuous Integration (CI)

- This project uses GitHub Actions for CI.
- On every push and pull request to `main`, tests are run automatically (see badge above).
- See `.github/workflows/ci.yml` for configuration details.

## License

MIT License (or specify your project's license here)

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

Start Ollama server:
```sh
ollama serve
```

Pull the Llama 3.2-1B model:
```sh
ollama pull llama3.2:1b
```

Set environment variable (Windows):
```powershell
$env:INFERENCE_MODEL = "llama3.2:1b"
```

Set environment variable (Linux/macOS):
```sh
export INFERENCE_MODEL=llama3.2:1b
```

### 5. Run Llama Stack Server
With Ollama running, start the Llama Stack server using the Ollama template:
```sh
uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

You should see logs confirming the server is running at http://0.0.0.0:8321

### 6. Test the Server

You can test the Llama Stack server using the `llama-stack-client` CLI. This tool allows you to send requests to your running server and get model responses directly from the terminal.

First, ensure `llama-stack-client` is installed (it is included in requirements.txt and the Docker image).

**Example command:**

```sh
llama-stack-client inference chat-completion --message "tell me a joke"
```

This command sends a prompt to the model and prints the model's response. If the server and Ollama are running, you should see a joke generated by the model.

You may also use the Python SDK or visit the API docs at `http://localhost:8321/docs` to interact with the server.

---

## Docker Setup

### 1. Build and Run with Docker Compose
```sh
docker-compose up --build
```

This will:
- Start Ollama service
- Pull the Llama 3.2-1B model
- Start the Llama Stack server

The server will be available at http://localhost:8321

---

## File Overview
- `Dockerfile`: Containerizes Llama Stack server with Ollama
- `docker-compose.yml`: Orchestrates Ollama and Llama Stack
- `requirements.txt`: Python dependencies (Llama Stack SDK)

---

## References
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/)
- [Llama Stack](https://github.com/llama-stack/llama-stack)
