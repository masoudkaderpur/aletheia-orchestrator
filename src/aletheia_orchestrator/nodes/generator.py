import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

from aletheia_orchestrator.state import AgentState

"""
PURPOSE: The 'Synthesis Node' (G).
This component is responsible for processing the current state history
and generating the most accurate technical response possible.
"""

load_dotenv()

# MODEL CONFIGURATION:
# Temperature is set to 0 to minimize 'stochastic variance'.
# This ensures that for the same set of inputs, the model provides the
# most probable and factual completion rather than creative alternatives.
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
)


def call_model(state: AgentState):
    """
    GENERATION LOGIC:
    Acts as the primary worker node. It consumes the 'messages' history
    from the state and generates a refined response based on the
    original query and any subsequent Critic feedback.
    """

    # Context Awareness:
    # By passing state["messages"], the model sees the entire conversation
    # thread, allowing it to 'learn' from previous Critic rejections.
    response = model.invoke(state["messages"])

    # STATE UPDATE:
    # 1. messages: The response is wrapped in an AIMessage and appended to history.
    # 2. iterations: Returning 1 triggers the 'add' reducer in state.py,
    #    automatically incrementing the global counter.
    return {"messages": [AIMessage(content=response.content)], "iterations": 1}
