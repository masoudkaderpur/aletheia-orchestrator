from operator import add
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage


def merge_messages(
    left: list[BaseMessage], right: list[BaseMessage]
) -> list[BaseMessage]:
    return left + right


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add]
    is_factually_correct: bool
    iterations: int
