# llm-client

A lightweight Python client for working with a locally hosted LLM through a small, validated interface.

This project was built as foundation work for a larger internal direction: an embedded RAG query system that can serve structured answers to tools, scripts, and internal workflows without depending on a cloud-hosted model.

## Why this exists

Running a local LLM is not the hard part. The harder part is making that model useful for software.

For internal tools, free-form text is often not enough. A tool needs output that is:

- reachable through a simple interface
- structured enough to validate
- reliable enough to retry when formatting breaks
- small and fast enough to run on constrained local hardware

`llm-client` is a focused experiment in that direction.

It provides a small Python wrapper around a local Ollama-served model, validates structured outputs with Pydantic, and establishes the reliability layer needed before a larger embedded RAG system can safely depend on local model outputs.

## What it does

`llm-client` currently supports:

- pinging a local Ollama host
- sending prompts through a minimal client interface
- validating request input with Pydantic
- extracting JSON from model responses
- validating structured output against a requested schema
- retrying with one correction path for invalid JSON and another correction path for schema-validation failure
- benchmarking candidate local models for speed, verbosity, and structured-output friendliness

## Public interface

The intended public surface is intentionally small:

- `ping()`
- `generate_reply(request, output_Type)`

The goal is to keep the interface simple while still supporting typed structured responses through a stable wrapper.

## Design highlights

### 1. Typed structured replies

The client accepts:

- an `LLMRequest`
- an output schema type

It returns:

- `LLMResponse.raw` for the original model output
- `LLMResponse.data` for the validated typed payload

This keeps the debugging path and the trusted structured path separate.

### 2. Validation-first workflow

The response pipeline is designed around validation:

1. send prompt to the local model
2. extract JSON from the raw output
3. validate the extracted JSON against a requested Pydantic schema
4. if JSON extraction fails, retry with a stricter JSON-only correction prompt
5. if schema validation fails, retry with a stricter schema-matching correction prompt
6. return the validated typed payload inside `LLMResponse.data`

That makes the client more useful for automation than a plain chat wrapper.

### 3. Small interface, explicit contracts

The package is centered on a narrow contract rather than an open-ended chatbot abstraction.

That contract is:

- construct a validated request
- call a small client interface
- receive raw output plus a typed validated payload
- fail conservatively when output cannot be trusted

This is the part of the project that matters most for downstream internal tools.

### 4. Benchmarking as support work, not the main product

This package also includes a benchmark script used to compare candidate local models on CPU-only hardware.

The benchmark focused on:

- instruction following
- factual recall
- structured-output format compliance
- latency
- output verbosity

The benchmark exists to help pick a practical default model for the client. It is supporting evidence, not the core abstraction of the package.

## Current benchmark takeaway

The best practical default for this setup was:

- `qwen2.5:7b-instruct-q4_K_M`

It offered the strongest balance of:

- correctness
- structured-output compliance
- acceptable latency
- reasonable output length

A faster alternative existed, but with weaker answer reliability on some prompts.

## What this demonstrates

This project is small on purpose.

It demonstrates several engineering concerns that matter in real AI systems:

- defining a safe interface around a probabilistic model
- validating outputs before tool use
- separating raw output from trusted structured payloads
- retrying differently for different classes of failure
- measuring model usefulness under real hardware constraints
- designing toward an internal system use case, not just a toy chatbot

## Foundation for future work

This package is intended as groundwork for a future embedded RAG query system for an internal tool.

That next step would build on the same principles:

- local or near-local model serving
- retrieval-backed query context
- typed structured answers
- validation before downstream automation
- practical operation on constrained infrastructure

In that sense, `llm-client` is not the end product. It is the reliability layer prototype that informs the next system.

## Tech stack

- Python
- Ollama
- Pydantic
- pytest

## Status

Working prototype.

Implemented:
- request validation
- typed reply validation
- JSON extraction plus schema validation
- distinct retry handling for JSON failure vs schema-validation failure
- benchmark script for local model selection
- unit and integration tests

Planned future improvements:
- stronger showcase schemas than the current example schema
- cleaner benchmark reporting
- tighter packaging and usage examples
- integration into a larger embedded RAG workflow
