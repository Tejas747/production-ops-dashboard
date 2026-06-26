import random
from utils.time_series import (
    generate_time_series,
    current_value,
    days_until
)
from utils.alert_engine import evaluate, evaluate_days


def get_database_data():
    connections = current_value(base=142, variance=30)
    active_queries = current_value(base=28, variance=10)
    slow_queries = random.randint(0, 8)
    query_latency = current_value(base=12, variance=5)
    replication_lag = current_value(base=1.8, variance=1.2)
    deadlocks = random.randint(0, 3)
    lock_waits = random.randint(0, 12)
    storage_gb = current_value(base=384, variance=5)
    storage_growth_gb_day = current_value(base=2.4, variance=0.5)
    backup_age_hours = current_value(base=6, variance=2)

    slow_query_list = []
    sample_queries = [
        "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
        "SELECT p.*, AVG(r.rating) FROM products p JOIN reviews r ON p.id = r.product_id GROUP BY p.id",
        "UPDATE inventory SET stock = stock - ? WHERE product_id = ?",
        "SELECT * FROM analytics_events WHERE timestamp > NOW() - INTERVAL 24 HOURS",
        "SELECT u.*, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id"
    ]
    for query in random.sample(sample_queries, k=slow_queries if slow_queries > 0 else 1):
        slow_query_list.append({
            "query": query[:60] + "...",
            "duration_ms": round(current_value(base=2400, variance=800), 0),
            "calls": random.randint(10, 200)
        })

    return {
        "summary": {
            "availability": "online",
            "connections": round(connections, 0),
            "connections_status": evaluate(connections, 150, 200),
            "active_queries": round(active_queries, 0),
            "slow_queries": slow_queries,
            "slow_queries_status": evaluate(slow_queries, 5, 10),
            "query_latency_ms": round(query_latency, 1),
            "replication_lag_s": round(replication_lag, 2),
            "replication_status": evaluate(replication_lag, 5, 30),
            "deadlocks": deadlocks,
            "lock_waits": lock_waits,
            "storage_gb": round(storage_gb, 1),
            "storage_growth_gb_day": round(storage_growth_gb_day, 2),
            "backup_status": "success" if random.random() > 0.1 else "failed",
            "backup_age_hours": round(backup_age_hours, 1),
            "backup_status_alert": evaluate(backup_age_hours, 24, 48)
        },
        "connections_history": generate_time_series(points=30, base=142, variance=30, trend=0.3),
        "latency_history": generate_time_series(points=30, base=12, variance=5),
        "slow_queries_history": generate_time_series(points=30, base=3, variance=2),
        "slow_query_list": slow_query_list
    }