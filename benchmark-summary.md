# Benchmark Summary

## Recommendation

**Default model:** `qwen2.5:7b-instruct-q4_K_M`

**Why:** It provided the best overall tradeoff between correctness, structured-output compliance, latency, and output length on a CPU-only spare PC.

**Fast alternative:** `mistral:7b-instruct-q4_K_M`

## Purpose

Evaluate candidate local LLMs for a CPU-only spare PC intended to support tools and scripts.

The goal was not to find the strongest model in abstract, but the most practical model for local tool-serving under constrained hardware.

## Environment

- Local Ollama host over LAN
- CPU-only inference
- No GPU acceleration

## Metrics Collected

- Instruction following
- Stable factual recall
- Modern factual recall
- Structured output format compliance
- Average generated tokens
- Average latency
- Minimum latency
- Maximum latency

## Models Tested

- `qwen2.5:7b-instruct-q4_K_M`
- `mistral:7b-instruct-q4_K_M`
- `llama3.1:8b-instruct-q4_K_M`
- `gemma4:e4b`
- `qwen3:8b`

## Results

### `qwen2.5:7b-instruct-q4_K_M`

- Instruction Following: `PASS`
- Stable Fact Correct: `PASS`
- Modern Fact Correct: `PASS`
- Structured Output Format: `2/2`
- Average Generated Tokens: `19.00`
- Average Latency: `5.25s`
- Min Latency: `0.64s`
- Max Latency: `12.11s`
- Notes: Best overall balance of correctness, structured-output compliance, and practical CPU latency.

### `mistral:7b-instruct-q4_K_M`

- Instruction Following: `PASS`
- Stable Fact Correct: `PASS`
- Modern Fact Correct: `PASS`
- Structured Output Format: `2/2`
- Average Generated Tokens: `17.67`
- Average Latency: `1.12s`
- Min Latency: `0.30s`
- Max Latency: `2.54s`
- Notes: Fastest overall. Structured format compliance was good, but answer quality was weaker on some structured prompts.

### `llama3.1:8b-instruct-q4_K_M`

- Instruction Following: `PASS`
- Stable Fact Correct: `PASS`
- Modern Fact Correct: `PASS`
- Structured Output Format: `2/2`
- Average Generated Tokens: `10.33`
- Average Latency: `4.97s`
- Min Latency: `0.70s`
- Max Latency: `12.72s`
- Notes: Compact normal-prompt outputs and acceptable correctness, but slower first-response behavior than the top practical candidate.

### `gemma4:e4b`

- Instruction Following: `PASS`
- Stable Fact Correct: `PASS`
- Modern Fact Correct: `PASS`
- Structured Output Format: `2/2`
- Average Generated Tokens: `82.00`
- Average Latency: `12.61s`
- Min Latency: `0.76s`
- Max Latency: `25.92s`
- Notes: Strong format compliance and good answers, but latency and verbosity were high for this CPU-only setup.

### `qwen3:8b`

- Instruction Following: `PASS`
- Stable Fact Correct: `PASS`
- Modern Fact Correct: `PASS`
- Structured Output Format: `2/2`
- Average Generated Tokens: `297.33`
- Average Latency: `20.78s`
- Min Latency: `5.96s`
- Max Latency: `28.78s`
- Notes: Correct and compliant, but excessively verbose and too slow for the intended local tool-serving use case.

## Interpretation

- All tested models were capable of passing the simple structured-output format checks.
- Structured-output format success did not automatically guarantee high answer quality.
- On this CPU-only setup, verbosity and latency mattered almost as much as correctness.
- Smaller and more restrained 7B-class models were the most practical fit for local tool-serving.

## Final Takeaway

For this hardware profile, `qwen2.5:7b-instruct-q4_K_M` was the strongest practical default.

It was not the absolute fastest model, but it delivered the most balanced result across correctness, response discipline, and CPU-friendly operation.
