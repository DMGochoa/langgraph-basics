import subprocess

def pull_node(state: dict):
    local_path = state.get("local_path")
    branch = state.get("branch", "main")
    remote = state.get("git_remote", "origin")

    print(f"Pulling {remote}/{branch}...")
    try:
        result = subprocess.run(
            ["git", "-C", local_path, "pull", remote, branch],
            capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        return {"error": "pull_timeout"}

    if result.returncode != 0 or "CONFLICT" in result.stdout or "CONFLICT" in result.stderr:
        conflict_result = subprocess.run(
            ["git", "-C", local_path, "diff", "--name-only", "--diff-filter=U"],
            capture_output=True, text=True
        )
        conflict_files = [f for f in conflict_result.stdout.strip().splitlines() if f]
        print(f"Merge conflicts detected in: {conflict_files}")
        return {"conflict_files": conflict_files, "error": "merge_conflict"}

    return {"conflict_files": []}
