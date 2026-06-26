import random
from utils.time_series import generate_time_series, current_value, days_until
from utils.alert_engine import evaluate, evaluate_days


def get_security_data():
    failed_logins = current_value(base=28, variance=15)
    blocked_ips = random.randint(12, 80)
    waf_events = current_value(base=145, variance=60)

    cert_days = random.randint(8, 45)
    secret_days = random.randint(5, 60)
    iam_key_days = random.randint(10, 90)

    open_vulns = random.randint(2, 18)
    critical_cves = random.randint(0, 4)

    return {
        "summary": {
            "failed_logins_per_min": round(failed_logins, 1),
            "failed_login_status": evaluate(failed_logins, 50, 200),
            "blocked_ips": blocked_ips,
            "waf_events_per_hour": round(waf_events, 0),
            "cert_expiry_days": cert_days,
            "cert_status": evaluate_days(cert_days),
            "cert_expiry_date": days_until(cert_days),
            "secret_expiry_days": secret_days,
            "secret_status": evaluate_days(secret_days),
            "iam_key_expiry_days": iam_key_days,
            "iam_status": evaluate_days(iam_key_days),
            "open_vulnerabilities": open_vulns,
            "critical_cves": critical_cves,
            "cve_status": evaluate(critical_cves, 1, 3)
        },
        "failed_login_history": generate_time_series(
            points=30, base=28, variance=15, spike_chance=0.08
        ),
        "waf_history": generate_time_series(points=30, base=145, variance=60)
    }