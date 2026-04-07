# AGENTS.md

## Purpose

This workspace contains a LangGraph lab for building a travel-planning agent named TravelBuddy. Treat [Assignment.md](Assignment.md) as the source of truth for requirements and deliverables.

## What To Build

The assignment expects these artifacts:

1. `system_prompt.txt` with an XML-style prompt structure.
2. `tools.py` with three mock tools: `search_flights`, `search_hotels`, and `calculate_budget`.
3. `agent.py` with a LangGraph-based agent that can chain tools.
4. `test_results.md` containing evidence from the required test cases.
5. A final zip export named according to the assignment rules.

## Working Rules

1. Read the assignment before making changes.
2. Keep all user-facing behavior in Vietnamese unless the task explicitly requires otherwise.
3. Use mock data only; do not introduce external API calls.
4. Prefer deterministic logic and human-readable tool outputs.
5. Preserve the assignment’s expected file structure and naming.
6. Make the agent useful for travel planning, not a generic chatbot.

## Model Provider Configuration

1. Choose the model provider through `.env`, not by hardcoding it in source files.
2. Use `DEFAULT_PROVIDER` to select the active provider.
3. Support these provider sections in `.env`:
	- `OPENAI_MODEL`, `OPENAI_API_KEY`
	- `OPENROUTER_MODEL`, `OPENROUTER_API_KEY`
	- `GEMINI_MODEL`, `GEMINI_API_KEY`
	- `OLLAMA_MODEL`, `OLLAMA_BASE_URL`
4. Keep provider-specific settings grouped together in the environment file so users can switch providers without editing Python code.
5. Read the selected provider from `.env` at runtime and build the LLM client from that configuration.
6. Treat OpenRouter as the default provider unless the assignment or local environment says otherwise.

## Implementation Order

1. Finish the system prompt first.
2. Implement the tools next and verify their output formatting.
3. Wire the LangGraph agent after the tools are stable.
4. Run the assignment test cases and capture output.
5. Polish any prompt or routing issues only after the end-to-end flow works.

## Tool And Prompt Expectations

1. The system prompt must define persona, rules, tool usage, response format, and constraints.
2. `search_flights` should look up routes in the mock database and handle missing routes gracefully.
3. `search_hotels` should filter by city and maximum nightly price, then sort results by rating.
4. `calculate_budget` should parse expense strings, sum costs, and warn when the budget is exceeded.
5. The agent should combine flight, hotel, and budget information into one coherent travel recommendation.

## Quality Checks

1. Confirm that money values use Vietnamese formatting with dot separators and `đ`.
2. Confirm that off-topic requests are rejected cleanly.
3. Confirm that the agent can do multi-step tool chaining without manual orchestration.
4. Confirm that the required test scenarios are documented in `test_results.md`.
5. Confirm that the final answer format matches the assignment’s travel recommendation structure.

## Guardrails

1. Do not use random or unstable outputs in the tools.
2. Do not hide errors silently; return a clear message when input is malformed.
3. Do not broaden the scope beyond travel planning, budgeting, and booking.
4. Do not rewrite the assignment requirements unless the code clearly needs a small clarification in comments or docs.
5. Do not add unrelated features that make the lab harder to review.

## Workflow Discipline

1. Read the active instruction set and the current plan before changing code.
2. Check what has already been done and identify the next task before writing new implementation.
3. Implement only the next task, then validate that it works as expected.
4. Record what changed and any handoff notes in a log or plan update so another agent can resume if needed.
5. If the plan changes during implementation, update this workspace plan immediately so it stays consistent with the code.
6. When the task is complete and a commit is requested, commit the work and push it only after the code and plan are in sync.