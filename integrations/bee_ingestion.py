"""
Bee wearable data ingestion layer.
In a real deployment this would connect to Bee CLI / MCP / Agent Skills
or an Apple Watch running Bee software.
"""

from typing import Any, Dict
from datetime import datetime, timezone
import random


def get_bee_vitals(senior_id: str) -> Dict[str, Any]:
    """Simulate Bee wearable biometrics for the given senior."""
    # Slight variation based on senior_id for realism
    base = sum(ord(c) for c in senior_id) % 30
    heart_rate = 68 + base
    spo2 = 97 - (base % 3)
    return {
        "device": "Bee Wearable / Apple Watch (Bee)",
        "heart_rate": heart_rate,
        "spo2": spo2,
        "steps_today": 3200 + base * 40,
        "sleep_hours_last_night": 6.5,
        "fall_detected": False,
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "battery_percent": 64,
    }
