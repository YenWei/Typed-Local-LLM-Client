import ollama
from ollama import ResponseError
from llm_client.schemas import LLMRequest
from llm_client.exceptions import LLMUnavailableError, LLMValidationError

class LLMClient:
    host : str
    client : ollama.Client

    def __init__(self, host: str):
        self.host = host
        self.client = ollama.Client(host)

    def ping(self) -> bool:
        try:
            self.client.list();
            return True
        except Exception as e:
            print(f"Error pinging LLM server: {e}")
            return False
        
    def generate(self, request: LLMRequest) -> str:        
        try:
            response = self.client.generate(model=request.model, prompt=request.prompt)
            return response.response
        except ResponseError as e:
            print(f"Error generating response from LLM: {e}")
            raise LLMValidationError(f"Error generating response from LLM: {e}") from e