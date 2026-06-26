# Monitored Parameters

All parameters monitored across 12 domains.

---

## 1. Infrastructure Health
| Parameter | Description | Unit |
|-----------|-------------|------|
| CPU Utilization | Average CPU usage across all nodes | % |
| Memory Utilization | Average RAM usage across all nodes | % |
| Disk Usage | Storage consumed on primary volumes | % |
| Disk IOPS | Input/output operations per second | ops/s |
| Disk Latency | Average disk read/write latency | ms |
| Network Throughput | Total inbound + outbound traffic | Mbps |
| Network Errors | Packet errors and drops | count/s |
| Load Average | 1-minute system load average | float |
| Node Availability | Nodes online vs total | count |
| Container Restarts | Total pod restarts across all services | count |
| Kubernetes Pod Health | Per-pod status (running/warning/crashloop) | status |
| Kubernetes Node Health | Per-node CPU and memory | % |
| Autoscaling Events | HPA scale-up/down events today | count |

## 2. Application Health
| Parameter | Description | Unit |
|-----------|-------------|------|
| Requests Per Second | Total RPS across all services | req/s |
| Response Time | Average end-to-end response time | ms |
| P50 Latency | Median request latency | ms |
| P95 Latency | 95th percentile latency | ms |
| P99 Latency | 99th percentile latency | ms |
| Error Rate | % of requests returning errors | % |
| HTTP 4xx | Client error responses per minute | count/min |
| HTTP 5xx | Server error responses per minute | count/min |
| API Success % | Overall successful request percentage | % |
| Slow Endpoints | Top endpoints exceeding latency SLO | list |
| Service Dependency Failures | Failed calls to downstream services | list |

## 3. Database Health
| Parameter | Description | Unit |
|-----------|-------------|------|
| Database Availability | PostgreSQL primary reachable | status |
| Connection Count | Active client connections | count |
| Active Queries | Queries currently executing | count |
| Slow Queries | Queries exceeding 1s execution time | count |
| Query Latency | Average query execution time | ms |
| Replication Lag | Primary-to-replica replication delay | seconds |
| Deadlocks | Deadlock events in last hour | count |
| Lock Waits | Queries waiting for row locks | count |
| Storage Growth | Daily storage increase rate | GB/day |
| Backup Status | Last backup success or failure | status |
| Backup Age | Hours since last successful backup | hours |

## 4. Cache Layer (Redis)
| Parameter | Description | Unit |
|-----------|-------------|------|
| Redis Availability | Redis primary reachable | status |
| Memory Usage | Redis memory used vs max | % |
| Eviction Rate | Keys evicted per second | keys/s |
| Hit Ratio | Cache hits / total requests | % |
| Miss Ratio | Cache misses / total requests | % |
| Connection Count | Active Redis connections | count |
| Replication Status | Replica sync status | status |

## 5. Messaging Systems (Kafka)
| Parameter | Description | Unit |
|-----------|-------------|------|
| Kafka Availability | Kafka broker reachable | status |
| Topic Throughput | Messages produced per second | msg/s |
| Producer Failures | Failed produce attempts | count |
| Consumer Lag | Messages behind latest offset | count |
| Message Backlog | Total unprocessed messages | count |
| DLQ Growth | Dead letter queue size | count |

## 6. External Dependencies
| Parameter | Description | Unit |
|-----------|-------------|------|
| Payment Gateway Status | Stripe/Razorpay availability | status |
| Email Service Status | SendGrid/SES availability | status |
| SMS Provider Status | Twilio availability | status |
| Third Party API Status | Maps, Auth0 availability | status |
| CDN Status | CloudFront availability | status |
| Vendor Latency | Response time per vendor | ms |

## 7. Security & Compliance
| Parameter | Description | Unit |
|-----------|-------------|------|
| Failed Logins | Failed auth attempts per minute | count/min |
| Login Spikes | Sudden increase in failed logins | detection |
| Blocked IPs | IPs currently blocked by WAF | count |
| WAF Events | Web application firewall triggers/hour | count/hr |
| Secret Expiry | Days until API secrets expire | days |
| Certificate Expiry | Days until SSL cert expires | days |
| IAM Key Expiry | Days until access keys expire | days |
| Open Vulnerabilities | Total known vulnerabilities | count |
| Critical CVEs | CVEs with CVSS score > 9.0 | count |

## 8. Operational Hygiene
| Parameter | Description |
|-----------|-------------|
| SSL Certificate Expiry | Days until cert expires with renewal alert |
| Domain Expiry | Days until domain registration expires |
| Backup Status | Last backup succeeded or failed |
| Backup Restore Verification | Days since last restore test |
| DNS Health | DNS resolution working for all records |
| NTP Synchronization | Clock drift detected on any node |
| Disk Forecast | Predicted days until disk is full |
| IP Whitelist Expiry | Days until vendor VPN access expires |
| Kubernetes Version | Cluster running supported K8s version |
| OS Patch Status | Critical security patches applied |

## 9. Cost Monitoring
| Parameter | Description | Unit |
|-----------|-------------|------|
| Daily Cloud Cost | Total cloud spend today | USD |
| Monthly Cloud Cost | Total cloud spend this month | USD |
| Cost by Service | Spend broken down per microservice | USD |
| Cost by Team | Spend broken down per engineering team | USD |
| Cost Trend | Daily cost over last 30 days | USD/day |
| Idle Resources | Unused resources wasting budget | list |

## 10. Reliability
| Parameter | Description | Unit |
|-----------|-------------|------|
| SLO Achievement | Service level objective met or breached | % |
| SLA Compliance | Contract SLA compliant or breached | status |
| Error Budget | Remaining error budget this month | % |
| Availability % | Actual uptime percentage | % |
| MTTR | Mean time to resolve incidents | minutes |
| MTTD | Mean time to detect incidents | minutes |
| Incident Count | Total incidents in last 30 days | count |

## 11. Incident Center
| Parameter | Description |
|-----------|-------------|
| Open Incidents | All currently open incidents |
| Incident Severity | P1 / P2 / P3 classification |
| Incident Owner | Engineer assigned to incident |
| Escalation Status | Whether incident has been escalated |
| Time Since Opened | Duration incident has been open |

## 12. Predictive Monitoring
| Parameter | Description |
|-----------|-------------|
| Disk Fill Forecast | Days until disk reaches 100% at current growth |
| Certificate Expiry Forecast | Days until SSL cert expires |
| DB Connection Trend | Connection growth rate and pool exhaustion ETA |
| Cloud Cost Projection | Projected month-end spend vs budget |