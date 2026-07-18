from utils.llm import call_llm

def fix_code(task, code, error):
    prompt = f"""
You are debugging Python code.

Task:
{task}

Current Code:
{code}

Error Output:
{error}

Fix the issue and return ONLY corrected Python code.
Do NOT include explanations.
"""
    return call_llm(prompt)