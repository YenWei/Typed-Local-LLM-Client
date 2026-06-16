import pytest
import os
from unittest.mock import MagicMock, patch
from llm_client.client import LLMClient, LLMRequest
from llm_client.schemas import TaskSummary

MOCK_OLLAMA_HOST_URL = str("http://localhost:1234")

def test_client_ping():
    with patch('llm_client.client.ollama.Client') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.list.return_value = []
        client = LLMClient(MOCK_OLLAMA_HOST_URL)
        assert client.ping() == True

def test_client_ping_invalid():
    with patch('llm_client.client.ollama.Client') as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.list.side_effect = Exception("connection refused")

        client = LLMClient(MOCK_OLLAMA_HOST_URL)
        assert client.ping() == False

def test_client_generate():
    with patch('llm_client.client.ollama.Client') as MockClient:
        mock_instance = MockClient.return_value

        mock_response = MagicMock()
        mock_response.response = "Test Generate"
        mock_instance.generate.return_value = mock_response

        client = LLMClient(MOCK_OLLAMA_HOST_URL)
        result = client._generate(LLMRequest(prompt="dummy"))

        assert result == mock_response.response

def test_client_generate_reply():
    with patch('llm_client.client.ollama.Client') as MockClient:
        mock_instance = MockClient.return_value

        mock_response = MagicMock()
        mock_response.response ="""
                                {
                                "title": "Test Generate",
                                "complexity": "medium",
                                "estimated_minutes": 3,
                                "key_steps": ["Step 1", "Step 2", "Step 3"]
                                }
                                """
        mock_instance.generate.return_value = mock_response

        client = LLMClient(MOCK_OLLAMA_HOST_URL)
        result = client.generate_reply(LLMRequest(prompt="dummy"), output_Type=TaskSummary)

        assert result.raw == mock_response.response
        assert isinstance(result.data, TaskSummary)
        assert result.data.title == "Test Generate"
        assert result.data.complexity == "medium"
        assert result.data.estimated_minutes == 3
        assert result.data.key_steps == ["Step 1", "Step 2", "Step 3"]

def test_client_generate_reply_invalid():
    with patch('llm_client.client.ollama.Client') as MockClient:
        mock_instance = MockClient.return_value

        mock_response = MagicMock()
        mock_response.response = "Here is the response: {\"key\": \"value\", \"number\": 123}"
        mock_instance.generate.return_value = mock_response

        client = LLMClient(MOCK_OLLAMA_HOST_URL)
        result = client.generate_reply(LLMRequest(prompt="dummy"), output_Type=TaskSummary)

        assert result.raw == "" and result.data == None
        assert not isinstance(result.data, TaskSummary)

@pytest.mark.integration
def test_client_integration():
    REAL_OLLAMA_HOST_URL = os.environ.get("OLLAMA_HOST")
    if not REAL_OLLAMA_HOST_URL:
        pytest.skip("OLLAMA HOST not set")

    test_client = LLMClient(REAL_OLLAMA_HOST_URL)
    assert test_client != None
    assert test_client.ping() == True

    simple_prompt = "Say HELLO in reply. No other words."
    reply = test_client._generate(LLMRequest(prompt=simple_prompt))

    assert reply != None and len(reply) > 0
