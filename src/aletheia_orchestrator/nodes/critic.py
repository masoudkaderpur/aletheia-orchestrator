from aletheia_orchestrator.nodes.generator import model
from aletheia_orchestrator.state import AgentState

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
    Evaluates the last AI message for quality and correctness.
    Returns a signal to either exit the loop or trigger a refinement.
    """
    last_response = state["messages"][-1].content
    formatted_prompt = CRITIC_PROMPT.format(last_response=last_response)

    raw_judge_response = model.invoke(formatted_prompt).content

    is_correct = raw_judge_response.strip().upper().startswith("YES")

    status = "PASSED" if is_correct else "FAILED"
    print(f"\n[CRITIC] Analysis: {status}")
    print(f"[CRITIC] Feedback: {raw_judge_response}")

    return {"is_factually_correct": is_correct}
