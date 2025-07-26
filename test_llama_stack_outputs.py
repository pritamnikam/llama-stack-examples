"""
test_llama_stack_outputs.py
--------------------------
Functional tests: run selected scripts as subprocesses and check for expected output snippets.
"""
import subprocess
import sys
import os
import pytest

# List of scripts and expected output snippets for functional testing
SCRIPTS_OUTPUTS = [
    ("01-llama-stack-hello.py", "chemical symbol for water"),
    ("02-llama-stack-together-ai.py", "You are a friendly assistant."),
    ("09-llama-stack-list-tools.py", "Available tools"),
    ("14-llama-stack-shield-list.py", "Available shields"),
    ("15-llama-stack-shield-in-action.py", "mass of the earth"),
    ("16-llama-stack-telemetry.py", "square root of 169"),
    ("17-llama-stack-evaluating-performance.py", "Available scoring functions"),
    ("18-llama-stack-llm-as-a-judge.py", "Which one letter doesn"),
]

@pytest.mark.parametrize("script,expected", SCRIPTS_OUTPUTS)
def test_script_output_contains(script, expected):
    script_path = os.path.join(os.path.dirname(__file__), script)
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=45)
    except Exception as e:
        pytest.fail(f"{script} failed to run: {e}")
    assert expected in result.stdout, f"Output of {script} did not contain expected text: '{expected}'\nActual output:\n{result.stdout}"

# More specific output assertions for streaming and error cases
@pytest.mark.parametrize("script,expected", [
    ("19-llama-stack-two-agent-with-different-providers.py", "Hosted Agent:"),
    ("20-llama-stack-prompt-chaining-strategy.py", "Turn 1:"),
    ("21-llama-stack-routing-specialized-agents.py", "Employee:"),
    ("22-llama-stack-parallelization-strategy.py", "Translated Alert"),
    ("23-llama-stack-building-chatbot.py", "You:"),
])
def test_script_output_new_examples(script, expected):
    script_path = os.path.join(os.path.dirname(__file__), script)
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=60)
    assert expected in result.stdout, f"Output of {script} did not contain expected text: '{expected}'\nActual output:\n{result.stdout}"

# Gradio UX script: only check import/run, not output (UI)
import importlib
@pytest.mark.skipif(importlib.util.find_spec("gradio") is None, reason="gradio not installed")
def test_gradio_ux_script_runs():
    script = "24-llama-staack-chatbot-UX.py"
    script_path = os.path.join(os.path.dirname(__file__), script)
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=60)
    assert "Agent and Client initialized successfully" in result.stdout or result.returncode == 0

@pytest.mark.parametrize("script,expected", [
    ("06-llama-stack-streaming-completion.py", "Streaming chat completion"),
    ("07-llama-stack-multi-turn-conversation-and-context.py", "multi-turn conversation"),
    ("10-llama-stack-tool-code-interpreter.py", "WolframAlpha"),
    ("12-llama-stack-tool-rag.py", "Artificial General Intelligence"),
    ("13-llama-stack-rag-enabled-agent.py", "Retrieval-Augmented Generation"),
])
def test_script_stream_output(script, expected):
    script_path = os.path.join(os.path.dirname(__file__), script)
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=45)
    assert expected in result.stdout, f"Output of {script} did not contain expected streaming text: '{expected}'\nActual output:\n{result.stdout}"

# Edge case: test a script that should handle missing API key gracefully
@pytest.mark.parametrize("script", ["01-llama-stack-hello.py"])
def test_script_missing_api_key(monkeypatch, script):
    monkeypatch.delenv("TOGETHER_API_KEY", raising=False)
    script_path = os.path.join(os.path.dirname(__file__), script)
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=30)
    assert "API key" in result.stderr or "KeyError" in result.stderr or result.returncode != 0
