import subprocess

def push_node(state: dict):
    local_path = state.get("local_path")
    branch = state.get("branch", "main")
    remote = state.get("git_remote", "origin")

    print(f"Pushing to {remote}/{branch}...")
    try:
        result = subprocess.run(
            ["git", "-C", local_path, "push", remote, branch],
            capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        return {"error": "push_timeout"}

    if result.returncode != 0:
        return {"error": f"push_failed: {result.stderr.strip()}"}

    print("Push successful.")
    return {}
