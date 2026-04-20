from typing import TypedDict, Dict, List, Optional

class RepoDocumenterState(TypedDict):
    repo_url: str
    local_path: str
    structure: str
    file_contents: Dict[str, str]
    documentation: str
    commit_message: str
    branch: str
    git_remote: str
    github_token: Optional[str]
    conflict_files: List[str]
    error: Optional[str]
    output_file_path: Optional[str]
