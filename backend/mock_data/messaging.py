import random
from utils.time_series import generate_time_series, current_value
from utils.alert_engine import evaluate


TOPICS = [
    "orders.created", "orders.updated", "payments.processed",
    "inventory.updated", "notifications.email", "notifications.sms",
    "analytics.events", "search.index"
]


def get_messaging_data():
    consumer_lag = current_value(base=4200, variance=1500)
    message_backlog = current_value(base=8400, variance=2000)
    dlq_size = current_value(base=23, variance=10)
    producer_failures = current_value(base=2, variance=2)
    throughput = current_value(base=15000, variance=3000)

    topics = []
    for topic in TOPICS:
        lag = current_value(base=500, variance=300)
        topics.append({
            "topic": topic,
            "throughput_per_sec": round(current_value(base=1800, variance=500), 0),
            "consumer_lag": round(lag, 0),
            "lag_status": evaluate(lag, 1000, 5000)
        })

    return {
        "summary": {
            "availability": "online",
            "consumer_lag": round(consumer_lag, 0),
            "lag_status": evaluate(consumer_lag, 10000, 100000),
            "message_backlog": round(message_backlog, 0),
            "dlq_size": round(dlq_size, 0),
            "dlq_status": evaluate(dlq_size, 50, 200),
            "producer_failures": round(producer_failures, 0),
            "throughput_per_sec": round(throughput, 0)
        },
        "lag_history": generate_time_series(points=30, base=4200, variance=1500, trend=20),
        "throughput_history": generate_time_series(points=30, base=15000, variance=3000),
        "dlq_history": generate_time_series(points=30, base=23, variance=10, trend=0.5),
        "topics": topics
    }