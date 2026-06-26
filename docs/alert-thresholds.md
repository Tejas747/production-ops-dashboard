# Alert Thresholds

Every alert threshold and the reasoning behind it.

---

## Infrastructure

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| CPU Utilization | > 70% | > 85% | Above 85% leaves no headroom for traffic spikes. At 70% we investigate before it becomes a problem. |
| Memory Utilization | > 75% | > 90% | OOM kills happen suddenly. 90% is too close to the edge — alert at 75% to allow graceful response. |
| Disk Usage | > 75% | > 85% | Disk full = instant outage for databases and logs. 85% gives ~hours to act, not minutes. |
| Disk Latency | > 10ms | > 50ms | High disk latency directly impacts database query times. |
| Network Errors | > 0.1% | > 1% | Any sustained network errors indicate hardware or config issues. |
| Load Average | > 3.0 | > 6.0 | On a 4-core node, load > 4 means queuing. Alert at 3 to catch trends early. |
| Container Restarts | > 5 total | > 15 total | Frequent restarts indicate crashlooping. 5+ warrants investigation. |
| Node Availability | < 100% | < 80% | Any offline node reduces capacity. Below 80% risks cascading failures. |

## Application

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| P95 Latency | > 500ms | > 1000ms | Users notice latency above 500ms. Above 1s causes abandonment. |
| P99 Latency | > 800ms | > 1500ms | P99 represents the worst 1% of users — still important to track. |
| Error Rate | > 1% | > 5% | 1% errors = 1000 failed requests/min at 100k RPS. 5% = user-visible outage. |
| HTTP 5xx | > 10/min | > 50/min | Server errors are always actionable. Any sustained 5xx needs investigation. |
| API Success % | < 99% | < 95% | Below 99% means errors are noticeable. Below 95% is a major incident. |

## Database

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Connection Count | > 150 | > 200 | PostgreSQL default max_connections is 200. Hitting the limit = connection refused errors. |
| Slow Queries | > 5 | > 10 | Slow queries block other queries and consume connection slots. |
| Replication Lag | > 5s | > 30s | Lag > 30s means significant data loss risk on failover. |
| Deadlocks | > 0 | > 5 | Any deadlock is a bug. More than 5/hour is a serious application issue. |
| Backup Age | > 24h | > 48h | RPO violation. Backups older than 24h mean potential data loss exceeds SLA. |
| Storage Growth | > 3 GB/day | > 5 GB/day | Extrapolate to predict disk full date and plan ahead. |

## Cache (Redis)

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Memory Usage | > 75% | > 90% | Redis evicts keys when full. Evictions cause cache misses which hammer the database. |
| Hit Ratio | < 80% | < 60% | Below 80% means cache isn't helping much. Below 60% means the database is taking the full load. |
| Eviction Rate | > 20/s | > 50/s | High eviction = memory pressure. Data is being thrown away faster than it's useful. |

## Messaging (Kafka)

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Consumer Lag | > 10,000 | > 100,000 | Growing lag means consumers can't keep up. At 100k messages behind, async systems are failing. |
| DLQ Size | > 50 | > 200 | Dead letter queue growth means messages are failing permanently. Each one is a lost transaction. |
| Producer Failures | > 5/min | > 20/min | Producer failures mean events are being dropped silently. |

## Security

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Failed Logins | > 50/min | > 200/min | 50/min could be a user issue. 200/min is almost certainly a brute force attack. |
| SSL Cert Expiry | < 30 days | < 14 days | Auto-renewal can fail. 30 days gives time to manually intervene before users see errors. |
| Secret Expiry | < 30 days | < 14 days | Expired secrets cause silent auth failures across all services using them. |
| IAM Key Expiry | < 30 days | < 14 days | Expired IAM keys break cloud API calls and deployments. |
| Critical CVEs | > 1 | > 3 | Any CVSS 9+ vulnerability is urgent. More than 3 unpatched is a compliance violation. |

## Operational Hygiene

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Domain Expiry | < 45 days | < 14 days | Domain expiry = complete outage. 45 days gives time to fix billing/renewal issues. |
| Disk Forecast | < 21 days | < 10 days | Forecasted full disk. 10 days is the minimum time to safely expand storage. |
| Backup Restore Test | > 30 days | > 90 days | Untested backups are not real backups. Test monthly at minimum. |
| Vendor VPN Expiry | < 14 days | < 5 days | Expired vendor VPN = support team locked out during incidents. |

## Cost

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Daily Cost vs Budget | > 110% | > 130% | 10% over budget needs review. 30% over means a runaway resource is consuming money. |
| Monthly Cost vs Budget | > 110% | > 130% | Same logic applied to monthly rollup. |

## Reliability

| Metric | Warning | Critical | Reasoning |
|--------|---------|----------|-----------|
| Error Budget Remaining | < 25% | < 10% | Burning error budget too fast means an SLO breach is imminent. Freeze risky deployments. |
| Availability % | < 99.9% | < 99.5% | 99.9% is the standard SLO. Below 99.5% is an SLA breach for most contracts. |
| MTTR | > 30 min | > 60 min | Incidents lasting over an hour cause significant user impact and revenue loss. |
| MTTD | > 15 min | > 30 min | Slow detection means longer outages. Under 15 min detection is the goal. |