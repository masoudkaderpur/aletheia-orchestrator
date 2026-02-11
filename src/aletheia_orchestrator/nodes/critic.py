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
4. **Formal Integrity**: Does the response maintain an academic tone,
avoiding all conversational filler and social pleasantries?

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
    # Invokes the model (reusing the gpt-4o instance) to perform the audit.
    raw_judge_response = model.invoke(formatted_prompt).content

    # 3. Qualitative Feedback Extraction:
    # Splits the response at the pipe operator. This ensures the Generator
    # receives only the actionable instructions, stripped of the YES/NO prefix.
    parts = raw_judge_response.split("|", 1)
    feedback = parts[1].strip() if len(parts) > 1 else raw_judge_response

    # 4. Signal Extraction:
    # Sets the boolean gate. startswith("YES") creates the binary switch
    # required by the conditional edge in graph.py.
    is_correct = raw_judge_response.strip().upper().startswith("YES")

    # 5. Observability:
    # Real-time console output for monitoring the internal reasoning loop.
    status = "PASSED" if is_correct else "FAILED"
    print(f"\n[CRITIC] Analysis: {status}")
    print(f"[CRITIC] Feedback: {raw_judge_response}")

    # STATE UPDATE:
    # Injects both the binary signal (for routing) and the qualitative feedback
    # (for the next generation cycle) back into the state.
    return {"is_factually_correct": is_correct, "critic_feedback": feedback}
