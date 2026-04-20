from langgraph.graph import StateGraph, END
from .state import RepoDocumenterState
from .nodes.clone.node import clone_repo_node
from .nodes.scan.node import scan_structure_node
from .nodes.read_code.node import read_code_node
from .nodes.generate.node import generate_docs_node
from .nodes.save_doc.node import save_doc_node
from .nodes.pull.node import pull_node
from .nodes.commit.node import commit_node
from .nodes.push.node import push_node


def _route_after_clone(state: RepoDocumenterState) -> str:
    return "error" if state.get("error") else "scan"


def _route_after_pull(state: RepoDocumenterState) -> str:
    if state.get("conflict_files"):
        return "conflict"
    if state.get("error"):
        return "error"
    return "commit"


def _route_after_push(state: RepoDocumenterState) -> str:
    return "error" if state.get("error") else END


def build_repo_documenter_graph():
    workflow = StateGraph(RepoDocumenterState)

    workflow.add_node("clone", clone_repo_node)
    workflow.add_node("scan", scan_structure_node)
    workflow.add_node("read", read_code_node)
    workflow.add_node("generate", generate_docs_node)
    workflow.add_node("save_doc", save_doc_node)
    workflow.add_node("pull", pull_node)
    workflow.add_node("commit", commit_node)
    workflow.add_node("push", push_node)

    workflow.set_entry_point("clone")

    workflow.add_conditional_edges("clone", _route_after_clone, {
        "scan": "scan",
        "error": END,
    })
    workflow.add_edge("scan", "read")
    workflow.add_edge("read", "generate")
    workflow.add_edge("generate", "save_doc")
    workflow.add_edge("save_doc", "pull")

    workflow.add_conditional_edges("pull", _route_after_pull, {
        "commit": "commit",
        "conflict": END,
        "error": END,
    })
    workflow.add_edge("commit", "push")

    workflow.add_conditional_edges("push", _route_after_push, {
        END: END,
        "error": END,
    })

    return workflow.compile()


agent = build_repo_documenter_graph()
