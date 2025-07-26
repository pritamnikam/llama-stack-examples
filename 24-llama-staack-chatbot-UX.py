"""
24-llama-staack-chatbot-UX.py
------------------------------
Full-featured Gradio UI chatbot demo for Llama Stack. Uses shields, tools, and streaming,
with a modern chat interface and robust error handling. Shows how to build a production-ready AI assistant UI.
"""

import gradio as gr
from gradio import ChatMessage
import os
from llama_stack_client import LlamaStackClient, Agent
import uuid
from datetime import datetime

# --- 1. SETUP AND INITIALIZATION ---
def get_current_date_formatted():
    return datetime.now().strftime('%d %B %Y')

# Initialize the LlamaStack client
try:
    client = LlamaStackClient(
        base_url="https://llama-stack.together.ai",
        provider_data={
            "together_api_key": os.environ['TOGETHER_API_KEY'],
            "tavily_search_api_key": os.environ['TAVILY_SEARCH_API_KEY'],
            "wolfram_alpha_api_key": os.environ['WOLFRAM_ALPHA_API_KEY'],
        }
    )
except Exception as e:
    raise ConnectionError(f"Failed to initialize LlamaStackClient. Please check your API keys. Error: {e}")

# Register the Llama Guard shield
shield_id = "llama_guard_3"
client.shields.register(
    shield_id=shield_id,
    provider_shield_id="meta-llama/Llama-Guard-3-8B"
)

# Define agent instructions
instructions = f"""
You are a helpful, intelligent AI assistant.
You have access to the following tools:

- Web Search — Use this to retrieve current events, niche topics, or up-to-date and real-time information from the web.
- Wolfram Alpha — Use this for math, science, data analysis, and precise computations. Always use Wolfram for mathematical questions.  

Guidelines:
- Your knowledge cut off is January 2023 and the current date is {get_current_date_formatted()}.
- Always use Web Search for any new information.
- Be accurate, clear, and concise.
- Use tools confidently and appropriately—never guess.
- If you’re unsure and tools don’t help, say so transparently.

Your goal is to provide high-quality answers that are well-reasoned, trustworthy, and useful.
"""

# Create the agent instance
agent = Agent(
    client=client,
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    instructions=instructions,
    tools=["builtin::wolfram_alpha", "builtin::websearch"],
    input_shields=[shield_id],
    output_shields=[shield_id]
)

print("✅ Agent and Client initialized successfully.")

# --- 2. GRADIO CHAT LOGIC ---

def add_user_message(user_input, history):
    """Adds the user's message to the chat history using ChatMessage."""
    if not user_input.strip():
        return gr.update(value=""), history
    
    # Append a ChatMessage for the user
    history.append(ChatMessage(role="user", content=user_input))
    
    return gr.update(value="", interactive=False), history

def stream_response(history, session_id):
    """
    Streams the response, updating the last ChatMessage's content and metadata.
    """
    if not session_id:
        session_id = agent.create_session(f"gradio-chat-{uuid.uuid4()}")
        print(f"✨ New session created: {session_id}")

    user_message = history[-1]["content"]
    
    response_stream = agent.create_turn(
        session_id=session_id,
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )

    # State to track if we are currently inside an inference block
    in_inference_block = False
    
    for chunk in response_stream:
        try:
            if not hasattr(chunk, "event") or not hasattr(chunk.event, "payload"):
                continue

            payload = chunk.event.payload
            event_type = payload.event_type
            step_type = getattr(payload, 'step_type', None)

            # --- Event 1: A Tool Execution step has completed ---
            if step_type == "tool_execution" and event_type == "step_complete":
                in_inference_block = False
                details = getattr(payload, 'step_details', None)
                if details:
                    for t in getattr(details, 'tool_calls', []):
                        history.append(ChatMessage(
                            role="assistant",
                            content=f"Tool `{t.tool_name}` was used.",
                            metadata={"title": f"⚙️ Used Tool: `{t.tool_name}`"}
                        ))
                        yield history, session_id

            # --- Event 2: A Shield Call step has completed ---
            elif step_type == "shield_call" and event_type == "step_complete":
                in_inference_block = False
                details = getattr(payload, 'step_details', None)
                if details:
                    title = "🛡️ Safety Check: Passed"
                    content = "Message passed the safety check."
                    if details.violation:
                        title = f"🚨 Safety Violation - Please clear chat"
                        content = details.violation.user_message
                        history.append(ChatMessage(
                            role="assistant",
                            content=content,
                            metadata={"title": title}
                        ))
                    yield history, session_id

            # --- Event 3: An Inference step is in progress (streaming text) ---
            elif step_type == "inference" and event_type == "step_progress":
                delta = getattr(payload, 'delta', None)
                if delta and delta.type == "text":
                    # If this is the first text chunk, create a new message bubble
                    if not in_inference_block:
                        in_inference_block = True
                        history.append(ChatMessage(role="assistant", content=""))
                    # Append the streamed text to the last message
                    history[-1].content += delta.text
                    yield history, session_id

        except Exception as e:
            print(f"Error processing stream chunk: {e}\nChunk: {chunk}")
            continue

    yield history, session_id


def clear_chat():
    """Clears the chat history and resets the session."""
    return [], None

# --- 3. GRADIO UI DEFINITION ---

with gr.Blocks(theme=gr.themes.Soft(), title="LlamaStack Agent") as demo:
    session_id_state = gr.State(None)
    
    gr.Markdown(
        """
        # 🤖 LlamaStack Chatbot Agent
        This chatbot uses **Llama-3.3-70B** with **Wolfram Alpha** & **Tavily Search**.
        Tool usage is displayed in the message metadata.
        """
    )
    
    chatbot = gr.Chatbot(
        label="Conversation",
        type="messages",
        height=300,
    )
    
    with gr.Row():
        user_input_textbox = gr.Textbox(placeholder="Type your message here...", scale=4, container=False)
        submit_btn = gr.Button("Send", variant="primary", scale=1)

    clear_btn = gr.Button("🗑️ Clear Chat", variant="stop")

    # --- 4. Event Handlers ---
    
    submit_event = user_input_textbox.submit(
        fn=add_user_message,
        inputs=[user_input_textbox, chatbot],
        outputs=[user_input_textbox, chatbot]
    ).then(
        fn=stream_response,
        inputs=[chatbot, session_id_state],
        outputs=[chatbot, session_id_state]
    ).then(
        fn=lambda: gr.update(interactive=True),
        outputs=[user_input_textbox]
    )
    
    submit_btn.click(
        fn=add_user_message,
        inputs=[user_input_textbox, chatbot],
        outputs=[user_input_textbox, chatbot]
    ).then(
        fn=stream_response,
        inputs=[chatbot, session_id_state],
        outputs=[chatbot, session_id_state]
    ).then(
        fn=lambda: gr.update(interactive=True),
        outputs=[user_input_textbox]
    )

    clear_btn.click(fn=clear_chat, outputs=[chatbot, session_id_state], queue=False)

# --- 5. LAUNCH THE APP ---

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", debug=True)