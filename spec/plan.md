# Proyecto: Agente Analizador y Documentador de Repositorios (LangGraph)

Este plan describe la arquitectura y los pasos para implementar un nuevo agente en tu proyecto LangGraph que toma como entrada el enlace (URL) de un repositorio, lo descarga, escanea sus archivos, lee el código y emite una documentación estructurada.

## Arquitectura y Flujo (StateGraph)

Vamos a crear un nuevo agente, por ejemplo, `repo_documenter`, manteniendo la estructura de directorios que ya vienes manejando en `src/agents/`.

**Estado del Grafo (`State`)**
El estado compartido entre los nodos almacenará:
- `repo_url` (str): El enlace a clonar provisto por el usuario.
- `local_path` (str): La ruta temporal donde se clona.
- `structure` (str/dict): Árbol de directorios escaneado.
- `file_contents` (list/dict): Contenido de los archivos clave.
- `documentation` (str): El resultado final generado en Markdown.

**Nodos (Nodes):**
1. **`clone_repo`**:
   - Descarga o clona el repositorio usando git en un directorio local temporal, o utilizando `subprocess`.
2. **`scan_structure`**:
   - Analiza las carpetas para generar una representación en texto del árbol (ignorando `node_modules`, `__pycache__`, `.git`, etc.).
3. **`read_code`**:
   - Lee el contenido interno de los archivos más relevantes (soporte para extensiones comunes: `.py`, `.js`, `.ts`, `.md`, etc.) y lo inyecta en el estado. Aquí hay un reto con los **modelos locales de LM Studio**: si el repositorio es muy largo, el contexto podría explotar. El código debe iterar o resumir partes.
4. **`generate_docs`**:
   - Toma el árbol y los contenidos recuperados y le pide al LLM generar una documentación general en Markdown.

## Estructura de Directorios a Crear

```text
root/
  spec/
    plan.md                      <-- Este archivo
  src/
    agents/
      repo_documenter/
        __init__.py
        agent.py                 <-- Inicialización del StateGraph
        state.py                 <-- Definición de TypedDict para el estado
        nodes/
          __init__.py
          clone/
             __init__.py
             node.py             <-- Lógica para git clone
             prompt.py
          scan/
             __init__.py
             node.py             <-- Lógica para listar ficheros
             prompt.py
          read_code/
             __init__.py
             node.py             <-- Extraer el contexto de los ficheros
             prompt.py
          generate/
             __init__.py
             node.py             <-- Invocación del LLM a través de LM Studio
             prompt.py
```

## Consideraciones Importantes
1. **El contexto del modelo local:**
   Los modelos locales muchas veces tienen ventanas de contexto limitadas (4K u 8K tokens dependiendo de tu hardware). Si le pasamos el proyecto entero de golpe al promp en `generate_docs`, el modelo puede bloquearse. Tendremos que validar si el nodo `read_code` debe procesar un archivo a la vez o enviar porciones del código.
2. **LM Studio (Local)**:
   Se utilizará la configuración base para apuntar a un modelo expuesto de forma local `ChatOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")` como estándar para que encaje con LM Studio.

## Preguntas Abiertas
- ¿Utilizas alguna librería específica de Git (como `GitPython`) o prefieres que use comandos estándar de subprocesos (`import subprocess`)?
- ¿Te gustaría que el resultado final de la documentación se guarde automáticamente en un archivo local extra, además de estar en el Output del graph?
