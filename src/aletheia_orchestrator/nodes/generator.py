import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

from aletheia_orchestrator.state import AgentState

load_dotenv()

# Initialize the model with zero temperature for deterministic, factual outputs
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
)


def call_model(state: AgentState):
    """
    Passes the current state messages to the LLM and records the response.
    """
    # Invoke the model with the full message history from the state
    response = model.invoke(state["messages"])

    # Return the new AI message and increment the iteration counter
    return {"messages": [AIMessage(content=response.content)], "iterations": 1}
