"""Wandr: AI companion for solo travellers.

Strands Decider 2B picks the right tool for every request (tool selection); Amazon Bedrock
handles the conversation. The demo UI, benchmark and AWS deployment use HackathonAgent.chat.

    from agent.agent import HackathonAgent
    out = HackathonAgent().chat("Is Bangkok safe for a solo female traveller?")
    out["reply"], out["decisions"]
"""

from __future__ import annotations

import time
from typing import Any

from decider_kit import Decider
from decider_kit.llm import agent_model, default_model_id, strip_thinking

from .decision import WandrSelector

NAME = "Wandr — AI companion for solo travellers"

SYSTEM_PROMPT = """You are Wandr, an AI travel companion built for solo travellers.
You help with safety checks, itinerary planning, local tips and live weather.
Be concise, warm and practical. Always tailor advice to solo travel.
If the traveller's destination or request is unclear, ask one focused question."""


class HackathonAgent:
    """One WandrSelector + Strands Agent per session, with tool selection wired in."""

    def __init__(self, decider: Decider | None = None, model_id: str | None = None, eager: bool | None = None):
        import os

        self.decider = decider or Decider()
        self.model_id = model_id or default_model_id()
        # eager is accepted for API compatibility but Wandr does not use an eager mode
        self.eager = eager if eager is not None else os.environ.get("DEMO_EAGER") == "1"

    def chat(self, message: str, session_id: str = "default", images: list[Any] | None = None) -> dict[str, Any]:
        """Send a message to Wandr and return reply + decision log.

        images is accepted for API compatibility but Wandr is text-only.
        """
        selector = WandrSelector(self.decider)
        t0 = time.perf_counter()
        agent = selector.agent_for(
            message,
            model=agent_model(self.model_id),
            system_prompt=SYSTEM_PROMPT,
            callback_handler=None,
        )
        result = agent(message)
        reply = strip_thinking(str(result))

        # Format the selector log to match the expected decisions contract
        decisions = []
        for entry in selector.log:
            probs = entry.get("probabilities", {})
            decisions.append({
                "pattern": "#tool-selection",
                "tool_selected": entry.get("tool"),
                "confidence": entry.get("confidence"),
                "narrowed": entry.get("narrowed"),
                "probabilities": probs,
                "verdict": entry.get("tool"),
                "decider_ms": entry.get("decider_ms"),
            })

        return {
            "reply": reply,
            "decisions": decisions,
            "model_id": self.model_id,
            "latency_ms": round((time.perf_counter() - t0) * 1000),
            "agent": NAME,
            "eager": self.eager,
        }


if __name__ == "__main__":
    import json
    import sys

    a = HackathonAgent()
    messages = sys.argv[1:] or [
        "Is Bangkok safe for a solo female traveller?",
        "Plan me 3 days in Lisbon on a mid budget.",
        "What should I do tonight in Tokyo?",
        "What's the weather like in Reykjavik this week?",
    ]
    for msg in messages:
        print(json.dumps(a.chat(msg), indent=2))
