import random
import time
from datetime import datetime, timedelta


def generate_time_series(points=30, base=50, variance=10, trend=0, spike_chance=0.05):
    """
    Generate a realistic time series with noise, trend, and occasional spikes.
    points       = how many data points
    base         = baseline value
    variance     = how much random noise
    trend        = gradual increase/decrease per point (e.g. 0.5 = slowly rising)
    spike_chance = probability of a sudden spike (0.05 = 5%)
    """
    series = []
    current = base
    now = datetime.utcnow()

    for i in range(points):
        noise = random.uniform(-variance, variance)
        current = current + trend + noise

        if random.random() < spike_chance:
            current += random.uniform(variance * 2, variance * 4)

        current = max(0, current)

        timestamp = now - timedelta(minutes=(points - i))
        series.append({
            "timestamp": timestamp.strftime("%H:%M"),
            "value": round(current, 2)
        })

    return series


def generate_percentage_series(points=30, base=60, variance=8, trend=0):
    """Same as above but clamps between 0 and 100."""
    series = generate_time_series(points, base, variance, trend)
    for point in series:
        point["value"] = min(100, max(0, point["value"]))
    return series


def current_value(base=50, variance=10):
    """Single current reading with small noise."""
    return round(base + random.uniform(-variance, variance), 2)


def current_percentage(base=60, variance=8):
    """Single percentage reading clamped 0-100."""
    val = base + random.uniform(-variance, variance)
    return round(min(100, max(0, val)), 2)


def status(ok_chance=0.85):
    """
    Returns a status string.
    ok_chance = probability of being healthy (0.85 = healthy 85% of the time)
    """
    roll = random.random()
    if roll < ok_chance:
        return "healthy"
    elif roll < ok_chance + 0.10:
        return "warning"
    else:
        return "critical"


def days_until(days):
    """Returns a future date string that is N days from now."""
    future = datetime.utcnow() + timedelta(days=days)
    return future.strftime("%Y-%m-%d")


def random_choice(options):
    return random.choice(options)