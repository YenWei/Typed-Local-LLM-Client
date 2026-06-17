import pytest
from pydantic import ValidationError
from llm_client.schemas import LLMRequest, TaskSummary

def test_llmrequest_valid():
    # just testing class defaults and validation
    request = LLMRequest(prompt="What is the capital of Singapore?")
    assert request.prompt == "What is the capital of Singapore?"
    assert request.model == "qwen2.5:7b-instruct-q4_K_M"

@pytest.mark.parametrize("empty_prompt", ["", "   ", "\t", "\n"])
def test_llmrequest_empty_prompt(empty_prompt):
    with pytest.raises(ValidationError) as exec_error:
        LLMRequest(prompt=empty_prompt)
    assert "Prompt cannot be empty or whitespace" in str(exec_error.value)

def test_tasksummary_valid():
    summary = TaskSummary(
        title="Test Task Summary",
        complexity="medium",
        estimated_minutes=5,
        key_steps=["Step 1 - Test", "Step 2 - Task", "Step 3 - Summary"]
    )
    assert summary.title == "Test Task Summary"
    assert summary.complexity == "medium"
    assert summary.estimated_minutes == 5
    assert summary.key_steps == ["Step 1 - Test", "Step 2 - Task", "Step 3 - Summary"]


@pytest.mark.parametrize("complexity", ["", "   ", "critical"])
def test_tasksummary_invalid_complexity(complexity):
    with pytest.raises(ValidationError) as exec_error:
        summary = TaskSummary(complexity=complexity)