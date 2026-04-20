import subprocess

def commit_node(state: dict):
    local_path = state.get("local_path")
    commit_message = state.get("commit_message", "docs: add generated documentation")

    subprocess.run(["git", "-C", local_path, "add", "."], check=True, capture_output=True)

    result = subprocess.run(
        ["git", "-C", local_path, "status", "--porcelain"],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        print("Nothing to commit.")
        return {}

    try:
        subprocess.run(
            ["git", "-C", local_path, "commit", "-m", commit_message],
            check=True, capture_output=True, text=True
        )
        print(f"Committed: {commit_message}")
    except subprocess.CalledProcessError as e:
        return {"error": f"commit_failed: {e.stderr.strip()}"}

    return {}
