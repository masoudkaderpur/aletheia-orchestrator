from operator import add
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage

"""
PURPOSE: The 'Shared Memory' of the system.
In LangGraph, nodes remain functionally isolated; they communicate exclusively by
writing to and reading from this State object. This architecture ensures the
Generator and Critic are stateless, while the Graph manages persistence.
"""


def merge_messages(
    left: list[BaseMessage], right: list[BaseMessage]
) -> list[BaseMessage]:
    """
    REDUCER LOGIC:
    LangGraph utilizes reducer functions to determine how state updates are applied.
    Instead of overwriting history, this appends new messages to the list.
    This preservation of context is critical for the Critic to analyze
    previous Generator outputs.
    """
    return left + right


class AgentState(TypedDict):
    """
    STATE SCHEMA:
    The formal definition of the system's configuration space.
    Every attribute acts as a signal for the Router's transition logic.

    Attributes:
        messages: The conversation thread containing all AI and Human interactions.
        is_factually_correct: The primary exit signal (Boolean Gate).
        iterations: A safety counter to enforce termination at n_max.
    """

    # Annotated[..., add] enables additive updates rather than overwrites.
    messages: Annotated[list[BaseMessage], add]

    is_factually_correct: bool

    # Utilizing 'add' here allows nodes to return {"iterations": 1}
    # for automatic global incrementing.
    iterations: Annotated[int, add]

    critic_feedback: str
