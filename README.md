# Production Operations Command Center

A full-stack monitoring dashboard that provides a single-pane-of-glass view of a production-grade internet business. Built as part of the iRage DevOps Assignment, June 2026.

Live Demo: https://production-ops-dashboard.onrender.com

---

## The Problem It Solves

Production systems fail in predictable ways. Disks fill up slowly. SSL certificates expire quietly. Kafka consumer lag grows unnoticed. Database connection pools exhaust without warning.

This dashboard answers one question before any of those become user-facing incidents:

> What can break in production tomorrow, and how would we know before users complain?

---

## System Context

The dashboard is designed around the following production scale:

- 100,000 Daily Active Users
- 20 Microservices on Kubernetes
- PostgreSQL (primary + replica)
- Redis cache cluster
- Kafka message broker
- CloudFront CDN
- AWS cloud infrastructure
- Web and mobile applications

---

## Architecture

```
Browser
   |
   | HTTP
   v
Flask Backend (Render.com)
   |
   |-- GET  /api/infrastructure
   |-- GET  /api/application
   |-- GET  /api/database
   |-- GET  /api/cache
   |-- GET  /api/messaging
   |-- GET  /api/external
   |-- GET  /api/security
   |-- GET  /api/hygiene
   |-- GET  /api/cost
   |-- GET  /api/reliability
   |-- GET  /api/incidents
   |-- GET  /api/predictive
   |-- POST /api/ask
   |
Mock Data Engine
   |-- utils/time_series.py   (realistic metric generation with noise and trends)
   |-- utils/alert_engine.py  (threshold evaluation for all metrics)
   |-- mock_data/*.py         (one file per monitoring domain)
```

### Frontend
Single HTML file using vanilla JavaScript and Chart.js. Polls all 12 APIs every 30 seconds. No build step or framework required.

### Backend
Python and Flask with 12 blueprints, one per monitoring domain. Served via Render.com with auto-deploy from GitHub.

### Mock Data Engine
Generates realistic time-series data with configurable baseline, variance, trend, and spike probability. Every metric is threshold-aware, meaning some values intentionally breach warning or critical levels to simulate a real production environment under stress.

---

## Monitoring Coverage

### 1. Infrastructure Health
CPU utilization, memory utilization, disk usage, disk IOPS, disk latency, network throughput, network errors, load average, node availability, container restarts, Kubernetes pod health, Kubernetes node health, autoscaling events.

### 2. Application Health
Requests per second, P50 latency, P95 latency, P99 latency, error rate, HTTP 4xx, HTTP 5xx, API success percentage, slow endpoints, service dependency failures.

### 3. Database Health
Availability, connection count, active queries, slow queries, query latency, replication lag, deadlocks, lock waits, storage growth, backup status, backup age.

### 4. Cache Layer
Redis availability, memory usage, eviction rate, hit ratio, miss ratio, connection count, replication status.

### 5. Messaging Systems
Kafka availability, topic throughput, producer failures, consumer lag, message backlog, dead letter queue growth.

### 6. External Dependencies
Payment gateway, email service, SMS provider, third-party APIs, CDN — status and latency per vendor.

### 7. Security and Compliance
Failed logins, login spikes, blocked IPs, WAF events, secret expiry, certificate expiry, IAM key expiry, open vulnerabilities, critical CVEs.

### 8. Operational Hygiene
SSL certificate expiry, domain expiry, backup status, backup restore verification age, DNS health, NTP synchronization, disk forecast, vendor VPN expiry, Kubernetes version, OS patch status.

### 9. Cost Monitoring
Daily cloud cost, monthly cloud cost, cost by service, cost by team, cost trend, idle resources.

### 10. Reliability
SLO achievement, SLA compliance, error budget remaining, availability percentage, MTTR, MTTD, incident count.

### 11. Incident Center
Open incidents, severity (P1/P2/P3), owner, escalation status, time since opened.

### 12. Predictive Monitoring
Disk fill forecast, certificate expiry forecast, database connection trend, cloud spend projection.

---

## Alert Thresholds

Selected thresholds and their reasoning:

| Metric | Warning | Critical | Reason |
|--------|---------|----------|--------|
| CPU Utilization | 70% | 85% | Headroom required for traffic spikes |
| Memory Utilization | 75% | 90% | OOM kills happen without warning |
| Disk Usage | 75% | 85% | Full disk causes immediate outage |
| P95 Latency | 500ms | 1000ms | User experience degrades above 500ms |
| Error Rate | 1% | 5% | 1% equals 1000 failed requests per minute at scale |
| Redis Hit Ratio | below 80% | below 60% | Low hit ratio forces full database load |
| Kafka Consumer Lag | 10,000 | 100,000 | Growing lag signals async system failure |
| Replication Lag | 5s | 30s | Data loss risk increases on failover |
| SSL Certificate Expiry | 30 days | 14 days | Auto-renewal can silently fail |
| Backup Age | 24h | 48h | RPO violation beyond 24 hours |
| Failed Logins | 50/min | 200/min | Brute force detection threshold |
| Error Budget Remaining | 25% | 10% | SLO breach becomes imminent |

