from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from .prompt import SYSTEM_PROMPT, HUMAN_PROMPT_TEMPLATE

def generate_docs_node(state: dict):
    structure = state.get("structure", "")
    file_contents = state.get("file_contents", {})
    
    # Formatear el contenido del código
    code_compilation = ""
    for path, content in file_contents.items():
        code_compilation += f"\n\n--- FILE: {path} ---\n{content}\n"
        
    human_msg = HUMAN_PROMPT_TEMPLATE.format(
        structure=structure,
        code=code_compilation
    )
    
    # Instanciar ChatOpenAI apuntando a LM Studio (localhost:1234)
    # LM Studio default config expects generic API key

    llm = init_chat_model(
        model="openai:google/gemma-4-e4b",
        base_url="http://100.105.94.89:1234/v1",
        profile={
            "structure_output": True
        }
    )
    
    print("Generating documentation via LM Studio...")
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_msg)
    ])
    
    return {"documentation": response.content}
