# Wandr — Requirements

## Overview
Wandr is an AI travel companion for solo travellers. It answers safety questions, builds itineraries, surfaces local tips and fetches live weather — with Strands Decider 2B selecting the right tool before every LLM turn.

## Users
Solo travellers, from first-timers to seasoned backpackers, asking questions before or during a trip.

## Functional requirements

1. **Safety check** — given a destination, return a solo travel safety score (overall, solo female, solo male out of 10) and 5 essential tips.
2. **Itinerary builder** — given a destination, number of days (3 or 5) and budget level, return a day-by-day plan with estimated daily cost in USD.
3. **Local tips** — given a destination, return 5 real-time tips on what to do, eat and see right now.
4. **Live weather** — given a destination, return current conditions and a 3-day forecast from open-meteo (no API key needed).
5. **Tool selection decision** — before every agent turn, Strands Decider 2B reads the request and picks the one best tool. If confidence < 0.6, all tools are kept and the LLM chooses.
6. **Graceful fallback** — for destinations not in the synthetic database, return a helpful message with available destinations.
7. **Direct answers** — for requests that need no tool (packing lists, visa info), the agent answers directly (`none` selection).

## Non-functional requirements
- Works fully offline except for `get_weather` (open-meteo) and the decider API.
- `HackathonAgent.chat` returns `reply`, `decisions`, `model_id`, `latency_ms`.
- Each decision dict contains `tool_selected`, `confidence`, `narrowed`, `probabilities`, `decider_ms`.
- No secrets in code; open-meteo needs no key.
