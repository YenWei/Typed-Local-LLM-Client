from pydantic import BaseModel
from llm_client.exceptions import LLMErrorBase, LLMValidationError
import json
import re

def extract_json(output: str) -> dict:
    """Extract/Convert JSON from LLM output string."""
    try:
        match = re.search(r'\{.*\}', output, re.DOTALL)
        if not match:
            raise LLMValidationError(f"No JSON found in response: {output}")
        
        json_str = match.group()
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise LLMValidationError(f"Invalid JSON format: {e.msg}") from e

def retry_generate(client, request: BaseModel, retries: int = 3) -> dict:
    """Retry logic for generating LLM output with error handling."""
    retries_count = 0
    while retries_count < retries:
        try:
            output = client.generate(request)
            return extract_json(output)
        except LLMErrorBase as e:
            retries_count += 1
            if retries_count >= retries:
                raise e


