import random
from utils.time_series import generate_time_series, current_value


def get_reliability_data():
    availability = current_value(base=99.94, variance=0.05)
    slo_target = 99.9
    slo_achieved = availability
    error_budget_total = 100 - slo_target
    error_budget_used = max(0, 100 - availability)
    error_budget_remaining_pct = max(0, round(
        (error_budget_total - error_budget_used) / error_budget_total * 100, 1
    ))

    return {
        "summary": {
            "availability_pct": round(availability, 3),
            "slo_target_pct": slo_target,
            "slo_achieved": round(slo_achieved, 3),
            "slo_status": "ok" if slo_achieved >= slo_target else "breached",
            "sla_compliance": "compliant" if availability >= 99.5 else "breached",
            "error_budget_remaining_pct": error_budget_remaining_pct,
            "error_budget_status": "ok" if error_budget_remaining_pct > 25 else "warning" if error_budget_remaining_pct > 10 else "critical",
            "mttr_minutes": round(current_value(base=22, variance=8), 1),
            "mttd_minutes": round(current_value(base=8, variance=3), 1),
            "incident_count_30d": random.randint(3, 12)
        },
        "availability_history": generate_time_series(points=30, base=99.94, variance=0.05),
        "error_budget_history": generate_time_series(points=30, base=error_budget_remaining_pct, variance=5)
    }