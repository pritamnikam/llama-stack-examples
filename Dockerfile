# Dockerfile for Llama Stack with Ollama
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl gnupg2 procps && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Create and activate virtual environment, Install Python dependencies and system libraries for RAG support
RUN apt-get update && \
    apt-get install -y --no-install-recommends libopenblas-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    uv venv .venv && \
    uv pip install -r requirements.txt && \
    uv pip install llama-stack-client faiss-cpu

# Pull Llama 3.2-1B model
RUN bash -c 'ollama serve & \
  for i in {1..30}; do \
    sleep 2; \
    if curl -s http://localhost:11434 > /dev/null; then \
      break; \
    fi; \
    echo "Waiting for Ollama to be ready... ($i)"; \
  done; \
  ollama pull llama3.2:1b; \
  pkill ollama'

# Set environment variable for inference model
ENV INFERENCE_MODEL=llama3.2:1b

# Document environment variables
#   TOGETHER_API_KEY: Required for Llama Stack API access
#   TAVILY_SEARCH_API_KEY: Optional, for web search tool
#   WOLFRAM_ALPHA_API_KEY: Optional, for WolframAlpha tool

# Copy rest of the code (if any)
COPY . .

# Expose port
EXPOSE 8321

# Expose Gradio default port for chatbot UX
EXPOSE 7860

# Production entrypoint: run script specified by SCRIPT (default: 01-llama-stack-hello.py)
# For Gradio UI, set SCRIPT=24-llama-staack-chatbot-UX.py
ENV SCRIPT=01-llama-stack-hello.py
CMD bash -c "ollama serve & sleep 5 && uv run --with llama-stack llama stack build --template ollama --image-type venv --run && sh -c 'python $SCRIPT'"
