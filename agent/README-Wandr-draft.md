# Wandr — AI Companion for Solo Travellers 🌍

Wandr is an AI travel companion designed to help solo travellers plan trips, explore destinations, check travel safety guidance, and get weather information.

Built using **Strands Agents** and **Strands Decider 2B**, Wandr demonstrates a reusable **tool-selection decision pattern**: the Decider selects the most relevant tool for a traveller's request before the main agent responds.

> Built with the AWS User Group Madurai Strands Decider hackathon kit.

## ✨ Features

- **Solo-travel safety guidance:** Destination-specific tips and indicative safety scores.
- **Itinerary planning:** Day-by-day travel plans for 1–5 days, with estimated budgets.
- **Local recommendations:** Destination-specific activities, food suggestions, and practical tips.
- **Weather forecasts:** Current conditions and a three-day forecast through Open-Meteo.
- **Decision transparency:** A decision log records tool-selection results and confidence information.

## 🧠 How the decision pattern works

Wandr uses the `#tool-selection` pattern.

Before the main agent handles a request, Strands Decider 2B evaluates which tool is most relevant.

The available tools are:

| Tool | Purpose |
|---|---|
| `check_safety` | Retrieve destination safety guidance |
| `build_itinerary` | Generate a day-by-day travel plan |
| `get_local_tips` | Retrieve local recommendations |
| `get_weather` | Retrieve weather and forecast information |

When the selected tool meets the configured confidence threshold, the agent can operate with a narrowed tool set. If confidence is too low, the broader tool set remains available.

This pattern can be adapted to other agents that need to choose between specialised tools.

## 📊 Benchmark results

The current benchmark evaluated 24 labelled cases.

| Metric | Result |
|---|---:|
| Decision-selection accuracy | 91.7% |
| Accuracy on confident decisions | 94.7% |
| Median decision latency (p50) | 2.514 seconds |
| 95th-percentile decision latency (p95) | 7.265 seconds |
| Decisions answered alone at confidence ≥ 0.7 | 79% |
| Reported Decider cost per 1,000 decisions | $0.035 |

These are results from the current evaluation set, not a guarantee of performance on unseen requests. Decision-selection accuracy measures whether the appropriate tool was selected; it does not measure the factual accuracy of the final travel advice.

## 🛠️ Technology stack

- Python
- Strands Agents SDK
- Strands Decider 2B
- Amazon Bedrock, configured for the main language model
- Open-Meteo for weather data
- FastAPI/Uvicorn for the demo server

## 🚀 Run locally

Run these commands from the project root in PowerShell.

**1. Run the tests**

```powershell
.\kit.cmd test
```

**2. Run the benchmark**

```powershell
.\kit.cmd bench
```

**3. Launch the demo**

```powershell
.\kit.cmd demo
```

The demo server should print a local URL, such as `http://127.0.0.1:8501`.

The main agent's Bedrock calls require valid AWS credentials and permission to invoke the configured model. A successful local test run does not, by itself, confirm that live Bedrock chat or AWS deployment works.

## ⚠️ Limitations

- Safety scores and budgets come from a limited sample dataset; they are not verified live ratings or guaranteed prices.
- Local recommendations come from predefined data and may become outdated.
- Weather retrieval requires internet access and can fail if the external service is unavailable.
- Live Amazon Bedrock chat and AWS deployment still require successful account authentication and model access.
- Benchmark results should be interpreted in the context of the 24 evaluated cases.

## 🔮 Future improvements

- Expand destination coverage and validate safety information against reliable sources.
- Improve handling of ambiguous destinations and travel requests.
- Add more evaluation cases and measure end-to-end answer quality.
- Complete AWS deployment and demonstrate the agent running on AWS.
- Publish a narrated demo and the accompanying Builder Center article.

## 🏷️ Hackathon tags

`#strands-decider-2b` `#tool-selection`

## Acknowledgements

Built with the AWS User Group Madurai Strands Decider hackathon kit.

The project uses Strands Agents and Strands Decider. Refer to the repository's licence and dependency licences for applicable terms.
