from langchain_huggingface import HuggingFaceEndpoint
from utils.llm_client import LLMClient

class HuggingFaceClient(LLMClient):

    def __init__(self, api_key: str, model: str = "mistralai/Mistral-7B-Instruct-v0.3"):
        super().__init__(model)
        self.llm = HuggingFaceEndpoint(
            repo_id=self.model,
            max_length=1500,
            temperature=0.5,
            huggingfacehub_api_token=api_key
        )