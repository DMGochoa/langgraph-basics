import os

def save_doc_node(state: dict):
    documentation = state.get("documentation", "")
    local_path = state.get("local_path", "")

    output_path = os.path.join(local_path, "DOCUMENTATION.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(documentation)

    print(f"Documentation saved to {output_path}")
    return {"output_file_path": output_path}
