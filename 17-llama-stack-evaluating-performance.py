"""
17-llama-stack-evaluating-performance.py
---------------------------------------
Lists available scoring functions and demonstrates a simple evaluation loop for agent responses.
"""

import os  # For environment variable access
from llama_stack_client import LlamaStackClient  # Llama Stack client
from llama_stack_client import Agent  # Agent abstraction

# Initialize the client
client = LlamaStackClient(
    base_url="https://llama-stack.together.ai", 
    provider_data = {
        "together_api_key": os.environ['TOGETHER_API_KEY']
    }
)

# List available scoring functions
scoring_functions = client.scoring_functions.list()
print("Available scoring functions:")
for function in scoring_functions:
    print(f"- {function.identifier} - {function.description}")

# Create an agent for evaluation
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
    instructions="You are a helpful AI assistant",
)

session_id = agent.create_session("evaluation-demo")

eval_rows = [
    {"input_query": "Which one letter doesn’t appear in any U.S. state name", "generated_answer": "", "expected_answer": "Q"},
    {"input_query": "How many Rs are there in 'strawberry'?", "generated_answer": "", "expected_answer": "3 or three"},
    {"input_query": "Who founded Ikea?", "generated_answer": "", "expected_answer": "Ingvar Kamprad"}
]

scoring_params = {
    "basic::subset_of": None
}

# Evaluate agent responses for each row
for row in eval_rows:
    response = agent.create_turn(
        messages=[{"role": "user", "content": row["input_query"]}],
        session_id=session_id,
        stream=False
    )
    generated_answer = response.output_message.content
    print(generated_answer)
    row["generated_answer"] = generated_answer
    
scoring_response = client.scoring.score(
    input_rows=eval_rows, 
    scoring_functions=scoring_params
)
pprint(scoring_response)