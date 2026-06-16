import json
import re
from pydantic import BaseModel
from pydantic import ValidationError
from llm_client.exceptions import LLMErrorBase, LLMValidationError, LLMTimeoutError

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

def retry_generate(client, request: BaseModel, output_Type: type[BaseModel], retries: int = 3) -> tuple[str, BaseModel]:
    """Retry logic for generating LLM output with error handling."""
    retries_count = 0
    while retries_count < retries:
        try:
            output = client._generate(request)
            json_data = extract_json(output)
            typed_data = output_Type.model_validate(json_data)
            return (output, typed_data)
        except LLMErrorBase as e:
            if isinstance(e, LLMValidationError) and retries_count == 0:
                request = request.model_copy(update={"prompt": request.prompt + "\nRespond with valid JSON only."})

            retries_count += 1
            if retries_count >= retries:
                raise LLMTimeoutError(str(e)) from e

        except ValidationError as e:
            if retries_count == 0:
                request = request.model_copy(update={"prompt": request.prompt + "\nRespond with JSON matching the requested schema only."})

            retries_count += 1
            if retries_count >= retries:
                raise LLMTimeoutError(str(e)) from e


