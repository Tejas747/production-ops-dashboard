import random
from datetime import datetime, timedelta


SEVERITIES = ["P1", "P2", "P3"]
OWNERS = ["alice", "bob", "carol", "dave", "eve"]
SERVICES = ["payment-service", "api-gateway", "auth-service", "order-service", "database"]
TITLES = [
    "Payment gateway latency spike",
    "Auth service returning 503s",
    "Database replication lag critical",
    "API gateway memory leak",
    "Kafka consumer group rebalancing",
    "CDN cache purge failure",
    "Redis eviction rate spike"
]


def get_incidents_data():
    num_incidents = random.randint(2, 6)
    incidents = []

    for i in range(num_incidents):
        opened_minutes_ago = random.randint(5, 480)
        opened_at = datetime.utcnow() - timedelta(minutes=opened_minutes_ago)
        severity = random.choices(SEVERITIES, weights=[10, 40, 50])[0]

        incidents.append({
            "id": f"INC-{1000 + i}",
            "title": random.choice(TITLES),
            "severity": severity,
            "owner": random.choice(OWNERS),
            "service": random.choice(SERVICES),
            "status": random.choice(["investigating", "identified", "monitoring"]),
            "escalated": random.random() > 0.7,
            "opened_at": opened_at.strftime("%H:%M UTC"),
            "duration_minutes": opened_minutes_ago
        })

    incidents.sort(key=lambda x: SEVERITIES.index(x["severity"]))

    return {
        "open_count": len(incidents),
        "p1_count": sum(1 for i in incidents if i["severity"] == "P1"),
        "p2_count": sum(1 for i in incidents if i["severity"] == "P2"),
        "incidents": incidents
    }