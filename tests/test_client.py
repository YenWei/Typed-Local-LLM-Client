import pytest
from unittest.mock import MagicMock, patch
from llm_client.client import LLMClient, LLMRequest

MOCK_OLLAMA_HOST_URL = "http://localhost:1234"

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
        result = client.generate(LLMRequest(prompt="dummy"))

        assert result == mock_response.response