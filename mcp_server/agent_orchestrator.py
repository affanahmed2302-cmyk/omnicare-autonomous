"""
Simple multi-tool agent orchestrator following AgentCore / Strands-style patterns.
Used for end-to-end caretaking workflows.
"""

from typing import Any, Dict, List
from .tools import execute_tool


async def run_agent(senior_id: str, goal: str = "full_status_check") -> Dict[str, Any]:
    """
    Run a short agentic loop:
    1. check_senior_status
    2. evaluate_risk
    3. conditionally trigger_alert / notify_family / log_care_event
    """
    steps: List[Dict[str, Any]] = []

    # Step 1
    status = await execute_tool("check_senior_status", {"senior_id": senior_id})
    steps.append({"tool": "check_senior_status", "result": status})

    # Step 2
    risk = await execute_tool(
        "evaluate_risk",
        {
            "status_summary": str(status),
            "context": f"Goal: {goal}",
        },
    )
    steps.append({"tool": "evaluate_risk", "result": risk})

    # Step 3 – conditional actions
    level = risk.get("risk_level", "low")
    if level in ("high", "critical"):
        alert = await execute_tool(
            "trigger_alert",
            {
                "severity": level,
                "title": f"OmniCare Alert – {level.upper()}",
                "message": risk.get("reasoning", "Elevated risk detected"),
            },
        )
        steps.append({"tool": "trigger_alert", "result": alert})

        notify = await execute_tool(
            "notify_family",
            {
                "senior_id": senior_id,
                "message": f"Risk level {level}: {risk.get('reasoning', '')}",
                "channels": ["push", "sms"],
            },
        )
        steps.append({"tool": "notify_family", "result": notify})

    log = await execute_tool(
        "log_care_event",
        {
            "senior_id": senior_id,
            "event_type": "agent_run",
            "details": f"Completed workflow with risk_level={level}",
        },
    )
    steps.append({"tool": "log_care_event", "result": log})

    return {
        "senior_id": senior_id,
        "goal": goal,
        "final_risk": risk,
        "steps": steps,
    }
