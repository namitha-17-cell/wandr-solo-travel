0. This is Wandr, an AI travel companion for solo travellers. It runs on Amazon Bedrock AgentCore Runtime. Before every reply, Strands Decider Two Billion reads the request and picks the right tool — safety check, itinerary builder, local tips or weather — so the agent is fast and focused.

1. A solo travel companion that checks safety, builds itineraries and shares local tips, with Strands Decider choosing the right tool for every request. What it does: Solo travel safety ratings and essential tips for any destination. Day-by-day itinerary builder with budget estimates. Real-time local tips — things to do, eat and see right now. Live weather via open-meteo (no API key needed).

2. A safety question — the decider should pick check_safety. The decider scored confidence 0.90, so the verdict was check_safety, in 1.9 seconds.

3. A planning request — the decider should pick build_itinerary. The decider scored confidence 0.89, so the verdict was build_itinerary, in 1.6 seconds.

4. A real-time local question — the decider should pick get_local_tips. The decider scored confidence 0.41, so the verdict was get_local_tips, in 1.8 seconds.

5. A weather question — the decider should pick get_weather. The decider scored confidence 0.87, so the verdict was get_weather, in 1.9 seconds.

6. On 24 labelled decisions, with the decider on the AWS User Group Madurai hosted API, Strands Decider was 92% accurate at a median of 1667 milliseconds, against 92% and 9374 milliseconds for a hosted open LLM asked the same questions.

7. One forward pass per decision, a calibrated confidence score, and Amazon Bedrock for the conversation — Wandr answers faster and with fewer wasted tool calls.