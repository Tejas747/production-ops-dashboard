import random
from utils.time_series import generate_time_series, current_value


SERVICES = [
    "api-gateway", "auth-service", "order-service",
    "payment-service", "analytics-service", "storage", "networking"
]

TEAMS = ["platform", "backend", "data", "frontend", "devops"]


def get_cost_data():
    daily_cost = current_value(base=1240, variance=150)
    monthly_cost = current_value(base=34800, variance=2000)
    budget_daily = 1100
    budget_monthly = 33000

    services = []
    for svc in SERVICES:
        cost = current_value(base=4800, variance=1500)
        services.append({
            "service": svc,
            "monthly_cost": round(cost, 2),
            "idle_pct": round(random.uniform(5, 35), 1)
        })

    teams = []
    for team in TEAMS:
        cost = current_value(base=6800, variance=2000)
        teams.append({
            "team": team,
            "monthly_cost": round(cost, 2)
        })

    idle_resources = [
        {"resource": "ec2-i-0abc123", "type": "EC2 instance", "waste_per_month": 280},
        {"resource": "rds-snapshot-old", "type": "RDS snapshot", "waste_per_month": 45},
        {"resource": "eip-unused-02", "type": "Elastic IP", "waste_per_month": 12},
        {"resource": "lb-staging-old", "type": "Load balancer", "waste_per_month": 95}
    ]

    return {
        "summary": {
            "daily_cost": round(daily_cost, 2),
            "daily_budget": budget_daily,
            "daily_variance_pct": round((daily_cost - budget_daily) / budget_daily * 100, 1),
            "monthly_cost": round(monthly_cost, 2),
            "monthly_budget": budget_monthly,
            "monthly_variance_pct": round((monthly_cost - budget_monthly) / budget_monthly * 100, 1),
            "idle_waste_monthly": sum(r["waste_per_month"] for r in idle_resources)
        },
        "daily_cost_history": generate_time_series(points=30, base=1240, variance=150),
        "services": services,
        "teams": teams,
        "idle_resources": idle_resources
    }