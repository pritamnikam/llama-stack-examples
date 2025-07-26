"""
21-llama-stack-routing-specialized-agents.py
--------------------------------------------
Shows routing pattern: a classifier agent routes user queries to specialized agents (policy, feedback, scheduling),
mimicking real-world triage and delegation in multi-agent LLM systems.
"""

# Pattern 2: Routing to specialized agents
#
# Routing is a dynamic workflow pattern where one agent acts as a router or classifier, 
# analyzing user intent and dispatching the query to the most appropriate downstream agent. 
# This mirrors how triage systems work in customer service or how requests are routed to 
# specialized microservices in distributed systems.
#
# This pattern is useful when:
# - You have multiple narrow-task agents (e.g., FAQ bots, experts)
# - You want to decouple classification logic from task execution.
# - You need a clean delegation interface for multi-intent inputs.
#
# This structure mirrors real-world systems in customer service, IT support, and internal automation.
# It also scales well. Adding a new intent means adding one agent and updating the routing logic schema,
# without disrupting the flow.

from pydantic import BaseModel
import json
import os  # For environment variable access
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

specialized_agents = {
    "policy": Agent(client, instructions="You are an HR policy assistant. Answer questions about vacation, benefits, leave, etc.", **base_config),
    "feedback": Agent(client, instructions="You collect anonymous employee feedback. Be neutral and encouraging.", **base_config),
    "scheduling": Agent(client, instructions="You help schedule internal meetings. Confirm times and required participants.", **base_config)
}

specialized_agents_session_ids = {
    "policy": specialized_agents["policy"].create_session("policy_agent"),
    "feedback": specialized_agents["feedback"].create_session("feedback_agent"),
    "scheduling": specialized_agents["scheduling"].create_session("scheduling_agent"),
}    

class RoutingDecision(BaseModel):
    intent: str  # one of: policy, feedback, scheduling
    reason: str

routing_agent = Agent(
    client,
    instructions="""
    You're an intent classifier for an HR assistant. Decide whether the employee's query relates to:
    - policy
    - feedback
    - scheduling

    Return your decision in this format:
    {
        "intent": "<policy | feedback | scheduling>",
        "reason": "<your reasoning here>"
    }
    """,
    response_format={"type": "json_schema", "json_schema": RoutingDecision.model_json_schema()},
    **base_config
)

routing_agent_session_id = routing_agent.create_session("routing_agent")

def handle_hr_query(user_input: str):
    routing_turn = routing_agent.create_turn(
        messages=[{"role": "user", "content": user_input}],
        session_id=routing_agent_session_id,
        stream=False
    )

    try:
        decision = json.loads(routing_turn.output_message.content)
        category = decision["intent"]
        reason = decision["reason"]

        print(f"[Routing → {category}] {reason}")

        agent = specialized_agents.get(category)
        if not agent:
            return f"No handler for category '{category}'"

        response = agent.create_turn(
            messages=[{"role": "user", "content": user_input}],
            session_id=specialized_agents_session_ids.get(category),
            stream=False
        )
        return response.output_message.content

    except Exception as e:
        return f"Routing error: {str(e)}"

queries = [
    "I need to know how many vacation days I have left this year.",
    "I'd like to give some feedback about team dynamics—can it stay anonymous?",
    "Can you book a 30-minute 1:1 with my manager this Friday afternoon?"
]

for q in queries:
    print("\n---")
    print("Employee:", q)
    print("Assistant:", handle_hr_query(q))