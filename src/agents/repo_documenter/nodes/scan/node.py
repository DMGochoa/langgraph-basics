import os
from pathlib import Path

def generate_tree(dir_path: str, exclude_dirs=None) -> str:
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.venv', 'build', 'dist', '.idea', '.vscode'}
        
    tree_str = ""
    startpath = dir_path
    
    for root, dirs, files in os.walk(startpath):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # Maybe exclude some common large binary extensions
            if f.endswith(('.pyc', '.exe', '.dll', '.so', '.pdf')):
                continue
            tree_str += f"{subindent}{f}\n"
            
    return tree_str

def scan_structure_node(state: dict):
    local_path = state.get("local_path")
    if not local_path or not os.path.exists(local_path):
        raise ValueError(f"local_path '{local_path}' is invalid or does not exist.")
    
    print(f"Scanning directory structure at {local_path}...")
    structure = generate_tree(local_path)
    
    return {"structure": structure}
