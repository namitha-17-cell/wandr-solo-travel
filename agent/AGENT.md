# Use case

- **Pitch:** an AI companion for solo travellers that checks safety, builds itineraries and surfaces local tips — with Strands Decider 2B picking the right tool for every request.
- **Who it is for:** solo travellers planning a trip or already on the road, who want fast, relevant answers without wading through generic travel sites.
- **Features:**
  - solo-travel safety ratings and tips for any destination;
  - day-by-day itinerary builder with budget awareness;
  - real-time local tips (things to do, eat and see right now);
  - live weather for any destination (open-meteo, no key needed);
  - Strands Decider 2B selects the right tool per request so the LLM never wastes a call;
  - a live decision panel in the demo UI that shows which tool was chosen and with what confidence;
  - deployed on Amazon Bedrock AgentCore Runtime.
- **The decision handed to Strands Decider 2B:** before every agent turn, which tool best matches what the traveller is asking? (`#tool-selection`)
- **Why a decision model:** tool selection runs on every request, so it must be fast and cheap; a calibrated confidence score lets the agent fall back gracefully when the request is ambiguous.
- **Amazon Bedrock:** the conversation and tool use (Amazon Nova Pro by default).
