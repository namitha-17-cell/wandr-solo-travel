\# Wandr 🌍 — Your AI Companion for Solo Travel



Wandr is an AI-powered travel companion designed to help solo travellers make more informed travel decisions. Built with \*\*Strands Agents\*\* and \*\*Strands Decider 2B\*\*, Wandr selects the tools needed to answer travel questions without relying on a fixed sequence of tool calls.



\## ✨ What Wandr Can Do



\- \*\*Safety information:\*\* Provides destination safety guidance for solo travellers.

\- \*\*Personalised itineraries:\*\* Creates multi-day plans based on destination, trip duration, and budget.

\- \*\*Local tips:\*\* Offers destination-specific suggestions and practical travel advice.

\- \*\*Weather updates:\*\* Retrieves weather information using the Open-Meteo API.



\## 🧠 How It Works



Wandr uses Strands Agents to power the conversational experience and Strands Decider 2B to help select the appropriate tool for each user request.



The available tools cover safety information, itinerary planning, local tips, and weather. The selected tool is then used to help generate a relevant response.



This tool-selection approach allows Wandr to handle different travel questions through a common conversational interface.



\## 🛠️ Built With



\- Python

\- Strands Agents

\- Strands Decider 2B

\- Amazon Bedrock model configuration

\- Open-Meteo API

\- Uvicorn



\## 📊 Decision Benchmark



In the project's 24-case tool-selection benchmark:



| Metric | Strands Decider 2B |

|---|---:|

| Tool-selection accuracy | 91.7% |

| Median decision latency | 1.67 seconds |

| 95th-percentile latency | 1.83 seconds |

| Estimated decision cost | $0.035 per 1,000 decisions |



These are benchmark results for tool selection, not a measure of overall travel-answer accuracy. Results are based on a limited evaluation set and may vary in other settings.



\## 🚀 Running the Project



This project uses the Strands Decider Hackathon Kit.



1\. Clone the repository.

2\. Follow the setup instructions in the kit's getting-started documentation.

3\. Configure your environment variables using `.env.example` as a template.

4\. Keep your actual API keys and `.env` file private.

5\. Start the demo:



&#x20;  ```powershell

&#x20;  .\\kit.cmd demo

&#x20;  ```



6\. Open `http://127.0.0.1:8501` in your browser.



\## ⚠️ Important Notes



\- Safety ratings, budget information, and local tips currently include sample data. They should not be treated as verified, real-time travel intelligence.

\- Weather information is retrieved from Open-Meteo and depends on service availability.

\- Always verify current safety guidance, entry requirements, local restrictions, and weather alerts through authoritative sources before travelling.



\## 🏆 Hackathon



Built for the \*\*Agent Experience Hackathon: Strands Decider\*\*, with the AWS User Group Madurai Strands Decider hackathon kit.



Built with the AWS User Group Madurai Strands Decider hackathon kit.



\## 📄 License



See \[LICENSE](LICENSE).



