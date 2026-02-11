import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from aletheia_orchestrator.state import AgentState

"""
PURPOSE: The 'Synthesis Node' (G).
Responsible for generating and refining technical content. It operates
in a reactive manner, adapting its output based on Critic feedback.
"""

load_dotenv()

# MODEL CONFIGURATION:
# temperature=0 ensures deterministic, high-fidelity technical output.
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
)


def call_model(state: AgentState):
    """
    GENERATION LOGIC:
    Processes message history and applies iterative corrections.
    """

    # 1. Context Retrieval:
    # Extract existing history and any qualitative feedback from the Critic.
    messages = state["messages"]
    feedback = state.get("critic_feedback", "")

    # 2. Dynamic Prompt Engineering:
    # If feedback exists, a SystemMessage is appended to the message list.
    # This acts as a high-priority instruction, forcing the LLM to address
    # specific weaknesses identified in the previous iteration.
    if feedback:
        feedback_instruction = SystemMessage(
            content=(
                f"Feedback to your last response: {feedback}\n"
                "Please correct your response based on this feedback!"
            )
        )
        input_messages = messages + [feedback_instruction]
    else:
        input_messages = messages

    # 3. Inference:
    # The model processes the full context (History + Feedback).
    response = model.invoke(input_messages).content

    # STATE UPDATE:
    # 1. messages: New response is added to the history.
    # 2. iterations: Counter is incremented via the State's 'add' reducer.
    return {"messages": [AIMessage(content=response)], "iterations": 1}
