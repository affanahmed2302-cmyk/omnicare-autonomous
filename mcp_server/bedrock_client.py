"""
Amazon Bedrock client for OmniCare risk evaluation.
Uses Claude via Bedrock Runtime. Falls back to a deterministic mock when
AWS credentials are not present (so the demo always runs).
"""

import json
import os
from typing import Any, Dict

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
    BOTO_AVAILABLE = True
except ImportError:
    BOTO_AVAILABLE = False


async def evaluate_with_bedrock(status_summary: str, context: str = "") -> Dict[str, Any]:
    """
    Call Amazon Bedrock (Claude) to evaluate risk.
    Falls back to a local heuristic if credentials / network are unavailable.
    """
    prompt = f"""You are OmniCare, an expert senior-care risk assessment agent.

Current status:
{status_summary}

Additional context:
{context or "None"}

Respond with a JSON object containing:
- risk_score (0-100)
- risk_level ("low" | "medium" | "high" | "critical")
- reasoning (short paragraph)
- recommended_actions (list of strings)
"""

    if BOTO_AVAILABLE and os.getenv("AWS_ACCESS_KEY_ID"):
        try:
            client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            }
            response = client.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )
            result = json.loads(response["body"].read())
            text = result["content"][0]["text"]
            # Try to parse JSON from the model response
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {
                    "risk_score": 40,
                    "risk_level": "medium",
                    "reasoning": text,
                    "recommended_actions": ["Review status manually"],
                    "source": "bedrock-claude",
                }
        except (BotoCoreError, ClientError, Exception) as e:
            # Fall through to mock
            pass

    # Deterministic mock for zero-setup demo
    try:
        data = json.loads(status_summary) if status_summary.strip().startswith("{") else {}
    except Exception:
        data = {}

    hr = data.get("bee_vitals", {}).get("heart_rate", 75)
    motion = data.get("ring_status", {}).get("motion_detected", False)

    if hr > 130 or (hr < 45 and not motion):
        score, level = 85, "critical"
        actions = ["Trigger Fire TV critical alert", "Notify family immediately", "Log care event"]
    elif hr > 110:
        score, level = 60, "high"
        actions = ["Trigger medium alert on Fire TV", "Notify primary caregiver"]
    elif motion and hr > 95:
        score, level = 35, "medium"
        actions = ["Continue monitoring", "Log event"]
    else:
        score, level = 15, "low"
        actions = ["No action required"]

    return {
        "risk_score": score,
        "risk_level": level,
        "reasoning": f"Heuristic evaluation based on heart rate={hr} and motion={motion}. (Mock mode – supply AWS credentials for live Bedrock Claude evaluation.)",
        "recommended_actions": actions,
        "source": "local-mock",
    }
