from langgraph.graph import END, StateGraph

from aletheia_orchestrator.nodes.critic import criticize
from aletheia_orchestrator.nodes.generator import call_model
from aletheia_orchestrator.state import AgentState

"""
PURPOSE: The 'Logic Layer'.
This file defines the system's topology—mapping how data moves from
generation to validation and determining the conditions for termination.
"""


def router(state: AgentState):
    """
    DECISION LOGIC (The Gateway):
    Acts as the conditional switch for the graph. It evaluates the
    convergence signal (is_factually_correct) to decide whether to
    terminate the process or trigger a refinement cycle.
    """

    # ITERATION GUARDRAIL (Safety Termination):
    # Implements a hard stop after n-attempts to mitigate unbounded
    # execution costs and potential oscillating feedback loops.
    # This acts as the 'Maximum Entropy' exit strategy.
    if state["iterations"] >= 3:
        print("\n[ROUTER] Info: Maximum iterations reached. Terminating safety loop.")
        return "exit"

    # CONVERGENCE SIGNAL:
    # Evaluates the boolean satisfaction flag from the Critic node.
    # Logic follows the 'Aletheia' principle: termination only upon
    # verification of factual integrity.
    if state["is_factually_correct"]:
        print("\n[ROUTER] Info: Truth condition met (Aletheia).")
        return "exit"

    # RECURSIVE REFINEMENT:
    # Default state for non-convergent paths. Re-triggers the Generator
    # to perform a delta-update based on the accumulated context.
    return "retry"


def create_orchestrator():
    """
    GRAPH CONCRETE IMPLEMENTATION:
    Constructs the LangGraph state machine by binding nodes and edges
    to the AgentState schema.
    """

    # 1. State Configuration:
    # Initializing the StateGraph with the AgentState schema ensures
    # data integrity across all node transitions.
    builder = StateGraph(AgentState)

    # 2. Node Registration:
    # Assigning logical identifiers to functional components.
    # 'generator' handles synthesis; 'critic' handles verification.
    builder.add_node("generator", call_model)
    builder.add_node("critic", criticize)

    # 3. Entry Point:
    # Defines the mandatory starting node for the system.
    builder.set_entry_point("generator")

    # 4. Edge Definition & Routing:
    # Sequential flow from generator to critic.
    builder.add_edge("generator", "critic")

    # Conditional flow from critic back to generator or to END.
    builder.add_conditional_edges("critic", router, {"exit": END, "retry": "generator"})

    # 5. Compilation:
    # Finalizes the graph structure into a CompiledGraph object,
    # ready for invocation via app.invoke().
    return builder.compile()


# System Instantiation
app = create_orchestrator()
