"""
Ring integration simulator.
In production this would call Ring APIs / Developer Playground.
For the hackathon we provide a realistic, deterministic simulator.
"""

from typing import Any, Dict
import random
from datetime import datetime, timezone


def get_ring_status(senior_id: str) -> Dict[str, Any]:
    """Return current Ring camera / perimeter status."""
    # Deterministic-ish for demo stability
    seed = sum(ord(c) for c in senior_id) % 100
    motion = seed > 70
    return {
        "device": "Ring Indoor Cam (Living Room)",
        "online": True,
        "motion_detected": motion,
        "last_motion_at": datetime.now(timezone.utc).isoformat() if motion else None,
        "battery_percent": 87,
        "recording": motion,
        "snapshot_url": "https://example.com/ring-snapshot.jpg",
        "perimeter_secure": not motion,
    }


def trigger_ring_event(event_type: str = "motion") -> Dict[str, Any]:
    return {
        "event": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "ring_simulator",
        "action_taken": "event_logged",
    }
