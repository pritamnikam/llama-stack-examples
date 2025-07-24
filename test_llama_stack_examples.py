"""
test_llama_stack_examples.py
---------------------------
Basic smoke tests for Llama Stack example scripts.
Ensures scripts run without import or top-level execution errors.
"""
import importlib
import pytest
import os

# List of example scripts to test (add more as needed)
SCRIPTS = [
    "01-llama-stack-hello",
    "02-llama-stack-together-ai",
    "03-llama-stack-library-client",
    "04-llama-stack-full-app",
    "05-llama-stack-constructing-sending-inference-request",
    "06-llama-stack-streaming-completion",
    "07-llama-stack-multi-turn-conversation-and-context",
    "08-llama-stack-agent-hello",
    "09-llama-stack-list-tools",
    "10-llama-stack-tool-code-interpreter",
    "11-llama-stack-tool-custom-tool",
    "12-llama-stack-tool-rag",
    "13-llama-stack-rag-enabled-agent",
    "14-llama-stack-shield-list",
    "15-llama-stack-shield-in-action",
    "16-llama-stack-telemetry",
    "17-llama-stack-evaluating-performance",
    "18-llama-stack-llm-as-a-judge",
]

def script_path(script):
    return os.path.join(os.path.dirname(__file__), f"{script}.py")

@pytest.mark.parametrize("script", SCRIPTS)
def test_script_import(script):
    """Test that each script can be imported without error."""
    spec = importlib.util.spec_from_file_location(script, script_path(script))
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"{script}.py failed to import: {e}")
