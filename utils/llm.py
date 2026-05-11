from langchain_community.llms import Ollama

def get_llm():
    llm = Ollama(
        model="qwen2.5"
    )
    return llm