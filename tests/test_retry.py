import pytest
from llm_client.exceptions import LLMValidationError
from llm_client.retry import extract_json, retry_generate

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
        def generate(self, request):
            return "Here is the response: {\"key\": \"value\", \"number\": 123}"
        
    client = MockClient()
    request = {}
    result = retry_generate(client, request, 3)

    assert result == {"key": "value", "number": 123}

def test_retry_generate_max_retries():
    class MockClient:
        def generate(self, request):
            return "Invalid response"
        
    client = MockClient()
    request = {}
    with pytest.raises(LLMValidationError) as exec_error:
        retry_generate(client, request, 3)
