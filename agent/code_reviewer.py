from utils.llm import call_llm

def review_code(code):
    prompt = f"""
You are a senior code reviewer.

Check and improve:
- Edge cases
- Performance
- Readability
- PEP8

Return ONLY improved Python code.

Code:
{code}
"""
    return call_llm(prompt)