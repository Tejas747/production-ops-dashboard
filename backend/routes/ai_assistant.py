import json
from flask import Blueprint, jsonify, request
from mock_data.infrastructure import get_infrastructure_data
from mock_data.application import get_application_data
from mock_data.database import get_database_data
from mock_data.cache import get_cache_data
from mock_data.messaging import get_messaging_data
from mock_data.external import get_external_data
from mock_data.incidents import get_incidents_data
from mock_data.reliability import get_reliability_data
from mock_data.cost import get_cost_data
from mock_data.hygiene import get_hygiene_data
from mock_data.predictive import get_predictive_data
from mock_data.security import get_security_data

ai_bp = Blueprint("ai", __name__)


def get_full_snapshot():
    return {
        "infrastructure": get_infrastructure_data()["summary"],
        "application": get_application_data()["summary"],
        "database": get_database_data()["summary"],
        "cache": get_cache_data()["summary"],
        "messaging": get_messaging_data()["summary"],
        "external": get_external_data(),
        "reliability": get_reliability_data()["summary"],
        "cost": get_cost_data()["summary"],
        "hygiene": get_hygiene_data()["items"],
        "predictive": get_predictive_data()["forecasts"],
        "security": get_security_data()["summary"],
        "incidents": get_incidents_data()
    }


