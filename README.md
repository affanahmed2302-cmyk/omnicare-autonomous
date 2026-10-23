# OmniCare Autonomous

**Intelligent multi-agent emergency response, family wellness & smart-home caretaking system**

Built for the **Build, Ship, Shape: Amazon Developer Hackathon 2026**

| Track | Status |
|-------|--------|
| **Primary Track** | Alexa+ (Self-hosted MCP Server – Spec 2025-11-25, Streamable HTTP) |
| **Cross-Device** | Ring + Bee + Fire TV |
| **Mini-Challenge** | AWS Builder (Amazon Bedrock + AgentCore patterns + Strands SDK) |

---

## What it does

OmniCare Autonomous turns Alexa+, Ring cameras, Bee wearables and Fire TV into a proactive family safety net for aging-in-place seniors and busy households.

- Continuous biometric + ambient monitoring
- Multi-agent risk evaluation powered by Amazon Bedrock (Claude)
- Instant multi-modal alerts on Fire TV (picture-in-picture dashboard)
- Automated caretaking actions (notify family, log events, escalate)

---

## Architecture

```
┌─────────────────┐     Streamable HTTP      ┌──────────────────────┐
│  Alexa+ / Web   │ ◄──────────────────────► │  OmniCare MCP Server │
│  Simulator      │                          │  (Python / FastAPI)  │
└─────────────────┘                          └──────────┬───────────┘
                                                        │
                    ┌───────────────────────────────────┼───────────────────────────┐
                    │                                   │                           │
             ┌──────▼──────┐                   ┌────────▼────────┐          ┌───────▼───────┐
             │ Amazon      │                   │ Ring Simulator  │          │ Bee Data      │
             │ Bedrock     │                   │ + Event Bridge  │          │ Ingestion     │
             │ (Claude)    │                   └─────────────────┘          └───────────────┘
             └─────────────┘
                    │
             ┌──────▼──────┐
             │ Fire TV     │
             │ Dashboard   │
             └─────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- (Optional) AWS credentials for real Bedrock calls

### 1. Clone & Install
```bash
git clone https://github.com/affanahmed2302-cmyk/omnicare-autonomous.git
cd omnicare-autonomous
pip install -r requirements.txt
```

### 2. Run the MCP Server
```bash
python -m mcp_server.main
```
Server starts at `http://localhost:8000` with Streamable HTTP transport.

### 3. Open the Web Simulator (Alexa+ experience)
Open `web_simulator/index.html` in any browser.  
It acts as a real MCP client (initialize → tools/list → tools/call).

### 4. Fire TV Dashboard Demo
Open `firetv_dashboard/index.html` — this is the multi-modal alert UI that appears on Fire TV / Vega OS style devices.

---

## MCP Tools Exposed

| Tool | Description |
|------|-------------|
| `check_senior_status` | Aggregate Bee biometrics + Ring camera status |
| `evaluate_risk` | Multi-agent risk scoring via Bedrock Claude |
| `trigger_alert` | Push picture-in-picture alert to Fire TV |
| `notify_family` | Send escalation notifications |
| `log_care_event` | Structured caretaking event log |

---

## AWS Builder Mini-Challenge

- **Amazon Bedrock** – Claude model for risk reasoning (`bedrock_client.py`)
- **AgentCore-style orchestration** – Multi-tool agent loop in `agent_orchestrator.py`
- **Strands SDK patterns** – Tool definition & execution following Strands conventions

All integrations are documented and have real runtime calls (with graceful mock fallback when AWS credentials are absent).

---

## Project Structure

```
omnicare-autonomous/
├── mcp_server/                 # Self-hosted MCP server (Alexa+ track)
│   ├── main.py
│   ├── tools.py
│   ├── bedrock_client.py
│   └── agent_orchestrator.py
├── integrations/
│   ├── ring_simulator.py
│   └── bee_ingestion.py
├── firetv_dashboard/           # Multi-modal Fire TV UI
│   └── index.html
├── web_simulator/              # Alexa+ web experience simulator
│   └── index.html
├── docs/
│   ├── PRODUCT_FEEDBACK.md
│   └── FRICTION_LOG.md
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Demo Video

*(Add your YouTube/Vimeo link here after recording a short screen recording of the web simulator + Fire TV dashboard)*

---

## License

MIT License – see [LICENSE](LICENSE)

---

Built with ❤️ for the Amazon Developer Hackathon 2026  
Primary Track: **Alexa+** | Mini-Challenge: **AWS Builder**
