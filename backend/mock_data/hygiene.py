import random
from utils.time_series import current_value, days_until
from utils.alert_engine import evaluate_days


def get_hygiene_data():
    ssl_days = random.randint(8, 60)
    domain_days = random.randint(20, 90)
    backup_age_hours = current_value(base=8, variance=4)
    restore_test_days = random.randint(30, 120)
    disk_forecast_days = random.randint(8, 30)
    vpn_expiry_days = random.randint(3, 20)

    return {
        "items": [
            {
                "name": "SSL Certificate",
                "detail": f"example.com expires in {ssl_days} days",
                "days": ssl_days,
                "status": evaluate_days(ssl_days),
                "expiry_date": days_until(ssl_days)
            },
            {
                "name": "Domain Expiry",
                "detail": f"example.com expires in {domain_days} days",
                "days": domain_days,
                "status": evaluate_days(domain_days, warning_days=45, critical_days=14),
                "expiry_date": days_until(domain_days)
            },
            {
                "name": "Backup Status",
                "detail": "Last backup succeeded" if backup_age_hours < 24 else "Last backup failed",
                "days": None,
                "status": "ok" if backup_age_hours < 24 else "critical",
                "expiry_date": None
            },
            {
                "name": "Backup Restore Verification",
                "detail": f"Last restore test: {restore_test_days} days ago",
                "days": restore_test_days,
                "status": evaluate_days(restore_test_days, warning_days=30, critical_days=90) if restore_test_days > 30 else "ok",
                "expiry_date": None
            },
            {
                "name": "DNS Health",
                "detail": "All DNS records resolving" if random.random() > 0.1 else "DNS resolution failed",
                "days": None,
                "status": "ok" if random.random() > 0.1 else "critical",
                "expiry_date": None
            },
            {
                "name": "NTP Synchronization",
                "detail": "Clock in sync" if random.random() > 0.1 else "Clock drift detected",
                "days": None,
                "status": "ok" if random.random() > 0.1 else "warning",
                "expiry_date": None
            },
            {
                "name": "Disk Forecast",
                "detail": f"Disk full in {disk_forecast_days} days at current growth rate",
                "days": disk_forecast_days,
                "status": evaluate_days(disk_forecast_days, warning_days=21, critical_days=10),
                "expiry_date": days_until(disk_forecast_days)
            },
            {
                "name": "Vendor VPN Access",
                "detail": f"Vendor VPN expires in {vpn_expiry_days} days",
                "days": vpn_expiry_days,
                "status": evaluate_days(vpn_expiry_days, warning_days=14, critical_days=5),
                "expiry_date": days_until(vpn_expiry_days)
            },
            {
                "name": "Kubernetes Version",
                "detail": "v1.26 — end of life, upgrade required" if random.random() > 0.5 else "v1.29 — supported",
                "days": None,
                "status": "critical" if random.random() > 0.5 else "ok",
                "expiry_date": None
            },
            {
                "name": "OS Patch Status",
                "detail": "Critical security updates pending" if random.random() > 0.4 else "All patches applied",
                "days": None,
                "status": "warning" if random.random() > 0.4 else "ok",
                "expiry_date": None
            }
        ]
    }