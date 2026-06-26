import random
from utils.time_series import generate_time_series, generate_percentage_series, current_value, current_percentage
from utils.alert_engine import evaluate


def get_cache_data():
    memory_usage = current_percentage(base=68, variance=10)
    hit_ratio = current_percentage(base=87, variance=5)
    miss_ratio = round(100 - hit_ratio, 2)
    eviction_rate = current_value(base=12, variance=5)
    connections = current_value(base=48, variance=10)

    return {
        "summary": {
            "availability": "online",
            "memory_usage_pct": memory_usage,
            "memory_status": evaluate(memory_usage, 75, 90),
            "hit_ratio_pct": hit_ratio,
            "hit_ratio_status": evaluate(hit_ratio, 80, 60, mode="below"),
            "miss_ratio_pct": miss_ratio,
            "eviction_rate": round(eviction_rate, 1),
            "eviction_status": evaluate(eviction_rate, 20, 50),
            "connections": round(connections, 0),
            "replication_status": "ok" if random.random() > 0.05 else "lagging"
        },
        "memory_history": generate_percentage_series(points=30, base=68, variance=10),
        "hit_ratio_history": generate_percentage_series(points=30, base=87, variance=5),
        "eviction_history": generate_time_series(points=30, base=12, variance=5)
    }