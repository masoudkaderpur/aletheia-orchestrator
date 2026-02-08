from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    Representing the state of the Aletheia-Orchestrator.

    Attributes:
        messages: A sequence of messages in the conversation,
                  utilizing add_messages for iterative refinement.
        next_step: A control variable for the state machine's decision logic.
        is_grounded: A boolean flag indicating if the critic has verified the output.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_step: str
    is_grounded: bool
