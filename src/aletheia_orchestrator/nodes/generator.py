import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from aletheia_orchestrator.state import AgentState

"""
PURPOSE: The 'Synthesis Node' (G).
Responsible for generating and refining technical content. It operates
in a reactive manner, adapting its output based on Critic feedback.
"""

BASE_SYSTEM_PROMPT = """
### ROLE
You are an elite Academic Professor and Senior Technical Architect.
Your goal is to provide exhaustive, factually impeccable,
and highly structured technical explanations.

### TONE & STYLE
1. **No Conversational Filler**: Absolutely no "I'd be happy to help,"
"Here is your answer," or "I hope this helps." Start directly with the content.
2. **Academic Precision**: Use formal, objective language.
Avoid emotional expressions or fluff.
3. **Accessibility**: Use technical terms where necessary for precision,
but define them immediately if they are complex.
The goal is deep understanding, not obfuscation.
4. **Logical Thread (Roter Faden)**: Every response must
follow a deductive reasoning chain—from
first principles to complex application.
5. **No Interaction**: Do not ask follow-up questions or seek validation.
 Provide the definitive answer.

### STRUCTURAL GUIDELINES
- Use markdown headers (##, ###) for clear hierarchy.
- Use bold text for key concepts to enhance scannability.
- If code or math is involved, ensure it is presented in an
industry-standard, clean format.
"""

load_dotenv()

# MODEL CONFIGURATION:
# temperature=0 ensures deterministic, high-fidelity technical output.
model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("GITHUB_TOKEN"),
    base_url="https://models.inference.ai.azure.com",
)


def call_model(state: AgentState):
    """
    GENERATION LOGIC:
    Processes message history and applies iterative corrections under
    strict academic grounding.
    """

    # 1. Context Retrieval:
    # Extract existing history and any qualitative feedback from the Critic.
    messages = state["messages"]
    feedback = state.get("critic_feedback", "")

    # 2. System Grounding:
    # The BASE_SYSTEM_PROMPT is always the first message to set the persona.
    input_messages = [SystemMessage(content=BASE_SYSTEM_PROMPT)] + messages

    # 3. Dynamic Prompt Engineering:
    # If feedback exists, a SystemMessage is appended to the message list.
    # This acts as a high-priority instruction, forcing the LLM to address
    # specific weaknesses identified in the previous iteration.
    if feedback:
        feedback_instruction = SystemMessage(
            content=(
                f"Feedback to your last response: {feedback}\n"
                "Please correct your response based on"
                "this feedback and your instructions"
            )
        )
        input_messages.append(feedback_instruction)

    # 4. Inference:
    # The model processes the full context (History + Feedback).
    response = model.invoke(input_messages).content

    # STATE UPDATE:
    # 1. messages: New response is added to the history.
    # 2. iterations: Counter is incremented via the State's 'add' reducer.
    return {"messages": [AIMessage(content=response)], "iterations": 1}
