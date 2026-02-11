import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from aletheia_orchestrator.graph import app

"""
PURPOSE: Orchestration entry point.
This script handles environment validation, user interaction,
and the invocation of the LangGraph-based state machine.
"""

load_dotenv()


def run_orchestrator():
    """
    Initializes and executes the Aletheia Orchestration graph.
    """

    # 1. Verification: Environment check.
    # Essential for preventing runtime failures in cloud or local deployments.
    if not os.getenv("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN not found in environment variables.")
        return

    # 2. Reading Input: Real-time query capture.
    # Transforms the static research script into a dynamic tool.
    print("\n--- Aletheia: Research Interface ---\n")
    user_query = input("What topic should I research for you? \n")

    # Validation logic to prevent empty state initialization.
    if not user_query.strip():
        print("No topic provided. \nExiting.")
        return

    # 3. State Initialization:
    # Defining the starting 'AgentState'.
    # The 'user_query' is wrapped in a HumanMessage to preserve
    # semantic role context within the LLM conversation history.
    inputs = {
        "messages": [HumanMessage(content=user_query)],
        "is_factually_correct": False,
        "iterations": 0,
    }

    # 4. Execution Loop:
    # Invokes the LangGraph compiled 'app'.
    # This triggers the Generator-Critic loop as defined in the graph.
    print(f"--- Aletheia Orchestrator: Analyzing '{user_query}' ---")
    try:
        result = app.invoke(inputs)

        # 5. Result Extraction:
        # Accesses the final message in the accumulated history.
        final_response = result["messages"][-1].content
        print("\n--- Final Output ---")
        print(final_response)

        # Performance Tracking:
        # Displays the iteration count to verify convergence efficiency.
        print(f"\n[Metadata]: Iterations performed: {result['iterations']}")

    except Exception as e:
        # Error handling for network timeouts or API rate limits.
        print(f"An error occurred during graph execution: {e}")


if __name__ == "__main__":
    run_orchestrator()
