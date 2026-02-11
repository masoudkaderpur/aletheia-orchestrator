from aletheia_orchestrator.nodes.generator import model
from aletheia_orchestrator.state import AgentState

"""
PURPOSE: The 'Verification Node' (C).
This component acts as an 'LLM-as-a-Judge'. It audits the Generator's
output against defined standards to determine if the orchestration
goal has been met.
"""

CRITIC_PROMPT = """
### ROLE
You are a rigorous Quality Assurance Auditor.
Your goal is to ensure that the provided information is accurate,
complete, and free of contradictions.

### EVALUATION CRITERIA
1. **Accuracy**: Is the information factually correct based on current consensus?
2. **Completeness**: Does it address the core of the user's request
without omitting critical context?
3. **Clarity**: Is the explanation logically structured and professional?

### INPUT TO EVALUATE
{last_response}

### OUTPUT FORMAT
Your response MUST start with:
'YES | [One sentence of praise for what was done correctly]'
OR
'NO | [One sentence of specific instruction on what to fix]'

Keep it professional and concise.
"""


def criticize(state: AgentState):
    """
    VERIFICATION LOGIC:
    Retrieves the most recent message from the state history and subjects
    it to a formal audit based on the CRITIC_PROMPT.
    """

    # 1. Input Extraction:
    # Accesses the content of the final message in the 'messages' list.
    last_response = state["messages"][-1].content
    formatted_prompt = CRITIC_PROMPT.format(last_response=last_response)

    # 2. Inference:
    # Invokes the model (reusing the gpt-4o instance from generator.py)
    # to perform the zero-shot audit.
    raw_judge_response = model.invoke(formatted_prompt).content

    # 3. Signal Extraction:
    # Parses the string response to set the 'is_factually_correct' boolean.
    # The startswith("YES") check creates a binary switch for the router.
    is_correct = raw_judge_response.strip().upper().startswith("YES")

    # 4. Observability:
    # Outputs the audit result to the console for real-time monitoring.
    status = "PASSED" if is_correct else "FAILED"
    print(f"\n[CRITIC] Analysis: {status}")
    print(f"[CRITIC] Feedback: {raw_judge_response}")

    # STATE UPDATE:
    # Returns only the boolean signal. Note that currently,
    # the textual feedback is printed but not stored back in 'messages'.
    return {"is_factually_correct": is_correct}
