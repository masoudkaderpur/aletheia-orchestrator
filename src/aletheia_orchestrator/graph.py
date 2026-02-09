from langgraph.graph import END, StateGraph

from aletheia_orchestrator.nodes.generator import call_model
from aletheia_orchestrator.state import AgentState


def create_orchestrator():
    """
    Constructs the LangGraph state machine for the Aletheia Orchestrator.

    This graph defines the cyclical flow between generation and factual
    validation, maintaining the state via the AgentState schema.
    """

    # 1. Initialize the StateGraph with the schema
    # The schema ensures all nodes have a shared, predictable data contract.
    builder = StateGraph(AgentState)

    # 2. Register Nodes
    # We map logical names to the actual Python functions (the "Workers").
    builder.add_node("generator", call_model)

    # 3. Define the Orchestration Flow (Edges)
    builder.set_entry_point("generator")

    # Current simplistic flow: Generator -> Exit
    # Tomorrow, this will evolve into: Generator -> Critic -> Router
    builder.add_edge("generator", END)

    # 4. Compile the Workflow
    # This transforms the definition into an executable 'CompiledGraph' object.
    return builder.compile()


# Instantiate the application
app = create_orchestrator()
