"""
18-llama-stack-llm-as-a-judge.py
--------------------------------
Demonstrates using an LLM as a judge for factual evaluation of agent responses.
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

# Model and prompt for LLM-as-a-judge evaluation
judge_model_id = "meta-llama/Llama-3.3-70B-Instruct"
judge_prompt =  """
    Given a QUESTION and GENERATED_RESPONSE and EXPECTED_RESPONSE.
    
    Compare the factual content of the GENERATED_RESPONSE with the EXPECTED_RESPONSE. Ignore any differences in style, grammar, or punctuation.
    The GENERATED_RESPONSE may either be a subset or superset of the EXPECTED_RESPONSE, or it may conflict with it. Determine which case applies. Answer the question by selecting one of the following options:
    (A) The GENERATED_RESPONSE is a subset of the EXPECTED_RESPONSE and is fully consistent with it.
    (B) The GENERATED_RESPONSE is a superset of the EXPECTED_RESPONSE and is fully consistent with it.
    (C) The GENERATED_RESPONSE contains all the same details as the EXPECTED_RESPONSE.
    (D) There is a disagreement between the GENERATED_RESPONSE and the EXPECTED_RESPONSE.
    (E) The answers differ, but these differences don't matter from the perspective of factuality.
    
    Give your answer in the format "Answer: One of ABCDE, Explanation: ".
    
    Your actual task:
    
    QUESTION: {input_query}
    GENERATED_RESPONSE: {generated_answer}
    EXPECTED_RESPONSE: {expected_answer}
    """

scoring_params = {
    "llm-as-judge::base": {
        "judge_model": judge_model_id,
        "prompt_template": judge_prompt,
        "type": "llm_as_judge",
    },
    "basic::subset_of": None,
}

for row in eval_rows:
    response = agent.create_turn(
        messages=[
            {
                "role": "user",
                "content": row["input_query"],
            }
        ],
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