# DeepAudit 🛡️
### Autonomous Corporate Forensics & Vendor Due Diligence Agent
**Nebius x NVIDIA Global AI Hackathon ($50,000 Cash & Jetson Awards)**  
*Categories:* **Best Apps & Agents** ($10,000) &middot; **Best Use of Tavily Award** ($3,000)

DeepAudit is an autonomous corporate intelligence and forensic accounting agent powered by **NVIDIA Nemotron-3_5-Lightning** on **Nebius Token Factory**, combined with real-time web intelligence via **Tavily AI Search**.

---

## 🔍 Core Capabilities
1. **Benford's Law Anomaly Engine**: Detects statistical deviations in invoice ledgers ($\chi^2$ test with critical threshold 15.51) to uncover fabricated billing and threshold evasion.
2. **Altman Z-Score Bankruptcy Predictor**: Quantitative evaluation of financial distress and 24-month insolvency probability.
3. **Red Flag Invoice Detector**: Flags split payments just under approval limits (4,900 € - 5,000 €), duplicate amounts, and round-number anomalies.
4. **Tavily Real-Time Web Intelligence**: Autonomous scraping and correlation with official gazettes (BORM, BOE, AEAT tax debtor registries, insolvency proceedings, and judicial news).
5. **Big-4 Partner Level Synthesis**: Generates comprehensive forensic audit reports with corporate risk scores (0-100) and actionable CFO directives.

---

## 🛠️ Project Structure
```
deepaudit-agent/
├── deepaudit/
│   ├── __init__.py
│   ├── config.py              # Configuration & API key loader
│   ├── nebius_client.py       # Nebius Token Factory client (NVIDIA Nemotron-3_5-Lightning)
│   ├── tavily_client.py       # Tavily AI Search client (live API + legal gazette cache)
│   ├── forensic_engine.py     # Benford's Law, Altman Z-Score, and anomaly algorithms
│   ├── auditor_agent.py       # Master agent orchestrating data, Tavily, and Nemotron
│   ├── test_cases.py          # Real-world corporate audit scenarios (Iberia, Solaria, Nexus)
│   ├── server.py              # FastAPI server
│   └── static/
│       └── index.html         # Interactive Forensic Dashboard with Chart.js & PDF Export
├── cli.py                     # Rich interactive command-line interface
├── requirements.txt
└── .env                       # API Credentials (Nebius & Tavily)
```

---

## 🚀 Quick Start

### 1. Launch Interactive Web Dashboard
```bash
python -m uvicorn deepaudit.server:app --host 127.0.0.1 --port 8001
```
Open **[http://127.0.0.1:8001](http://127.0.0.1:8001)** in your browser.

### 2. Run Terminal Forensics CLI
```bash
python cli.py
```
Select a supplier profile (1-3) to run the full forensic investigation.
