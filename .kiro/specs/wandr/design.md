# Wandr — Design

## Architecture

```
user message
    │
    ▼
WandrSelector.agent_for(message)
    │  Strands Decider 2B reads the request
    │  choice question: check_safety | build_itinerary | get_local_tips | get_weather | none
    │  confidence ≥ 0.6 → narrow to one tool
    │  confidence < 0.6 → keep all tools, LLM chooses
    ▼
Strands Agent (narrowed tool list, Amazon Bedrock LLM)
    │
    ▼
HackathonAgent.chat → { reply, decisions, model_id, latency_ms }
```

## Components

### agent/tools.py
Four `@tool` functions with clear one-line docstrings (used as decider option descriptions):
- `check_safety(destination)` — synthetic data, 5 destinations
- `build_itinerary(destination, days, budget_level)` — synthetic 3-day and 5-day templates
- `get_local_tips(destination)` — synthetic 5 tips per destination
- `get_weather(destination)` — live open-meteo API call, fallback on error

### agent/decision.py
- `PATTERN_TAG = "#tool-selection"`
- `QUESTIONS` — built from TOOLS via `questions_for(TOOLS)`
- `WandrSelector` — wraps `ToolSelector`, formats log for `decisions` contract

### agent/agent.py
- `NAME`, `SYSTEM_PROMPT`, `HackathonAgent`
- Creates a fresh `WandrSelector` per `chat()` call (stateless tool selection)
- Strips thinking tokens, returns full contract dict

## Data
- Synthetic: 5 destinations (Bangkok, Lisbon, Tokyo, Medellín, Reykjavik) with safety scores, itineraries and local tips in `tools.py`
- Live: open-meteo free API (no key) for weather

## Decision pattern
`ToolSelector` from `decider_kit.patterns.tool_selection`:
- One `choice` question with N+1 options (one per tool + `none`)
- Option descriptions come from tool docstrings — no hardcoding
- `threshold=0.6` — below this, all tools kept
