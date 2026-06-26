import random
from utils.time_series import (
    generate_percentage_series,
    generate_time_series,
    current_percentage,
    current_value,
    status
)
from utils.alert_engine import evaluate


NODES = [
    "node-01", "node-02", "node-03", "node-04", "node-05"
]

PODS = [
    "api-gateway", "auth-service", "user-service", "order-service",
    "payment-service", "notification-service", "inventory-service",
    "search-service", "recommendation-service", "analytics-service",
    "shipping-service", "cart-service", "product-service", "review-service",
    "email-service", "sms-service", "cdn-service", "config-service",
    "logging-service", "monitoring-service"
]


def get_infrastructure_data():
    cpu = current_percentage(base=62, variance=12)
    memory = current_percentage(base=71, variance=8)
    disk = current_percentage(base=74, variance=5)

    nodes = []
    for node in NODES:
        cpu_val = current_percentage(base=60, variance=15)
        mem_val = current_percentage(base=70, variance=10)
        nodes.append({
            "name": node,
            "cpu": cpu_val,
            "memory": mem_val,
            "cpu_status": evaluate(cpu_val, 70, 85),
            "memory_status": evaluate(mem_val, 75, 90),
            "availability": "online" if random.random() > 0.05 else "offline"
        })

    pods = []
    for pod in PODS:
        restarts = random.choices([0, 1, 2, 5, 12], weights=[70, 15, 8, 5, 2])[0]
        pod_status = "running"
        if restarts >= 5:
            pod_status = "crashloopbackoff"
        elif restarts >= 2:
            pod_status = "warning"

        pods.append({
            "name": pod,
            "status": pod_status,
            "restarts": restarts,
            "cpu": current_percentage(base=45, variance=20),
            "memory": current_percentage(base=55, variance=15)
        })

    disk_iops = current_value(base=3200, variance=400)
    disk_latency = current_value(base=4.2, variance=1.5)
    network_throughput = current_value(base=850, variance=120)
    network_errors = current_value(base=0.3, variance=0.2)
    load_average = current_value(base=2.8, variance=0.8)
    container_restarts = sum(p["restarts"] for p in pods)
    autoscaling_events = random.randint(0, 5)

    return {
        "summary": {
            "cpu": cpu,
            "cpu_status": evaluate(cpu, 70, 85),
            "memory": memory,
            "memory_status": evaluate(memory, 75, 90),
            "disk": disk,
            "disk_status": evaluate(disk, 75, 85),
            "disk_iops": round(disk_iops, 0),
            "disk_latency_ms": round(disk_latency, 2),
            "network_throughput_mbps": round(network_throughput, 1),
            "network_errors": round(network_errors, 3),
            "load_average": round(load_average, 2),
            "container_restarts": container_restarts,
            "autoscaling_events": autoscaling_events,
            "nodes_online": sum(1 for n in nodes if n["availability"] == "online"),
            "nodes_total": len(nodes),
            "pods_running": sum(1 for p in pods if p["status"] == "running"),
            "pods_total": len(pods)
        },
        "cpu_history": generate_percentage_series(points=30, base=62, variance=12),
        "memory_history": generate_percentage_series(points=30, base=71, variance=8),
        "disk_history": generate_percentage_series(points=30, base=74, variance=3, trend=0.1),
        "network_history": generate_time_series(points=30, base=850, variance=120),
        "nodes": nodes,
        "pods": pods
    }