import subprocess

def run_tests():
    try:
        result = subprocess.run(
            ["pytest", "generated/test_solution.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)