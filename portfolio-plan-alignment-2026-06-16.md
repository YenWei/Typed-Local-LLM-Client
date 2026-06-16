# Offline LLM Client - Portfolio Plan Alignment

## Why this note exists
The original offline-LLM plan was written before the handwritten implementation settled. The implementation now works, but some of the original wording should be tightened so the portfolio story reflects reality rather than an earlier assumption.

## What the implementation proves today
- local Ollama host is reachable from the Python client
- the client can ping the server
- the client can generate responses successfully
- responses can be post-processed into extracted JSON
- extracted JSON can be validated against a requested Pydantic output schema
- validation errors can trigger a stricter retry prompt
- benchmark comparison across multiple candidate models has been completed

## What the implementation does not fully prove yet
- explicit support for every originally imagined request parameter in the live Ollama call path
- a mature benchmark utility artifact beyond the recorded benchmark results
- a final portfolio-quality schema better suited than the current `TaskSummary` example

## Recommended wording change for the portfolio story

### Original framing
"Attach schema to the request, receive trusted typed output, and validate it with Pydantic."

### Better current framing
"Use a lightweight client wrapper to generate responses from a local Ollama host, extract structured JSON from the model output, validate it against a requested Pydantic schema, and retry with stricter instructions when the output fails JSON or schema validation."

This stays honest to the current implementation while still telling a strong engineering story.

## Plan adjustments to consider
1. Treat Ollama request-shape limitations as implementation constraints, not failures.
2. Emphasize the reliability layer as:
   - input validation
   - JSON extraction
   - schema-driven validation
   - corrective retry
3. Describe typed output carefully:
   - current state: typed validated payload returned inside `LLMResponse.data`
   - future enhancement: replace `TaskSummary` with a more meaningful showcase schema
4. Treat `benchmark.txt` as legitimate evidence even if `benchmark.py` remains rough.

## Recommended next portfolio decision
Decide which of these two narratives you want:

### Current recommended narrative
Present the system as a practical local LLM reliability wrapper that:
- accepts a request plus an output schema
- validates the response against that schema
- returns the validated typed payload inside `LLMResponse.data`
- retries with stricter instructions when output quality is insufficient

### Optional next upgrade
Replace `TaskSummary` with a more meaningful showcase schema tied to a realistic use case.
