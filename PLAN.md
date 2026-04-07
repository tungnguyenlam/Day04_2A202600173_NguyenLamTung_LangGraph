# PLAN

## Goal

Build a TravelBuddy agent for the LangGraph lab by implementing the prompt, mock tools, and agent workflow required by [Assignment.md](Assignment.md).

## Deliverables

1. `system_prompt.txt`
2. `tools.py`
3. `agent.py`
4. `test_results.md`
5. Final zip archive for submission

## Phase 0: Environment Setup

1. Add `.env` support for selecting the model provider at runtime.
2. Use `DEFAULT_PROVIDER` as the switch for choosing OpenAI, OpenRouter, Gemini, or Ollama.
3. Define provider-specific variables in separate blocks so the configuration is easy to scan.
4. Keep the model name configurable through the environment for every provider.
5. For local Ollama usage, store the base URL in `.env` instead of hardcoding it.

## Phase 1: Prompt Design

1. Write an XML-style system prompt for a friendly travel assistant.
2. Make the persona specific to Vietnamese travel advice and budget-aware recommendations.
3. Add rules that force Vietnamese responses, travel-only behavior, and clear refusal of off-topic requests.
4. Add tool instructions that describe when to call each tool.
5. Define a strict response format so the agent consistently reports flight, hotel, and estimated total cost.
6. Add constraints that prevent the model from answering unrelated questions such as coding, politics, or finance advice.

## Phase 2: Mock Tools

1. Implement `search_flights(origin, destination)`.
2. Use the provided flight database and format the results in a readable list.
3. Support reverse-route fallback only when the forward route is missing.
4. Implement `search_hotels(city, max_price_per_night)`.
5. Filter by nightly price, sort by rating, and return a clear no-result message when needed.
6. Implement `calculate_budget(total_budget, expenses)`.
7. Parse the expense string, sum the values, calculate the remainder, and warn when the budget is exceeded.
8. Keep all tool outputs stable and easy for the agent to summarize.

## Phase 3: Agent Wiring

1. Create the LangGraph state definition with message history support.
2. Build an agent node that injects the system prompt and calls the LLM with tools bound.
3. Add a provider loader that reads `DEFAULT_PROVIDER` and instantiates the matching client configuration.
4. Add a tools node that executes tool calls returned by the model.
5. Route between the agent and tools until the model stops requesting tool calls.
6. Make sure the graph can support multi-step reasoning such as flight lookup, budget calculation, and hotel selection in one conversation.
7. Add lightweight logging if it helps debug tool usage, routing decisions, and selected provider settings.

## Phase 4: Verification

1. Run an API sanity check before deeper debugging.
2. Test each tool independently with at least one normal case and one edge case.
3. Test at least one multi-step travel request that requires more than one tool.
4. Test an off-topic request and confirm that the agent refuses it.
5. Capture the required console outputs in `test_results.md`.
6. Review the final response format against the assignment’s expected structure.

## Risks To Watch

1. Malformed expense strings may break budget calculations.
2. Missing routes may require careful reverse lookup behavior.
3. Hotel queries with low budgets may return no results and should fail gracefully.
4. Weak prompt wording may let the model answer off-topic requests.
5. The LLM may skip tool use unless the prompt clearly pushes it toward grounded travel advice.
6. Provider-specific setup may fail if environment variables are incomplete or the wrong provider is selected.

## Suggested Work Sequence

1. Draft `system_prompt.txt`.
2. Implement and manually inspect `tools.py`.
3. Build `agent.py` and verify graph flow.
4. Run the assignment test cases.
5. Write `test_results.md` from the actual outputs.
6. Package the finished submission.

## Plan Synchronization

1. Before each coding step, confirm the current plan still matches the assignment and the existing implementation.
2. If the implementation approach changes, update this plan in the same pass so the written steps stay accurate.
3. After each completed task, note the outcome, the next task, and any blockers so another agent can continue without re-reading everything.
4. Treat commit and push as the final step after code, tests, and plan updates are aligned.