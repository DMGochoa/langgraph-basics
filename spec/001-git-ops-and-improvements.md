# 001 - Git Ops y Mejoras al Repo Documenter

## Nuevos nodos a agregar

```
nodes/
  commit/node.py    # git add + git commit
  pull/node.py      # git pull con manejo de conflictos
  push/node.py      # git push con manejo de auth
```

**Flujo propuesto:**
```
clone → scan → read → generate → pull → commit → push → END
```

Con conditional edges en `pull` y `push` para manejar errores.

---

## State — campos a agregar en `state.py`

```python
class RepoDocumenterState(TypedDict):
    # ... campos actuales ...
    commit_message: str
    branch: str
    git_remote: str
    conflict_files: List[str]        # archivos con conflicto detectados
    error: Optional[str]             # error capturado en cualquier nodo
    output_file_path: Optional[str]  # ruta local del .md generado
```

---

## Nodo `pull/node.py`

```python
result = subprocess.run(["git", "pull", "origin", branch], ...)
# Detectar conflictos parseando stdout/stderr:
if "CONFLICT" in result.stdout or result.returncode != 0:
    # Extraer archivos conflictivos con: git diff --name-only --diff-filter=U
    return {"conflict_files": [...], "error": "merge_conflict"}
```

Si hay conflicto → conditional edge que va a un nodo `resolve_conflict` o termina con error en el state.

---

## Nodo `push/node.py` — auth

Para repos privados con `subprocess`, opciones de autenticación:
1. **SSH key** (recomendado): esperar que la URL sea `git@github.com:...`
2. **Token en URL**: `https://<TOKEN>@github.com/user/repo` — pasarlo como campo extra `github_token` en el state
3. **git credential store**: configurar antes del push con `subprocess`

---

## Grafo con conditional edges

```python
from langgraph.graph import StateGraph, END

def has_conflict(state):
    return "conflict" if state.get("conflict_files") else "commit"

workflow.add_conditional_edges("pull", has_conflict, {
    "conflict": END,   # o nodo de resolución
    "commit": "commit"
})
```

---

## Problemas actuales a corregir

| Problema | Ubicación | Fix |
|---|---|---|
| `tempfile.mkdtemp` no se limpia nunca | `clone/node.py` | Usar `atexit` o campo `cleanup` en state para borrar al final |
| `MAX_CHARS=30000` global, no por archivo | `read_code/node.py` | Truncar por archivo individualmente (ej: max 3000 chars/archivo) |
| Sin timeout en `git clone` | `clone/node.py` | Agregar `timeout=60` a `subprocess.run` |

---

## Estructura final del grafo

```
clone → scan → read → generate → [save_doc] → pull → commit → push → END
                                                         ↓ (conflict)
                                                        END (con error en state)
```

`save_doc` es opcional para persistir el `.md` localmente antes de hacer push.
