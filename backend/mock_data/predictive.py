import random
from utils.time_series import generate_time_series, current_value, days_until
from utils.alert_engine import evaluate_days


def get_predictive_data():
    disk_fill_days = random.randint(7, 25)
    cert_expiry_days = random.randint(10, 40)
    db_conn_trend = current_value(base=2.5, variance=1)
    cost_overrun_pct = current_value(base=28, variance=15)

    forecasts = [
        {
            "metric": "Disk Storage",
            "prediction": f"Disk will be full in {disk_fill_days} days",
            "days": disk_fill_days,
            "status": evaluate_days(disk_fill_days, warning_days=21, critical_days=10),
            "action": "Increase disk size or clean up old logs"
        },
        {
            "metric": "SSL Certificate",
            "prediction": f"Certificate expires in {cert_expiry_days} days",
            "days": cert_expiry_days,
            "status": evaluate_days(cert_expiry_days),
            "action": "Trigger cert renewal via certbot"
        },
        {
            "metric": "DB Connections",
            "prediction": f"Connections growing at +{round(db_conn_trend, 1)}/min — pool exhaustion in ~4 days",
            "days": 4,
            "status": "warning",
            "action": "Review connection pooling settings or add read replicas"
        },
        {
            "metric": "Cloud Spend",
            "prediction": f"Monthly spend projected {round(cost_overrun_pct, 0)}% over budget",
            "days": None,
            "status": evaluate_days(100 - cost_overrun_pct, warning_days=20, critical_days=5) if cost_overrun_pct > 0 else "ok",
            "action": "Identify and terminate idle EC2 instances"
        }
    ]

    return {
        "forecasts": forecasts,
        "disk_forecast_history": generate_time_series(points=30, base=74, variance=2, trend=0.3),
        "conn_forecast_history": generate_time_series(points=30, base=142, variance=10, trend=2.5)
    }