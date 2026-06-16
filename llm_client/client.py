import ollama
from ollama import ResponseError, GenerateResponse
from pydantic import BaseModel
from llm_client.retry import retry_generate
from llm_client.schemas import LLMRequest, LLMResponse
from llm_client.exceptions import LLMErrorBase, LLMValidationError

class LLMClient:
    host : str
    client : ollama.Client
    max_retries_count: int

    def __init__(self, host: str):
        self.host = host
        self.client = ollama.Client(host)
        self.max_retries_count = 3

    def ping(self) -> bool:
        try:
            self.client.list();
            return True
        except Exception as e:
            print(f"Error pinging LLM server: {e}")
            return False
        
    def generate_reply(self, request: LLMRequest, output_Type: type[BaseModel]) -> LLMResponse:
        try:
            raw, response = retry_generate(self, request, output_Type, self.max_retries_count)
            return LLMResponse(raw=raw, data=response)
        
        except (ResponseError, LLMErrorBase) as e:
            print(f"Error generating response from LLM: {e}")
            return LLMResponse(raw="", data=None)
        
    def _generate(self, request: LLMRequest) -> str:
        try:
            response = self.client.generate(model=request.model, prompt=request.prompt)
            return response.response
        except ResponseError as e:
            print(f"Error generating response from LLM: {e}")
            raise LLMValidationError(f"Error generating response from LLM: {e}") from e
        
    def _generateRAW(self, request: LLMRequest) -> GenerateResponse:
        try:
            response = self.client.generate(model=request.model, prompt=request.prompt)
            return response
        except ResponseError as e:
            raise ResponseError(f"Error generating response from LLM: {e}") from e
        