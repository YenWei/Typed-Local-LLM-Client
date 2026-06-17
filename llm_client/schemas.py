from pydantic import BaseModel
from pydantic import field_validator
from typing import Literal

class LLMRequest(BaseModel):
    model: str = "qwen2.5:7b-instruct-q4_K_M"
    prompt: str

    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, val: str) -> str:
        if len(val.strip()) == 0:
            raise ValueError('Prompt cannot be empty or whitespace')
        return val
    
class LLMResponse(BaseModel):
    raw: str
    data: BaseModel | None = None


class TaskSummary(BaseModel):
    title: str
    complexity: Literal['low', 'medium', 'high']
    estimated_minutes: int
    key_steps: list[str]

