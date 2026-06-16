import time
from llm_client.client import LLMClient
from llm_client.schemas import LLMRequest

if __name__ == "__main__":
    HOST_URL = "http://10.170.10.109:11434"

    test_prompts = ["Say HELLO in reply. No other words/format.", 
                    "Where is the capital of Singapore?", 
                    "what is the host country of World Cup 2026?"]
    
    test_models = ["qwen2.5:7b-instruct-q4_K_M" ,
                   "mistral:7b-instruct-q4_K_M" ,
                   "llama3.1:8b-instruct-q4_K_M",
                   "gemma4:e4b"]

    test_client = LLMClient(HOST_URL)
    assert test_client.ping() == True

    for currModel in test_models:
        total_model_latency = 0.0
        min_model_latency =  99999.99
        max_model_latency = -99999.99

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

            print(f"Current Prompt: {currPrompt}")
            print(f"Current Response: {raw_response.response}")
            print(f"Current Prompt Latency: {currLatency}")
            print(f"Current Generated Tokens: {raw_response.eval_count}")
            print(f"Current Tokens / sec: {raw_response.eval_count / (raw_response.eval_duration / 1000000000)}")
            print("\n")
        
        print(f"Min Latentcy for Model: {min_model_latency}")
        print(f"Max Latentcy for Model: {max_model_latency}")
        print(f"Avg Latentcy for Model: {total_model_latency / len(test_prompts)}")
        print("\n")


