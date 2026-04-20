import os

MAX_CHARS_PER_FILE = 3000
MAX_TOTAL_CHARS = 30000

def read_code_node(state: dict):
    local_path = state.get("local_path")

    allowed_extensions = {'.py', '.js', '.ts', '.md', '.json', '.txt', '.yml', '.yaml', '.sh', '.html', '.css'}
    exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'build', 'dist'}

    file_contents = {}
    total_chars = 0

    for root, dirs, files in os.walk(local_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in allowed_extensions or f.startswith('.'):
                continue

            file_path = os.path.join(root, f)
            rel_path = os.path.relpath(file_path, local_path)

            try:
                with open(file_path, 'r', encoding='utf-8') as f_in:
                    content = f_in.read(MAX_CHARS_PER_FILE)
                    file_contents[rel_path] = content
                    total_chars += len(content)
            except Exception as e:
                print(f"Failed to read {rel_path}: {e}")

            if total_chars >= MAX_TOTAL_CHARS:
                print("Warning: reached total context limit, stopping early.")
                break

        if total_chars >= MAX_TOTAL_CHARS:
            break

    print(f"Read {len(file_contents)} files ({total_chars} chars).")
    return {"file_contents": file_contents}
