from src.utils.llm_client import LLMClient
from langchain_ollama.llms import OllamaLLM

class OllamaClient(LLMClient):

    def __init__(self, model: str = "llama2", base_url: str = "http://127.0.0.1:11434"):
        super().__init__(model)
        self.llm = OllamaLLM(model=self.model, base_url=base_url)