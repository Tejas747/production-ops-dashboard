import random
from utils.time_series import (
    generate_time_series,
    generate_percentage_series,
    current_value,
    current_percentage
)
from utils.alert_engine import evaluate


SLOW_ENDPOINTS = [
    "/api/checkout",
    "/api/search",
    "/api/recommendations",
    "/api/orders/history",
    "/api/reports/sales"
]

SERVICES = [
    "api-gateway", "auth-service", "payment-service",
    "inventory-service", "notification-service"
]


def get_application_data():
    rps = current_value(base=1200, variance=200)
    p50 = current_value(base=45, variance=10)
    p95 = current_value(base=180, variance=40)
    p99 = current_value(base=420, variance=80)
    error_rate = current_value(base=0.8, variance=0.5)
    http_4xx = current_value(base=24, variance=8)
    http_5xx = current_value(base=6, variance=4)
    success_pct = round(100 - error_rate, 2)

    slow_endpoints = []
    for endpoint in random.sample(SLOW_ENDPOINTS, k=3):
        latency = current_value(base=800, variance=300)
        slow_endpoints.append({
            "endpoint": endpoint,
            "latency_ms": round(latency, 1),
            "status": evaluate(latency, 500, 1000)
        })

    dependency_failures = []
    for svc in SERVICES:
        if random.random() < 0.15:
            dependency_failures.append({
                "service": svc,
                "error": random.choice([
                    "connection timeout",
                    "503 service unavailable",
                    "circuit breaker open"
                ])
            })

    return {
        "summary": {
            "rps": round(rps, 1),
            "p50_ms": round(p50, 1),
            "p95_ms": round(p95, 1),
            "p99_ms": round(p99, 1),
            "p95_status": evaluate(p95, 500, 1000),
            "p99_status": evaluate(p99, 800, 1500),
            "error_rate_pct": round(error_rate, 2),
            "error_status": evaluate(error_rate, 1, 5),
            "http_4xx": round(http_4xx, 0),
            "http_5xx": round(http_5xx, 0),
            "api_success_pct": success_pct
        },
        "rps_history": generate_time_series(points=30, base=1200, variance=200),
        "latency_history": generate_time_series(points=30, base=180, variance=40),
        "error_rate_history": generate_time_series(points=30, base=0.8, variance=0.5),
        "slow_endpoints": slow_endpoints,
        "dependency_failures": dependency_failures
    }