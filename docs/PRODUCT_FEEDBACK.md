# Product Feedback – OmniCare Autonomous
Amazon Developer Hackathon 2026

## Feedback Question 1: Which developer tools, APIs, and SDKs did you use and for what?

- **Model Context Protocol (MCP) Spec 2025-11-25** – Core transport and tool surface for the Alexa+ track. Implemented a self-hosted Streamable HTTP server.
- **FastAPI + Uvicorn** – HTTP server that exposes the MCP endpoint.
- **Amazon Bedrock Runtime (boto3)** – Claude 3.5 Sonnet for multi-agent risk evaluation.
- **Strands SDK / AgentCore patterns** – Tool definition schema and agent orchestration loop (check → evaluate → act).
- **Ring Developer concepts / simulator** – Camera status, motion events, perimeter state.
- **Bee wearable data model** – Biometric ingestion layer (heart rate, SpO₂, fall detection flag).
- **Plain HTML/CSS/JS** – Fire TV picture-in-picture dashboard and Alexa+ web simulator (acts as a real MCP client).

## Feedback Question 2: For each tool, API, or SDK used in your project, what worked well?

- **MCP Streamable HTTP** – Once the protocol shape is understood, building a compliant server is straightforward. The initialize → tools/list → tools/call flow is clean.
- **Bedrock invoke_model** – Reliable when credentials are present; response format is predictable.
- **FastAPI** – Excellent for rapid MCP endpoint scaffolding and CORS handling for the web simulator.
- **Local mock fallbacks** – Letting the demo run without AWS credentials made development and judging-friendly demos much easier.

## Feedback Question 3: For each tool, API, or SDK used in your project, what needs work?

- **Alexa+ gated tooling** – No public access to Category SDK / MCP Toolkit / Web Simulator. We had to build our own web-based MCP client. Clearer public documentation that “self-hosted MCP + your own simulator is the expected path” would reduce confusion.
- **Bedrock model IDs and region availability** – Occasional region/model mismatches; better error messages when a model is not enabled in the account would help.
- **Ring & Bee public SDKs** – For a hackathon audience, more ready-to-run simulator packages (or official mock servers) would accelerate integration work.
- **MCP session / auth story** – Spec is flexible but real-world auth and multi-tenant session handling still require significant custom code.

## Feedback Question 4: For each tool, API, or SDK used in your project, how was your onboarding experience?

- **MCP** – Good once you locate the official spec and examples. “Zero to hello-world” took roughly 2–3 hours including reading the Streamable HTTP transport notes.
- **Bedrock** – Familiar if you already know boto3; first successful Claude call was under 30 minutes after setting credentials.
- **Ring / Bee** – Onboarding was mostly design-time (reading docs + building simulators) because physical devices / full API access were not assumed for every participant.

## Feedback Question 5: Would you build with these devices and services again?

**Yes.**  
The combination of a standards-based MCP surface (Alexa+), multi-modal devices (Ring + Bee + Fire TV), and Bedrock for reasoning is extremely powerful for real caretaking and ambient-intelligence products. The main friction is access and documentation consistency across the gated Alexa+ surface; once that is smoothed out, the developer experience becomes compelling for production agentic applications.
