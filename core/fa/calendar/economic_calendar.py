from datetime import datetime, timedelta


# Known recurring high-impact macro events
HIGH_IMPACT_EVENTS = [
    {
        "name": "FOMC Meeting",
        "severity": "High",
        "impact_window_hours": 6
    },
    {
        "name": "CPI Inflation Data",
        "severity": "High",
        "impact_window_hours": 4
    },
    {
        "name": "US Jobs Report",
        "severity": "High",
        "impact_window_hours": 4
    }
]


def detect_upcoming_events(current_time=None):
    """
    Detect upcoming high-impact economic events.

    NOTE:
    This version uses placeholder scheduling logic and is
    designed to be replaced with a live calendar later.
    """

    if current_time is None:
        current_time = datetime.utcnow()

    upcoming_events = []

    # Placeholder logic: simulate events occurring every Friday
    for event in HIGH_IMPACT_EVENTS:
        next_event_time = current_time + timedelta(hours=3)

        hours_to_event = (next_event_time - current_time).total_seconds() / 3600

        if hours_to_event <= event["impact_window_hours"]:
            upcoming_events.append({
                "upcoming_event": True,
                "event": event["name"],
                "hours_to_event": round(hours_to_event, 2),
                "severity": event["severity"],
                "score": -50,
                "confidence": 1.0,
                "action": "Reduce confidence and widen liquidity range"
            })

    return upcoming_events
