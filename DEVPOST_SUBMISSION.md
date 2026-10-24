# DeepAudit: Autonomous Forensic Due Diligence & Corporate Integrity Agent

**Hackathon Track:** Best Apps and Agents Track  
**Special Award Category:** **Best Use of Tavily ($3,000 in cash)**  
**Submission for:** Nebius x NVIDIA Global AI Hackathon  

---

## 💡 Inspiration
Corporate accounting fraud, supplier insolvency, and hidden tax debts cost enterprises billions annually. In the real business world (such as our own logistics and corporate management experience), vetting a critical supplier or counterparty requires tedious, multi-day manual investigation: pulling balance sheets, recalculating financial ratios, running statistical fraud tests, and combing through fragmented public records (official gazettes, tax registry liens, and insolvency filings).

Small-to-medium enterprises and audit teams cannot afford Big-4 forensic teams for routine vendor checks. We created **DeepAudit**: an autonomous AI forensic auditor combining **NVIDIA Nemotron-3.5-Lightning on Nebius Token Factory** with **Tavily AI Search Engine** and rigorous statistical anomaly detection.

---

## 🔍 What It Does
1. **Mathematical & Statistical Forensic Analysis:**
   - **Benford's Law Chi-Square ($\chi^2$) Goodness-of-Fit:** Analyzes the first-digit frequency distribution of supplier invoice ledgers to detect fabricated numbers ($p < 0.05$ anomaly flagging).
   - **Altman Z-Score Bankruptcy Prediction:** Computes working capital, retained earnings, EBIT, equity, and asset turnover ratios to categorize financial distress (*Distress Zone: $Z < 1.81$*, *Grey Zone: $1.81 \le Z \le 2.99$*, *Safe Zone: $Z > 2.99$*).
   - **Threshold Avoidance Detection:** Flags structured invoice clusters hovering just below mandatory audit/approval ceilings (€3,000, €5,000, €10,000).
2. **Deep Real-Time Intelligence via Tavily Search Engine (Special Prize Focus):**
   - Autonomously formulates targeted Boolean queries across public regulatory bodies:
     - Spanish State Official Gazette (**BOE**) & Commercial Registry (**BORM**).
     - Tax Agency debts & liens (**AEAT** Art. 95 LGT).
     - Judicial insolvency declarations & bankruptcy proceedings (**Registro Público Concursal**).
   - Synthesizes fragmented web articles and creditor notices into verified factual claims with source URLs.
3. **Big-4 Executive Forensic Report Generation:**
   - NVIDIA Nemotron synthesizes financial metrics and live Tavily web intelligence into a professional auditor memorandum formatted with KPMG/PwC diligence rigor.
   - Provides concrete operational recommendations: bank guarantee requirements, payment term reductions, or immediate supplier disengagement.
4. **Interactive Corporate Dashboard:**
   - Web application on port `8001` loaded with 3 pre-calibrated real-world test cases:
     - *Iberia Logistics Global SL* (Critical Risk 98/100, Insolvency Proceedings, Benford Chi-Square Fail).
     - *Solaria Energy Soluciones SL* (Low Risk 12/100, Safe Zone Z=4.12, Clean Registry).
     - *Nexus Inversiones Tech SL* (Elevated Risk 76/100, Aggressive Debt Leverage).

---

## 🌟 Best Use of Tavily AI Search ($3,000 Category)
Tavily is the core intelligence sensor of DeepAudit. Financial statements alone cannot detect a secret bankruptcy petition filed last week or an active tax lien published yesterday in the provincial gazette. DeepAudit leverages Tavily's search API to:
1. Conduct multi-hop verification of corporate CIF/NIF identification numbers.
2. Query legal insolvencies and commercial registry changes in real time.
3. Feed clean, relevant regulatory extracts directly into Nemotron's context window without hallucination.

---

## 🛠️ How We Built It
- **Forensic Reasoning Engine:** NVIDIA Nemotron-3.5-Lightning on **Nebius Token Factory** delivering executive auditor memos.
- **Real-Time Web Intelligence:** **Tavily AI Search API** for official gazettes and regulatory filings.
- **Mathematical Forensics:** Custom Python implementation of Benford Chi-Square distribution and Altman Z-Score calculations.
- **Web Dashboard & API:** FastAPI backend (`deepaudit/server.py`) and responsive dark glassmorphism user interface.

---

## 📊 Sample Audit Output (Iberia Logistics Global SL)
- **Composite Forensic Risk Score:** **98 / 100 (CRITICAL RISK)**
- **Altman Z-Score:** **-0.42 (Severe Insolvency / Distress Zone)**
- **Benford's Law Chi-Square:** **24.81 (Statistically Significant Manipulation Detected)**
- **Tavily Intelligence Finding:** Active tax enforcement proceedings and concurrent insolvency declaration verified in Official Gazette.
- **Recommendation:** Freeze all invoice prepayment requests; require 100% bank performance bond for ongoing transport operations.

---

## 🚧 Challenges We Ran Into
- **Synthesizing Quantitative Math with Unstructured Web Text:** Blending hard mathematical scores (Altman Z, Chi-Square $p$-values) with unstructured regulatory text requires strict prompt grounding so the LLM does not distort numbers. We engineered structured JSON schemas passed directly from the `ForensicEngine` into Nemotron.
- **Handling False Positives in Small Invoice Sets:** Small invoice samples can trigger noisy Benford distributions. We added sample-size confidence intervals and invoice clustering metrics.

---

## 🏆 Accomplishments We're Proud Of
- A practical, battle-tested tool built for our own real-world corporate due diligence needs.
- Flawless integration between Tavily web search and Nebius Token Factory LLM inference.
- Production-grade web interface ready to audit any enterprise in seconds.

---

## 🔮 What's Next
- Direct API connectors for SAP, NetSuite, and QuickBooks ledgers.
- Automated generation of formal judicial expert witness reports (*informes periciales de parte*) for legal disputes.
