import pytest
from llm_client.exceptions import LLMValidationError, LLMTimeoutError
from llm_client.retry import extract_json, retry_generate
from llm_client.schemas import LLMRequest, TaskSummary

def test_extract_json_valid():
    output = "Here is the response: {\"key\": \"value\", \"number\": 123}"
    result = extract_json(output)
    assert result == {"key": "value", "number": 123}

    output = "Here is the empty reponse: {}"
    result = extract_json(output)
    assert result == {}

def test_extract_json_invalid():
    output = "Invalid response"
    with pytest.raises(LLMValidationError) as exec_error:
        extract_json(output)

def test_retry_generate_success():
    class MockClient:
        def _generate(self, request):
            return "Here is the response: {\"title\": \"value\", \"complexity\": \"medium\", \"estimated_minutes\": \"3\", \"key_steps\":[]}"
        
    client = MockClient()
    request = LLMRequest(prompt="Dummy prompt.")
    result = retry_generate(client, request, TaskSummary, 3)

    valid_data = result[1].model_dump()
    assert valid_data == {"title": "value", "complexity": "medium", "estimated_minutes": 3, "key_steps": []}

def test_retry_generate_max_retries():
    class MockClient:
        def _generate(self, request):
            return "Invalid response"
        
    client = MockClient()
    request = LLMRequest(prompt="Dummy prompt.")
    with pytest.raises(LLMTimeoutError) as exec_error:
        retry_generate(client, request, TaskSummary, 3)

def test_retry_generate_bad_json():
    received_prompts = []

    class MockClient:
        def _generate(self, request):
            received_prompts.append(request.prompt)
            return "Bad JSON"
        
    client = MockClient()
    request = LLMRequest(prompt="Dummy prompt.")
    with pytest.raises(LLMTimeoutError) as exec_error:
        retry_generate(client, request, TaskSummary, 3)
    assert "Dummy prompt." in received_prompts[0]
    assert "\nRespond with valid JSON only." in received_prompts[1]

def test_retry_generate_bad_schema():
    received_prompts = []

    class MockClient:
        def _generate(self, request):
            received_prompts.append(request.prompt)
            return "Here is the response: {\"key\": \"value\", \"number\": 123}"
        
    client = MockClient()
    request = LLMRequest(prompt="Dummy prompt.")
    with pytest.raises(LLMTimeoutError) as exec_error:
        retry_generate(client, request, TaskSummary, 3)
    assert "Dummy prompt." in received_prompts[0]
    assert "\nRespond with JSON matching the requested schema only." in received_prompts[1]

