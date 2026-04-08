# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# deactivate the virtual environment
deactivate
rm -rf .venv

## init
uv init
uv venv

# add dependencies
uv add langgraph langchain langchain-openai langchain-ollama 
uv add "fastapi[standard]"

# add dev dependencies
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel --dev
uv add grandalf --dev

# run the agent
set -a && source .env && set +a && uv run langgraph dev

# install the project
Entonces para tomar los cambios lo que podemos hacer es compilar el proyecto.

uv pip install -e .


```toml
[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]
```