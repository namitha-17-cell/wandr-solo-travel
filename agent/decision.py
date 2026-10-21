"""REUSABLE DECISION PATTERN: solo-travel tool selection  (#tool-selection)

What it does
    Before every Wandr agent turn, Strands Decider 2B reads the traveller's request and picks
    the one tool most likely to answer it:
    - check_safety    → safety ratings and essential tips for a destination
    - build_itinerary → day-by-day plans with budget estimates
    - get_local_tips  → things to do, eat and see right now
    - get_weather     → live 3-day forecast
    - none            → the agent can answer directly (e.g. packing list, visa info)
    When the decider is confident (≥ 0.6) it hands the agent only that tool, cutting token
    use and wrong-tool calls. Below the threshold every tool is kept and the LLM chooses.

Typed questions and options
    `tool` (choice): one option per tool, labelled by its one-line docstring, plus `none`.
    Built dynamically from TOOLS by `questions_for` in decider_kit.patterns.tool_selection —
    no retraining needed when a tool is added.

Wiring
    `WandrSelector` wraps `ToolSelector` and is called in `HackathonAgent.chat` before
    the Strands Agent is created for each turn:

        selector = WandrSelector(decider)
        agent = selector.agent_for(message, model=agent_model(), system_prompt=SYSTEM_PROMPT,
                                   callback_handler=None)
        result = agent(message)

    The selection log (`selector.log`) is forwarded to the `decisions` list in the chat
    response so the demo UI and the benchmark can inspect it.

How to reuse it
    Copy this file, replace TOOLS with your own list of Strands @tool functions, and adjust
    the threshold if needed. Every tool needs a clear one-line docstring — that becomes the
    option description the decider reads.
"""

from __future__ import annotations

from typing import Any

from decider_kit import Decider
from decider_kit.patterns.tool_selection import ToolSelector, questions_for

from .tools import TOOLS

PATTERN_TAG = "#tool-selection"

# Re-export so the benchmark can read QUESTIONS without importing tools
QUESTIONS = questions_for(TOOLS)


class WandrSelector:
    """Thin wrapper around ToolSelector that formats the log for HackathonAgent."""

    def __init__(self, decider: Decider, threshold: float = 0.6):
        self._selector = ToolSelector(
            decider,
            tools=TOOLS,
            threshold=threshold,
            context="The user is a solo traveller asking about a destination.",
        )

    @property
    def log(self) -> list[dict[str, Any]]:
        return self._selector.log

    def agent_for(self, request: str, **agent_kwargs: Any) -> Any:
        """Return a Strands Agent narrowed to the best tool for this request."""
        return self._selector.agent_for(request, **agent_kwargs)
