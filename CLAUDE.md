# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Start the LangGraph dev server (loads .env automatically)
set -a && source .env && set +a && uv run langgraph dev

# Install dependencies
uv sync

# Install project in editable mode (needed to import src packages)
uv pip install -e .

# Add a dependency
uv add <package>

# Run the repo_documenter test script
uv run python notebooks/test_repo_doc.py
```

## Architecture

This is a LangGraph learning repo. Agents are registered in `langgraph.json` and served via the LangGraph dev server.

### Agent types

**Simple agents** (`src/agents/main.py`, `simple.py`, `joke.py`) — single-file `StateGraph` definitions with typed state dicts. They demonstrate basic node/edge patterns, conditional edges, and tool binding.

**repo_documenter** (`src/agents/repo_documenter/`) — the main complex agent. It clones a public or private Git repo, scans it, reads source files, generates documentation via an LLM, then pulls/commits/pushes back to the repo. Each step is a separate node file under `nodes/<name>/node.py`. The state schema is in `state.py`. Conditional edges route to `END` on any error.

**support** (`src/agents/support/`) — stub agent, not yet implemented.

### LLM configuration

The repo targets **LM Studio** (local inference server) rather than the real OpenAI API. The `OPENAI_API_KEY` in `.env` is set to `"lm-studio"` and the base URL points to a local LM Studio instance. To switch models, update the `base_url` and `model` in the relevant agent file.

### Error propagation pattern

Nodes set `state["error"]` on failure. The graph uses conditional edges that check for a non-empty `error` field and route to `END`, short-circuiting the rest of the pipeline.

### File reading limits in repo_documenter

`read_code` node caps each file at **3 KB** and total context at **30 KB** to stay within LLM context windows. Supported extensions: `.py .js .ts .md .json .txt .yml .yaml .sh .html .css`.

### Notebooks

Jupyter notebooks in `notebooks/` are numbered learning exercises (001–007). They are standalone and not imported by the agents.
