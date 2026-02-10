import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from aletheia_orchestrator.graph import app

load_dotenv()


def run_orchestrator():
    """
    Initializes and executes the Aletheia Orchestration graph.
    """
    # 1. Verification: Ensure the environment is ready
    if not os.getenv("GITHUB_TOKEN"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return

    # 2. Define the initial state (The user's entry point)
    # We explicitly define the starting state to ensure predictability.
    inputs = {
        "messages": [HumanMessage(content="Explain KL-Divergence")],
        "is_factually_correct": False,
        "iterations": 0,
    }

    # 3. Execution
    print("--- Aletheia Orchestrator: Initializing Loop ---")
    try:
        result = app.invoke(inputs)

        # 4. Extract and present the final refined message
        final_response = result["messages"][-1].content
        print("\n--- Final Output ---")
        print(final_response)
        print(f"\n[Metadata]: Iterations performed: {result['iterations']}")

    except Exception as e:
        print(f"An error occurred during graph execution: {e}")


if __name__ == "__main__":
    run_orchestrator()