def analyze(question, snap):
    q = question.lower()
    infra = snap["infrastructure"]
    app = snap["application"]
    db = snap["database"]
    cache = snap["cache"]
    kafka = snap["messaging"]
    ext = snap["external"]
    rel = snap["reliability"]
    cost = snap["cost"]
    hygiene = snap["hygiene"]
    predictive = snap["predictive"]
    sec = snap["security"]
    incidents = snap["incidents"]

    # ── helpers ──────────────────────────────────────────
    def status_label(s):
        if s in ("ok", "healthy", "online", "operational", "running", "success", "compliant"):
            return "healthy"
        if s in ("warning", "degraded", "warn", "lagging"):
            return "degraded"
        return "critical"

    def vendor_issues():
        issues = []
        for v in ext.get("vendors", []):
            if v["status"] != "operational":
                issues.append(f"{v['name']} is {v['status']} ({v['latency_ms']}ms)")
        return issues

    def hygiene_issues():
        return [h for h in hygiene if h["status"] in ("warning", "critical")]

    def forecast_issues():
        return [f for f in predictive if f["status"] in ("warning", "critical")]

    def open_p1():
        return [i for i in incidents.get("incidents", []) if i["severity"] == "P1"]

    # ── CHECKOUT / PAYMENT ───────────────────────────────
    if any(w in q for w in ["checkout", "payment", "paying", "purchase", "order"]):
        issues = []
        cause = []
        actions = []

        payment_vendor = next(
            (v for v in ext.get("vendors", []) if "payment" in v["name"].lower()), None
        )
        if payment_vendor:
            if payment_vendor["status"] != "operational":
                issues.append(
                    f"Payment gateway is {payment_vendor['status']} "
                    f"with latency at {payment_vendor['latency_ms']}ms"
                )
                cause.append("third-party payment gateway degradation")
                actions.append("check payment provider status page and enable fallback gateway")

        if app["error_rate_pct"] > 1:
            issues.append(f"API error rate is elevated at {app['error_rate_pct']}%")
            cause.append("elevated application error rate")
            actions.append("review 5xx logs on order-service and payment-service")

        if app["p99_ms"] > 800:
            issues.append(f"P99 latency is {app['p99_ms']}ms — users are experiencing slow responses")
            cause.append("high tail latency on checkout flow")
            actions.append("check payment-service pod CPU and memory limits")

        if kafka["consumer_lag"] > 10000:
            issues.append(
                f"Kafka consumer lag is {kafka['consumer_lag']:,} — "
                f"order events may be delayed"
            )
            cause.append("Kafka consumer falling behind")
            actions.append("scale up order-consumer replicas")

        if not issues:
            return {
                "summary": "Checkout appears healthy based on current metrics.",
                "observed": [
                    f"Payment gateway: operational",
                    f"Error rate: {app['error_rate_pct']}%",
                    f"P99 latency: {app['p99_ms']}ms"
                ],
                "likely_cause": "No issues detected in checkout flow right now.",
                "recommended_action": "Continue monitoring — no immediate action required."
            }

        return {
            "summary": f"Checkout is degraded. {len(issues)} issue(s) detected.",
            "observed": issues,
            "likely_cause": "Most likely caused by " + " and ".join(cause) + ".",
            "recommended_action": " | ".join(actions)
        }

    # ── LATENCY ──────────────────────────────────────────
    if any(w in q for w in ["latency", "slow", "response time", "fast", "speed"]):
        issues = []
        cause = []
        actions = []

        if app["p95_ms"] > 500:
            issues.append(f"P95 latency is {app['p95_ms']}ms — above 500ms warning threshold")
            cause.append("high P95 latency")
        if app["p99_ms"] > 800:
            issues.append(f"P99 latency is {app['p99_ms']}ms — worst 1% of users badly affected")
            cause.append("high P99 tail latency")
        if infra["cpu"] > 70:
            issues.append(f"CPU is at {infra['cpu']}% — server under pressure")
            cause.append("CPU saturation slowing request processing")
            actions.append("check if autoscaling has triggered — current events: " + str(infra["autoscaling_events"]))
        if cache["hit_ratio_pct"] < 80:
            issues.append(
                f"Redis hit ratio is {cache['hit_ratio_pct']}% — "
                f"cache misses forcing database queries"
            )
            cause.append("low cache hit ratio increasing database load")
            actions.append("review cache TTL settings and warm up frequently accessed keys")
        if db["query_latency_ms"] > 20:
            issues.append(f"Database query latency is {db['query_latency_ms']}ms")
            cause.append("slow database queries contributing to response time")
            actions.append(f"review {db['slow_queries']} slow queries in the database section")

        if not issues:
            return {
                "summary": "Latency looks healthy across all layers.",
                "observed": [
                    f"P50: {app['p50_ms']}ms",
                    f"P95: {app['p95_ms']}ms",
                    f"P99: {app['p99_ms']}ms"
                ],
                "likely_cause": "All latency metrics within acceptable thresholds.",
                "recommended_action": "No action required."
            }

        return {
            "summary": f"Latency is elevated. Root cause spans {len(cause)} layer(s).",
            "observed": issues,
            "likely_cause": "Likely caused by " + ", ".join(cause) + ".",
            "recommended_action": " | ".join(actions) if actions else "Scale application pods and review slow query logs."
        }

    # ── DATABASE ─────────────────────────────────────────
    if any(w in q for w in ["database", "db", "postgres", "postgresql", "query", "queries", "replication"]):
        issues = []
        cause = []
        actions = []

        if db["connections"] > 150:
            issues.append(
                f"Connection count is {db['connections']} — "
                f"approaching PostgreSQL max_connections limit of 200"
            )
            cause.append("connection pool nearing exhaustion")
            actions.append("enable PgBouncer connection pooling or increase max_connections")

        if db["slow_queries"] > 5:
            issues.append(f"{db['slow_queries']} slow queries detected — check slow query log")
            cause.append("unoptimized queries blocking connection slots")
            actions.append("run EXPLAIN ANALYZE on the slowest queries")

        if db["replication_lag_s"] > 5:
            issues.append(
                f"Replication lag is {db['replication_lag_s']}s — "
                f"replica is falling behind primary"
            )
            cause.append("replication lag increasing data loss risk on failover")
            actions.append("check replica I/O and network bandwidth")

        if db["deadlocks"] > 0:
            issues.append(f"{db['deadlocks']} deadlock(s) detected in the last hour")
            cause.append("deadlocks indicate application-level transaction ordering bug")
            actions.append("review transaction ordering in order-service and inventory-service")

        if db["backup_status"] == "failed":
            issues.append("Last database backup failed — RPO is at risk")
            cause.append("backup failure")
            actions.append("trigger manual backup immediately and check storage capacity")

        storage_days = round(
            (1000 - db["storage_gb"]) / db["storage_growth_gb_day"]
        ) if db.get("storage_growth_gb_day", 0) > 0 else 999

        if storage_days < 14:
            issues.append(
                f"At current growth rate of {db.get('storage_growth_gb_day', 0)} GB/day, "
                f"storage will be full in ~{storage_days} days"
            )
            cause.append("storage growth rate")
            actions.append("expand database volume or archive old records")

        if not issues:
            return {
                "summary": "Database is healthy across all monitored parameters.",
                "observed": [
                    f"Connections: {db['connections']} / 200",
                    f"Replication lag: {db['replication_lag_s']}s",
                    f"Slow queries: {db['slow_queries']}",
                    f"Backup: {db['backup_status']}"
                ],
                "likely_cause": "No database issues detected.",
                "recommended_action": "Continue monitoring. Next backup check in 24 hours."
            }

        return {
            "summary": f"Database has {len(issues)} issue(s) requiring attention.",
            "observed": issues,
            "likely_cause": "Issues span: " + ", ".join(cause) + ".",
            "recommended_action": " | ".join(actions)
        }

    # ── REDIS / CACHE ────────────────────────────────────
    if any(w in q for w in ["redis", "cache", "hit ratio", "eviction", "bottleneck"]):
        issues = []
        cause = []
        actions = []

        if cache["memory_usage_pct"] > 75:
            issues.append(f"Redis memory usage is {cache['memory_usage_pct']}%")
            cause.append("high memory usage approaching eviction threshold")
            actions.append("increase Redis maxmemory or evict stale keys")

        if cache["hit_ratio_pct"] < 80:
            issues.append(
                f"Cache hit ratio is {cache['hit_ratio_pct']}% — "
                f"target is above 80%"
            )
            cause.append("low hit ratio pushing extra load onto PostgreSQL")
            actions.append("review cache key TTL and warming strategy")

        if cache["eviction_rate"] > 20:
            issues.append(
                f"Eviction rate is {cache['eviction_rate']} keys/sec — "
                f"Redis is actively discarding data"
            )
            cause.append("memory pressure causing key evictions")
            actions.append("scale Redis memory or reduce key expiry time")

        if cache["replication_status"] != "ok":
            issues.append(f"Redis replication is {cache['replication_status']}")
            cause.append("replication issue")
            actions.append("check replica connectivity and replication offset")

        if not issues:
            return {
                "summary": "Redis is healthy. No bottleneck detected.",
                "observed": [
                    f"Hit ratio: {cache['hit_ratio_pct']}%",
                    f"Memory usage: {cache['memory_usage_pct']}%",
                    f"Eviction rate: {cache['eviction_rate']}/s"
                ],
                "likely_cause": "Cache is performing well within thresholds.",
                "recommended_action": "No action required."
            }

        return {
            "summary": f"Redis has {len(issues)} issue(s) — may become a bottleneck.",
            "observed": issues,
            "likely_cause": ", ".join(cause) + ".",
            "recommended_action": " | ".join(actions)
        }

    # ── KAFKA / MESSAGING ────────────────────────────────
    if any(w in q for w in ["kafka", "messaging", "consumer", "lag", "queue", "dlq", "async"]):
        issues = []
        cause = []
        actions = []

        if kafka["consumer_lag"] > 10000:
            issues.append(
                f"Consumer lag is {kafka['consumer_lag']:,} messages — "
                f"critical threshold is 100,000"
            )
            cause.append("consumers cannot keep up with producers")
            actions.append("scale consumer group replicas for lagging topics")

        if kafka["dlq_size"] > 50:
            issues.append(
                f"Dead letter queue has {kafka['dlq_size']} messages — "
                f"these are permanently failed events"
            )
            cause.append("message processing failures landing in DLQ")
            actions.append("inspect DLQ messages and fix the processing bug causing failures")

        if kafka["producer_failures"] > 5:
            issues.append(f"{kafka['producer_failures']} producer failures detected")
            cause.append("producers failing to write events")
            actions.append("check broker connectivity and disk space on Kafka nodes")

        if not issues:
            return {
                "summary": "Kafka messaging systems are healthy.",
                "observed": [
                    f"Consumer lag: {kafka['consumer_lag']:,}",
                    f"DLQ size: {kafka['dlq_size']}",
                    f"Throughput: {kafka['throughput_per_sec']:,}/sec"
                ],
                "likely_cause": "Async systems operating within normal parameters.",
                "recommended_action": "No action required."
            }

        return {
            "summary": f"Kafka has {len(issues)} issue(s). Async systems are degraded.",
            "observed": issues,
            "likely_cause": ", ".join(cause) + ".",
            "recommended_action": " | ".join(actions)
        }

    # ── SECURITY ─────────────────────────────────────────
    if any(w in q for w in ["security", "login", "attack", "cve", "vulnerability", "certificate", "cert", "ssl"]):
        issues = []
        cause = []
        actions = []

        if sec["failed_logins_per_min"] > 50:
            issues.append(
                f"Failed logins at {sec['failed_logins_per_min']}/min — "
                f"possible brute force attack"
            )
            cause.append("credential stuffing or brute force")
            actions.append(f"review blocked IPs list — currently {sec['blocked_ips']} IPs blocked")

        if sec["critical_cves"] > 0:
            issues.append(f"{sec['critical_cves']} critical CVEs unpatched (CVSS 9+)")
            cause.append("unpatched vulnerabilities")
            actions.append("apply security patches immediately — check OS patch status")

        if sec["cert_expiry_days"] < 30:
            issues.append(f"SSL certificate expires in {sec['cert_expiry_days']} days")
            cause.append("certificate expiry approaching")
            actions.append("trigger certbot renewal or manually renew via CA")

        if sec["secret_expiry_days"] < 30:
            issues.append(f"API secrets expire in {sec['secret_expiry_days']} days")
            cause.append("secret rotation overdue")
            actions.append("rotate secrets in vault and update all consuming services")

        if not issues:
            return {
                "summary": "Security posture looks good across monitored parameters.",
                "observed": [
                    f"Failed logins: {sec['failed_logins_per_min']}/min",
                    f"SSL expiry: {sec['cert_expiry_days']} days",
                    f"Critical CVEs: {sec['critical_cves']}"
                ],
                "likely_cause": "No active security threats detected.",
                "recommended_action": "Continue regular secret rotation and patch management."
            }

        return {
            "summary": f"Security has {len(issues)} concern(s) requiring attention.",
            "observed": issues,
            "likely_cause": ", ".join(cause) + ".",
            "recommended_action": " | ".join(actions)
        }

    # ── COST ─────────────────────────────────────────────
    if any(w in q for w in ["cost", "money", "spend", "budget", "expensive", "waste", "idle"]):
        issues = []
        actions = []

        if cost["daily_variance_pct"] > 10:
            issues.append(
                f"Daily spend is ${cost['daily_cost']:,} — "
                f"{cost['daily_variance_pct']}% over budget of ${cost['daily_budget']:,}"
            )
            actions.append("identify and terminate idle resources immediately")

        if cost["monthly_variance_pct"] > 10:
            issues.append(
                f"Monthly spend is ${cost['monthly_cost']:,} — "
                f"{cost['monthly_variance_pct']}% over budget of ${cost['monthly_budget']:,}"
            )

        if cost["idle_waste_monthly"] > 0:
            issues.append(
                f"${cost['idle_waste_monthly']}/month wasted on idle resources — "
                f"check EC2 instances, snapshots, and load balancers"
            )
            actions.append("run idle resource cleanup — estimated saving $" + str(cost["idle_waste_monthly"]) + "/month")

        for f in forecast_issues():
            if "spend" in f["metric"].lower() or "cost" in f["metric"].lower():
                issues.append(f["prediction"])
                actions.append(f["action"])

        if not issues:
            return {
                "summary": "Cloud spend is within budget.",
                "observed": [
                    f"Daily cost: ${cost['daily_cost']:,} (budget: ${cost['daily_budget']:,})",
                    f"Monthly cost: ${cost['monthly_cost']:,} (budget: ${cost['monthly_budget']:,})"
                ],
                "likely_cause": "No cost anomalies detected.",
                "recommended_action": "Continue monitoring for idle resource accumulation."
            }

        return {
            "summary": f"Cost monitoring flagged {len(issues)} issue(s).",
            "observed": issues,
            "likely_cause": "Overspend driven by resource waste and unoptimized provisioning.",
            "recommended_action": " | ".join(actions)
        }

    # ── RELIABILITY / SLO ────────────────────────────────
    if any(w in q for w in ["reliability", "slo", "sla", "uptime", "availability", "error budget", "incident"]):
        issues = []
        actions = []

        if rel["slo_status"] != "ok":
            issues.append(
                f"SLO breached — achieved {rel['slo_achieved']}% "
                f"against target of {rel['slo_target_pct']}%"
            )
            actions.append("freeze non-critical deployments until error budget recovers")

        if rel["error_budget_remaining_pct"] < 25:
            issues.append(
                f"Error budget is {rel['error_budget_remaining_pct']}% remaining — "
                f"burning too fast"
            )
            actions.append("halt risky changes and focus on reliability fixes")

        if rel["mttr_minutes"] > 30:
            issues.append(
                f"MTTR is {rel['mttr_minutes']} minutes — "
                f"incidents are taking too long to resolve"
            )
            actions.append("improve runbook coverage and on-call escalation paths")

        p1s = open_p1()
        if p1s:
            issues.append(f"{len(p1s)} P1 incident(s) currently open")
            actions.append("all hands on P1 resolution — " + p1s[0]["title"])

        if not issues:
            return {
                "summary": "Reliability metrics are within acceptable range.",
                "observed": [
                    f"Availability: {rel['availability_pct']}%",
                    f"SLO: {rel['slo_achieved']}% vs target {rel['slo_target_pct']}%",
                    f"Error budget remaining: {rel['error_budget_remaining_pct']}%",
                    f"MTTR: {rel['mttr_minutes']} min"
                ],
                "likely_cause": "System is getting more reliable over time.",
                "recommended_action": "No action required. Continue weekly reliability reviews."
            }

        return {
            "summary": f"Reliability has {len(issues)} concern(s).",
            "observed": issues,
            "likely_cause": "Error budget burn rate is too high for current deployment velocity.",
            "recommended_action": " | ".join(actions)
        }

    # ── OVERALL HEALTH / GENERAL ─────────────────────────
    if any(w in q for w in ["health", "status", "overall", "system", "everything", "anything", "what", "how"]):
        critical_items = []
        warning_items = []

        if infra["cpu_status"] in ("warning", "critical"):
            critical_items.append(f"CPU at {infra['cpu']}%")
        if infra["memory_status"] in ("warning", "critical"):
            critical_items.append(f"Memory at {infra['memory']}%")
        if app["error_status"] in ("warning", "critical"):
            critical_items.append(f"Error rate at {app['error_rate_pct']}%")
        if db["backup_status"] == "failed":
            critical_items.append("Database backup failed")
        if kafka["dlq_status"] in ("warning", "critical"):
            warning_items.append(f"Kafka DLQ has {kafka['dlq_size']} messages")
        for v in vendor_issues():
            warning_items.append(v)
        for h in hygiene_issues():
            warning_items.append(h["detail"])
        p1s = open_p1()
        if p1s:
            critical_items.append(f"{len(p1s)} P1 incident(s) open")

        total = len(critical_items) + len(warning_items)
        if total == 0:
            return {
                "summary": "All systems are healthy. No issues detected.",
                "observed": [
                    f"CPU: {infra['cpu']}% | Memory: {infra['memory']}%",
                    f"Error rate: {app['error_rate_pct']}% | P95: {app['p95_ms']}ms",
                    f"DB connections: {db['connections']} | Backup: {db['backup_status']}",
                    f"Redis hit ratio: {cache['hit_ratio_pct']}%"
                ],
                "likely_cause": "System is operating normally.",
                "recommended_action": "Continue monitoring. Auto-refresh active every 30 seconds."
            }

        return {
            "summary": f"System has {len(critical_items)} critical and {len(warning_items)} warning issue(s).",
            "observed": critical_items + warning_items,
            "likely_cause": "Multiple systems showing stress — review each flagged area.",
            "recommended_action": "Start with critical items first, then address warnings."
        }

    # ── PREDICTIVE / FORECAST ────────────────────────────
    if any(w in q for w in ["predict", "forecast", "will", "future", "break", "tomorrow", "next"]):
        issues = forecast_issues()
        hyg = hygiene_issues()

        observed = [f["prediction"] for f in issues]
        observed += [h["detail"] for h in hyg]
        actions = [f["action"] for f in issues]

        if not observed:
            return {
                "summary": "No imminent issues predicted based on current trends.",
                "observed": ["All forecasts within safe thresholds"],
                "likely_cause": "System growth is within planned capacity.",
                "recommended_action": "Review forecasts weekly and plan capacity quarterly."
            }

        return {
            "summary": f"{len(observed)} predicted issue(s) require proactive action.",
            "observed": observed,
            "likely_cause": "Current growth trends will breach thresholds if left unaddressed.",
            "recommended_action": " | ".join(actions) if actions else "Review each forecast and create remediation tickets."
        }

    # ── EXTERNAL VENDORS ─────────────────────────────────
    if any(w in q for w in ["vendor", "external", "third party", "api", "cdn", "email", "sms"]):
        issues = vendor_issues()
        if not issues:
            return {
                "summary": "All external vendors are operational.",
                "observed": [
                    f"{v['name']}: {v['status']} ({v['latency_ms']}ms)"
                    for v in ext.get("vendors", [])
                ],
                "likely_cause": "No external dependency issues.",
                "recommended_action": "No action required."
            }
        return {
            "summary": f"{len(issues)} vendor(s) are experiencing issues.",
            "observed": issues,
            "likely_cause": "Third-party service degradation impacting dependent features.",
            "recommended_action": "Enable fallback mechanisms and notify affected teams."
        }

    # ── FALLBACK ─────────────────────────────────────────
    critical_count = sum([
        1 if infra["cpu_status"] == "critical" else 0,
        1 if app["error_status"] == "critical" else 0,
        1 if db["backup_status"] == "failed" else 0,
        1 if len(open_p1()) > 0 else 0
    ])

    return {
        "summary": f"Here is a current snapshot of your production system.",
        "observed": [
            f"Infrastructure: CPU {infra['cpu']}% | Memory {infra['memory']}% | Nodes {infra['nodes_online']}/{infra['nodes_total']}",
            f"Application: {app['rps']} RPS | P95 {app['p95_ms']}ms | Error rate {app['error_rate_pct']}%",
            f"Database: {db['connections']} connections | {db['slow_queries']} slow queries | Backup {db['backup_status']}",
            f"Cache: Hit ratio {cache['hit_ratio_pct']}% | Memory {cache['memory_usage_pct']}%",
            f"Kafka: Consumer lag {kafka['consumer_lag']:,} | DLQ {kafka['dlq_size']}",
            f"Reliability: {rel['availability_pct']}% availability | Error budget {rel['error_budget_remaining_pct']}% remaining",
            f"Open incidents: {incidents['open_count']} ({incidents['p1_count']} P1)"
        ],
        "likely_cause": f"System has {critical_count} critical issue(s) active right now.",
        "recommended_action": "Try asking: 'Why is checkout failing?' or 'Is the database healthy?' or 'What will break tomorrow?'"
    }


@ai_bp.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    snap = get_full_snapshot()
    result = analyze(question, snap)

    return jsonify({
        "question": question,
        "summary": result["summary"],
        "observed": result["observed"],
        "likely_cause": result["likely_cause"],
        "recommended_action": result["recommended_action"]
    })