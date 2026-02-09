from operator import add
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage


def merge_messages(
    left: list[BaseMessage], right: list[BaseMessage]
) -> list[BaseMessage]:
    """
    Reducer function to append new messages to the existing state history.
    Ensures the conversation context is preserved for iterative refinement.
    """
    return left + right


class AgentState(TypedDict):
    """
    Maintains the orchestration state for the Aletheia-Orchestrator.

    Attributes:
        messages: Accumulated history of generator outputs and critic feedback.
        is_factually_correct: Convergence signal used to exit the refinement loop.
        iterations: Guardrail counter to prevent infinite recursion during k-refinement.
    """

    messages: Annotated[list[BaseMessage], add]
    is_factually_correct: bool
    iterations: Annotated[int, add]
