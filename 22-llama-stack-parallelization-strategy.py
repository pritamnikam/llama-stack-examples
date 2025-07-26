"""
22-llama-stack-parallelization-strategy.py
------------------------------------------
Demonstrates parallelization: multiple agents handle subtasks (e.g. translations) concurrently,
mirroring scalable, map-reduce style LLM workflows in production.
"""

# Pattern 3: Parallelization
#
# Parallelization is a workflow pattern where multiple agents handle independent subtasks simultaneously. 
# It’s useful when different parts of a job can be performed concurrently, reducing total runtime and 
# allowing specialized execution paths for each subtask.

# This pattern is especially useful when:
# - Each input chunk or subtask is independent.
# - You want to fan out work to multiple LLM instances.
# - Task volume is high, and latency matters.


# Example:
# Let’s say an organization needs to broadcast a critical alert across multiple regions. Each region requires:
# - A localized translation of the alert has been provided.
# - The tone has been adjusted to match cultural norms.
# - Country-specific contact details have been included.
# Rather than translating sequentially, we’ll spin up one agent per region and run them in parallel to reduce 
# time-to-delivery. We can start by defining our instructions for each agent in a dictionary. This is where you 
# can customize the agent. For example, we have asked the agent to add the region-specific email address with each 
# translation.

import os  # For environment variable access
from concurrent.futures import ThreadPoolExecutor

from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction

base_config = {
    "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
    "sampling_params": {
        "strategy": {"type": "top_p", "temperature": 0.8, "top_p": 0.9}
    }
}

# Initialize the client
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

base_alert = """
⚠️ Critical Notice:
Due to a system vulnerability identified in our authentication service, we are temporarily restricting new user sign-ups. 
We are actively working to patch the issue. Existing users remain unaffected.
"""

locale_configs = {
    "fr": "Translate the following system alert into French. Keep the tone formal and concise. Append this: 'Contactez le support: support-fr@example.com'",
    "de": "Translate the following system alert into German. Use a professional tone. Add: 'Support kontaktieren: support-de@example.com'",
    "es": "Translate into Spanish. Keep it direct, and add: 'Soporte técnico: soporte-es@example.com'",
    "jp": "Translate into Japanese using business etiquette. Append: 'サポート: support-jp@example.com'"
}

def build_agent(instructions):
    return Agent(
        client=client,
        model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
        instructions=instructions,
        sampling_params={
            "strategy": {"type": "top_p", "temperature": 0.5, "top_p": 0.85}
        }
    )
    
def localize_alert(language, prompt, message):
    print(f"Creating {language} agent")
    agent = build_agent(prompt)
    session_id = agent.create_session(session_name=f"alert_{language}")
    response = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": message}],
        stream=False
    )
    return language, response.output_message.content

# This setup offers simultaneous processing, which means immediate readiness across time zones. 
# It is also scalable, so we can add more regions by adding agents without changing the workflow logic.
# As each agent handles just one task, it also avoids overload or prompt bloat. We can expand this pattern 
# to analyze large document batches, generate multiple options or styles for the same content, or even run 
# AI-powered evaluations in parallel (e.g. scoring or grading). This approach mirrors map-reduce-style data 
# processing pipelines and is a strong candidate for serverless or autoscaled backends.

with ThreadPoolExecutor(max_workers=len(locale_configs)) as executor:
    futures = [
        executor.submit(localize_alert, lang, prompt, base_alert)
        for lang, prompt in locale_configs.items()
    ]
    results = [future.result() for future in futures]

for lang, output in results:
    print(f"\n🌐 [{lang.upper()}] Translated Alert:\n{output}")