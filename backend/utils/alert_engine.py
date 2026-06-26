def evaluate(value, warning_threshold, critical_threshold, mode="above"):
    """
    Evaluate a metric value against thresholds.
    mode='above'  → alert when value goes above threshold (e.g. CPU, error rate)
    mode='below'  → alert when value goes below threshold (e.g. hit ratio, availability)
    
    Returns: 'critical', 'warning', or 'ok'
    """
    if mode == "above":
        if value >= critical_threshold:
            return "critical"
        elif value >= warning_threshold:
            return "warning"
        else:
            return "ok"
    elif mode == "below":
        if value <= critical_threshold:
            return "critical"
        elif value <= warning_threshold:
            return "warning"
        else:
            return "ok"


def evaluate_days(days_remaining, warning_days=30, critical_days=14):
    """
    For expiry-based checks (SSL certs, domain, backups).
    Alerts when days_remaining is LOW.
    """
    if days_remaining <= critical_days:
        return "critical"
    elif days_remaining <= warning_days:
        return "warning"
    else:
        return "ok"


def badge(status):
    """Returns emoji badge for a status string."""
    return {
        "ok": "✅",
        "warning": "⚠️",
        "critical": "🔴",
        "healthy": "✅",
        "degraded": "⚠️",
        "down": "🔴"
    }.get(status, "❓")