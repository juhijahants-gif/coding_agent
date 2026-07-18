from utils.llm import call_llm

def generate_code(task: str) -> str:
    prompt = f"""
You are a senior Python developer.

Write COMPLETE, runnable Python code.

Task:
{task}

Rules:
- Return ONLY code
- No explanation
- No markdown
- Must be valid Python
"""

    response = call_llm(prompt)

    if not response:
        return "❌ Error: Empty response from LLM"

    return response