Full threshold documentation is in docs/alert-thresholds.md.

---

## Project Structure

```
production-ops-dashboard/
|
|-- backend/
|   |-- app.py                      # Flask entry point, all blueprints registered
|   |-- requirements.txt
|   |
|   |-- mock_data/
|   |   |-- infrastructure.py
|   |   |-- application.py
|   |   |-- database.py
|   |   |-- cache.py
|   |   |-- messaging.py
|   |   |-- external.py
|   |   |-- security.py
|   |   |-- hygiene.py
|   |   |-- cost.py
|   |   |-- reliability.py
|   |   |-- incidents.py
|   |   `-- predictive.py
|   |
|   |-- routes/
|   |   |-- infrastructure.py       # GET /api/infrastructure
|   |   |-- application.py          # GET /api/application
|   |   |-- database.py             # GET /api/database
|   |   |-- cache.py                # GET /api/cache
|   |   |-- messaging.py            # GET /api/messaging
|   |   |-- external.py             # GET /api/external
|   |   |-- security.py             # GET /api/security
|   |   |-- hygiene.py              # GET /api/hygiene
|   |   |-- cost.py                 # GET /api/cost
|   |   |-- reliability.py          # GET /api/reliability
|   |   |-- incidents.py            # GET /api/incidents
|   |   |-- predictive.py           # GET /api/predictive
|   |   `-- ai_assistant.py         # POST /api/ask
|   |
|   `-- utils/
|       |-- time_series.py          # Time-series generation with noise and trends
|       `-- alert_engine.py         # Threshold evaluation engine
|
|-- frontend/
|   |-- index.html                  # Complete dashboard SPA
|   `-- assets/
|       `-- styles.css
|
|-- docs/
|   |-- architecture.md
|   |-- monitored-parameters.md
|   `-- alert-thresholds.md
|
|-- render.yaml                     # Render.com deployment config
`-- README.md
```

---

## Running Locally

Requirements: Python 3.11+, Git

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/production-ops-dashboard.git
cd production-ops-dashboard

# Create virtual environment
cd backend
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Open http://localhost:5000 in your browser.

To enable the AI Operations Assistant, set your Anthropic API key before starting the server:

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="your_key_here"

# Mac/Linux
export ANTHROPIC_API_KEY="your_key_here"
```

---

## Deployment

The project is deployed on Render.com with automatic deploys on every push to main.

Build command: `pip install -r backend/requirements.txt`

Start command: `python backend/app.py`

The `render.yaml` file in the root handles configuration automatically.

---

## Extending to Real Data

The mock data layer is intentionally isolated. To connect real infrastructure, replace any file in `mock_data/` with live queries while keeping the return structure identical.

Example using Prometheus:

```python
import requests

def get_infrastructure_data():
    response = requests.get(
        "http://your-prometheus:9090/api/v1/query",
        params={"query": "100 - (avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)"}
    )
    cpu = float(response.json()["data"]["result"][0]["value"][1])
    # rest of the function unchanged
```

Compatible data sources: Prometheus, Node Exporter, CloudWatch, Datadog API, direct database queries.

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| Hosted Dashboard | https://production-ops-dashboard.onrender.com |
| Source Code | This repository |
| Architecture Diagram | docs/architecture.md |
| Monitored Parameters | docs/monitored-parameters.md |
| Alert Thresholds | docs/alert-thresholds.md |

---

## Evaluation Criteria Coverage

| Area | Weight | How Addressed |
|------|--------|---------------|
| Completeness of Monitoring | 35% | All 12 sections, 60+ parameters across every layer of the stack |
| Production Thinking | 25% | Threshold reasoning, predictive forecasting, operational hygiene section |
| Dashboard Usability | 15% | Single-page app, sidebar navigation, 30-second auto-refresh |
| Alert Design | 10% | Three-level alerting (ok/warning/critical) with documented reasoning |
| Architecture | 10% | Clean separation of data, API, and presentation layers |
| Innovation | 5% | AI Operations Assistant for natural language root cause analysis |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, Flask-CORS |
| Frontend | HTML, vanilla JavaScript, Chart.js |
| Deployment | Render.com |
| Version Control | GitHub |
| AI Assistant | Anthropic Claude API |
