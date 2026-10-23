# Friction Log – OmniCare Autonomous
Amazon Developer Hackathon 2026  
(These entries are intended to help Amazon engineering teams and may contribute to the up-to-10% judging bonus.)

---

## Friction Entry 1 – Alexa+ Gated Tools vs Public Rules

**Task attempted**  
Build a self-hosted MCP server that could be demonstrated as an Alexa+ experience.

**Steps taken**  
1. Read Official Rules and FAQ stating that Category SDK / MCP Toolkit / Web Simulator are gated.  
2. Confirmed on Resources page that a self-hosted MCP server + own web simulator is the accepted path.  
3. Implemented Streamable HTTP MCP server (spec 2025-11-25) and a browser-based MCP client.

**Expected**  
Clear, single source of truth that says “use self-hosted MCP + your own front-end; no gated tools required.”

**Actual**  
Some individual setup-guide pages still reference the gated tools without the clarifying FAQ language, causing temporary confusion about whether a pure self-hosted approach is sufficient.

**Severity**  
Medium (wasted ~1–2 hours of clarification time).

**Workaround**  
Relied on the official FAQ answer and forum clarification that a web page acting as a real MCP client satisfies the requirement.

**Actionable suggestion**  
Add a prominent call-out on every Alexa+ getting-started page: “Hackathon participants should build a self-hosted MCP server (Streamable HTTP) and demonstrate it with their own web simulator. Gated tools are not required or available.”

---

## Friction Entry 2 – Bedrock Model Availability & Error Clarity

**Task attempted**  
Call Anthropic Claude 3.5 Sonnet via Bedrock Runtime from the risk-evaluation tool.

**Steps taken**  
1. Configured AWS credentials.  
2. Used `bedrock-runtime.invoke_model` with a commonly documented model ID.  
3. Observed AccessDenied or ValidationException in some regions.

**Expected**  
Clear error message indicating “model not enabled in this region/account – enable it in the Bedrock console.”

**Actual**  
Generic AccessDenied / ValidationException that required cross-referencing documentation and console screens to diagnose.

**Severity**  
Medium.

**Workaround**  
Implemented a deterministic local mock that activates when credentials are missing or the call fails, so the demo remains fully runnable for judges.

**Actionable suggestion**  
Surface a more specific error (or a direct console deep-link) when a requested model is not enabled for the calling account/region.

---

## Friction Entry 3 – Ring / Bee Simulator Expectations

**Task attempted**  
Integrate Ring camera status and Bee biometric data without requiring physical hardware for every team member.

**Steps taken**  
1. Reviewed Ring developer documentation and Bee CLI / MCP mentions.  
2. Built lightweight, deterministic simulators that match the data shapes expected by the agent.

**Expected**  
Official or community “hackathon-ready” mock servers / Docker images that emit realistic events.

**Actual**  
Had to design the simulator contracts ourselves. This is fine for a strong team but adds overhead for newcomers.

**Severity**  
Low–Medium.

**Workaround**  
Shipped `integrations/ring_simulator.py` and `integrations/bee_ingestion.py` with stable, documented response shapes.

**Actionable suggestion**  
Provide a small official “Device Simulators” package (or GitHub template) that emits Ring motion events and Bee vital streams over HTTP/MCP so hackathon participants can focus on the agentic logic.

---

## Friction Entry 4 – Fire TV / Vega OS Demo Path for Web Technologies

**Task attempted**  
Deliver a demo-ready multi-modal alert UI suitable for Fire TV / Vega OS.

**Steps taken**  
Created a pure HTML/CSS/JS picture-in-picture style dashboard that can be loaded on a device or shown in a browser as the visual component of the submission.

**Expected**  
Clear guidance on the lightest acceptable path for a web-technology Fire TV submission (e.g., “hosted web app + screen recording of the UI is sufficient for demo”).

**Actual**  
Documentation is strong for React Native / native paths; the pure web path required some inference.

**Severity**  
Low.

**Workaround**  
Shipped `firetv_dashboard/index.html` as a self-contained, visually complete alert surface.

**Actionable suggestion**  
Add a short “Web technologies on Fire TV – minimum viable demo” section with an example of a hosted page + screen-recording checklist.
