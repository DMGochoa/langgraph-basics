import subprocess
import tempfile
import atexit
import shutil

def clone_repo_node(state: dict):
    repo_url = state.get("repo_url")
    if not repo_url:
        raise ValueError("No repo_url provided in state.")

    token = state.get("github_token")
    if token and repo_url.startswith("https://"):
        host = repo_url.replace("https://", "")
        repo_url = f"https://{token}@{host}"

    temp_dir = tempfile.mkdtemp(prefix="repo_doc_")
    atexit.register(shutil.rmtree, temp_dir, True)

    print(f"Cloning into {temp_dir}...")
    try:
        subprocess.run(
            ["git", "clone", repo_url, temp_dir],
            check=True, capture_output=True, text=True, timeout=60
        )
    except subprocess.CalledProcessError as e:
        return {"error": f"clone_failed: {e.stderr.strip()}"}
    except subprocess.TimeoutExpired:
        return {"error": "clone_timeout"}

    return {"local_path": temp_dir}
