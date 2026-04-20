import os
import sys

# Añadir src al path para que pueda importar el módulo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.repo_documenter.agent import graph

def main():
    repo_url = "https://github.com/langchain-ai/langgraph-example.git" # Ejemplo pequeño
    print(f"Ejecutando Agente con URL: {repo_url}\n")
    
    # El estado inicial solo necesita la url
    initial_state = {"repo_url": repo_url}
    
    # Se va a usar .invoke(), o .stream(). Usaremos stream para ver el paso a paso
    for step in graph.stream(initial_state):
        for key, value in step.items():
            print(f"\n--- Nodo ejecutado: {key} ---")
            
            # Print brief summary of state values
            if "local_path" in value:
                print(f"Ruta Local: {value['local_path']}")
            if "structure" in value:
                print(f"Estructura encontrada:\n{value['structure'][:200]}...\n")
            if "file_contents" in value:
                print(f"Archivos leídos: {len(value['file_contents'])}")
                
            if "documentation" in value:
                print(f"\n=== DOCUMENTACIÓN FINAL GENERADA ===")
                print(value["documentation"])

if __name__ == "__main__":
    main()
