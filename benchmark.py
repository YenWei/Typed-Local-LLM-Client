import time
import sys
import os
import re
import json
from pydantic import BaseModel, ValidationError
from typing import Literal
from llm_client.client import LLMClient
from llm_client.schemas import LLMRequest

class BenchmarkReply(BaseModel):
    answer: str
    confidence: Literal["low", "medium", "high"]

def extract_json(output: str) -> dict:
    """Extract/Convert JSON from LLM output string."""

    match = re.search(r'\{.*\}', output, re.DOTALL)
    if not match:
        return {}
    
    json_str = match.group()
    return json.loads(json_str)

def eval_test_prompts(prompt: str, response: str) -> str | None:
    normalized = response.strip().lower()

    if prompt == "Say HELLO in reply. No other words/format.":
        if normalized == "hello":
            return "instruction"

    elif prompt == "Where is the capital of Japan?":
        if "tokyo" in normalized:
            return "stable_fact"

    elif prompt == "Which country is hosting World Cup 2026?":
        if "united states" in normalized and "canada" in normalized and "mexico" in normalized:
            return "modern_fact"

    return None

if __name__ == "__main__":
    test_prompts = ["Say HELLO in reply. No other words/format.", 
                    "Where is the capital of Japan?", 
                    "Which country is hosting World Cup 2026?"]
    
    test_schema_prompts = ["Which country won World Cup 2022?", 
                           "What is a RAG system?"]
    
    test_models = ["qwen2.5:7b-instruct-q4_K_M" ,
                   "mistral:7b-instruct-q4_K_M" ,
                   "llama3.1:8b-instruct-q4_K_M",
                   "gemma4:e4b",
                   "qwen3:8b"]
    
    schema_prompt = """ 
        Return JSON only with this exact schema:
        {
            "answer": str,
            "confidence": "low" | "medium" | "high"
        }\n
    """
    
    HOST_URL = os.environ.get("OLLAMA_HOST")
    if not HOST_URL:
        print("Error: OLLAMA_HOST is not set. Terminating execution...")
        sys.exit(1)

    test_client = LLMClient(HOST_URL)
    assert test_client.ping() == True

    for currModel in test_models:
        total_model_latency = 0.0
        min_model_latency =  99999.99
        max_model_latency = -99999.99

        total_generated_tokens = 0

        instruction_pass = 0
        stable_fact_pass = 0
        modern_fact_pass = 0

        schema_pass = 0
        schema_fail = 0

        print(f"Benchmarking for current Model: {currModel}\n")

        for currPrompt in test_prompts:
            start = time.perf_counter()
            raw_response = test_client._generateRAW(LLMRequest(model=currModel, prompt=currPrompt))
            end = time.perf_counter()

            currLatency = end - start
            total_model_latency += currLatency
            if currLatency < min_model_latency:
                min_model_latency = currLatency
            if currLatency > max_model_latency:
                max_model_latency = currLatency

            total_generated_tokens += raw_response.eval_count
            passed_case = eval_test_prompts(currPrompt, raw_response.response)
            if passed_case == "instruction":
                instruction_pass += 1
            elif passed_case == "stable_fact":
                stable_fact_pass += 1
            elif passed_case == "modern_fact":
                modern_fact_pass += 1

            print(f"Current Prompt: {currPrompt}")
            print(f"Current Response: {raw_response.response}")
            print(f"Current Prompt Latency: {currLatency}")
            print(f"Current Generated Tokens: {raw_response.eval_count}")
            print(f"Current Tokens / sec: {raw_response.eval_count / (raw_response.eval_duration / 1000000000)}")
            print("\n")

        for nextPrompt in test_schema_prompts:
            structured_prompt = schema_prompt + nextPrompt

            raw_response = test_client._generateRAW(LLMRequest(model=currModel, prompt=structured_prompt))

            print(f"Current Prompt: {nextPrompt}")

            try:
                extracted_data = extract_json(raw_response.response)
                if extracted_data:
                    validated_data = BenchmarkReply.model_validate(extracted_data)
                    print(f"Current Extracted Response: [Confidence: {validated_data.confidence}] {validated_data.answer}")
                    print("Current Schema Check PASSED.")
                    print("\n")

                    schema_pass += 1

            except ValidationError as err:
                print("Current Schema Check FAILED.")
                schema_fail += 1
                continue
    
        print("Benchmark Summary")
        print(f"Instruction Following: {'PASS' if instruction_pass == 1 else 'FAIL'}")
        print(f"Stable Fact Correct: {'PASS' if stable_fact_pass == 1 else 'FAIL'}")
        print(f"Modern Fact Correct: {'PASS' if modern_fact_pass == 1 else 'FAIL'}")
        print(f"Schema Checks Passed: {schema_pass}/{len(test_schema_prompts)}")
        print(f"Schema Checks Failed: {schema_fail}/{len(test_schema_prompts)}")
        print(f"Average Generated Tokens: {total_generated_tokens / len(test_prompts)}")
        print(f"Average Latency: {total_model_latency / len(test_prompts)}")
        print(f"Min Latency: {min_model_latency}")
        print(f"Max Latency: {max_model_latency}")
        print("\n")


