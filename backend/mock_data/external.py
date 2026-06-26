import random
from utils.time_series import generate_time_series, current_value


VENDORS = [
    {"name": "Payment Gateway", "key": "payment"},
    {"name": "Email Service", "key": "email"},
    {"name": "SMS Provider", "key": "sms"},
    {"name": "CDN", "key": "cdn"},
    {"name": "Maps API", "key": "maps"},
    {"name": "Auth0", "key": "auth0"}
]


def get_external_data():
    vendors = []
    for vendor in VENDORS:
        latency = current_value(base=180, variance=60)
        roll = random.random()
        if roll > 0.90:
            vstatus = "down"
        elif roll > 0.75:
            vstatus = "degraded"
        else:
            vstatus = "operational"

        vendors.append({
            "name": vendor["name"],
            "status": vstatus,
            "latency_ms": round(latency, 1),
            "uptime_pct": round(current_value(base=99.5, variance=0.4), 2)
        })

    payment = next(v for v in vendors if v["name"] == "Payment Gateway")

    return {
        "vendors": vendors,
        "payment_latency_history": generate_time_series(
            points=30, base=180, variance=60,
            spike_chance=0.1
        ),
        "summary": {
            "total": len(vendors),
            "operational": sum(1 for v in vendors if v["status"] == "operational"),
            "degraded": sum(1 for v in vendors if v["status"] == "degraded"),
            "down": sum(1 for v in vendors if v["status"] == "down"),
            "payment_status": payment["status"]
        }
    }