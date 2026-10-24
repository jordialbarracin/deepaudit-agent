"""
DeepAudit Autonomous Agent: Orchestrates financial statement forensics,
Tavily web intelligence, and NVIDIA Nemotron forensic synthesis.
"""

import json
import time
from typing import Dict, Any, List, Optional

from deepaudit.nebius_client import DeepAuditNebiusClient
from deepaudit.tavily_client import DeepAuditTavilyClient
from deepaudit.forensic_engine import ForensicEngine, clean_amount
from deepaudit.compliance_engine import ComplianceEngine
from deepaudit.test_cases import get_case, AUDIT_TEST_CASES

FORENSIC_AUDITOR_SYSTEM_PROMPT = """You are the Managing Partner of Forensic Accounting, Corporate Due Diligence, and Financial Crime Prevention at a top-tier international advisory firm.
Your job is to audit vendors and flagged corporate entities by correlating internal financial ledgers with real-time external intelligence.
You are relentless, technically authoritative, rigorous, and quantitative.
You must issue a formal, audit-ready Due Diligence Forensic Dictum (admissible for Executive Risk Committees, General Counsel reviews, and Forensic Inquiries) structured as:
1. CORPORATE RISK SCORE (0 to 100, where 0 is pristine solvency and 100 is severe fraud or imminent bankruptcy).
2. EXECUTIVE VERDICT (APPROVED, UNDER OBSERVATION, or IMMEDIATE FREEZE & DISQUALIFICATION).
3. FORENSIC EVIDENCE & RED FLAGS MATRIX (internal ledger anomalies vs external intelligence).
4. QUANTITATIVE CORRELATION: How numerical indicators (Benford Chi-Square, Altman Z''-Score, CCC working capital, threshold avoidance) connect with external regulatory gazettes and tax registries uncovered via Tavily Search (BOE, BORM, Tax liens, accreditation registries).
5. CFO IMMEDIATE ACTION PLAN: Step-by-step mitigation and automated ERP hold instructions.
Write in authoritative, formal, and precise corporate English."""

class DeepAuditAgent:
    def __init__(self):
        self.nebius_client = DeepAuditNebiusClient()
        self.tavily_client = DeepAuditTavilyClient()
        self.forensic_engine = ForensicEngine()

    def run_audit(self, case_or_id: Any) -> Dict[str, Any]:
        """
        Executes an end-to-end forensic audit for a company.
        """
        if isinstance(case_or_id, str):
            case = get_case(case_or_id)
        else:
            case = case_or_id

        company_name = case.get("company_name", "Audited Entity")
        cif = case.get("cif", "N/A")
        financials = case.get("financials", {})
        invoices = case.get("invoices", [])

        # Step 1: Internal Quantitative Forensics
        amounts = [clean_amount(inv.get("amount", 0.0)) for inv in invoices]
        benford_res = self.forensic_engine.analyze_benford(amounts)
        altman_res = self.forensic_engine.calculate_altman_z_score(financials)
        irregularities = self.forensic_engine.detect_invoice_irregularities(invoices)
        counterparty_res = self.forensic_engine.verify_payment_counterparty(case)

        # Step 2: ISO Standards, Labor Safety (PRL) & Regulatory Compliance
        compliance_res = ComplianceEngine.audit_certifications(case)

        # Step 3: External Web Intelligence via Tavily
        tavily_query = f"{company_name} {cif} bankruptcy insolvency public gazette BOE BORM tax liens ISO accreditation labor safety"
        tavily_res = self.tavily_client.search(tavily_query, search_depth="advanced", max_results=3)

        # Step 4: LLM Synthesis with NVIDIA Nemotron on Nebius
        prompt = f"""
FORENSIC DUE DILIGENCE, REGULATORY COMPLIANCE & VENDOR AUDIT MEMORANDUM

AUDITED CORPORATE ENTITY:
- Company Legal Name: {company_name}
- Tax Identification (CIF/VAT): {cif}
- Industry Sector: {case.get('sector', 'Commercial Services')}
- Annual Invoiced Volume Under Review: {case.get('annual_volume_invoiced', 'N/A')}
- Audit Description & Context: {case.get('description', '')}

INTERNAL QUANTITATIVE EVIDENCE (INVOICE LEDGER & BALANCE SHEET FORENSICS):
1. Benford's Law Chi-Square Test (First-Digit Anomaly Detection):
   - Sample Size Evaluated: {benford_res.get('sample_size')} invoices.
   - Chi-Square Statistic: {benford_res.get('chi_square_statistic')} (95% Critical Threshold: 15.51).
   - Benford Classification: {benford_res.get('risk_classification')}.

2. Altman Z''-Score Model (Private Non-Manufacturing Firm Solvency / Distress Prediction):
   - Z''-Score: {altman_res.get('z_score')}
   - Solvency Zone: {altman_res.get('zone')} ({altman_res.get('description')})
   - Net Working Capital: {altman_res.get('working_capital_euros')} EUR
   - Current Liquidity Ratio: {altman_res.get('current_ratio')}

3. Flagged Invoice Irregularities & Proof-of-Delivery (POD) Telemetry:
   - Total Anomalies Flagged: {len(irregularities)}
   - Forensic Findings: {json.dumps(irregularities, ensure_ascii=False, indent=2)}

4. Banking Counterparty & IBAN Diversion Audit (Payment Fraud Defense):
   - Status: {counterparty_res.get('status')}
   - Destination Account: {counterparty_res.get('iban_masked')} (Jurisdiction: {counterparty_res.get('iban_country')})
   - Registered Beneficiary: {counterparty_res.get('beneficiary_name')}
   - Fraud Warnings: {json.dumps(counterparty_res.get('anomalies'), ensure_ascii=False, indent=2)}

5. ISO Official Accreditation & Labor Safety (PRL) Registry Verification:
   - Compliance Index: {compliance_res.get('compliance_score')}% ({compliance_res.get('maturity_level')})
   - ISO Certification Matrix: {json.dumps(compliance_res.get('certifications'), ensure_ascii=False, indent=2)}
   - Labor Safety Audit & Sanction Registry: {json.dumps(compliance_res.get('labor_safety_audit'), ensure_ascii=False, indent=2)}

REAL-TIME EXTERNAL INTELLIGENCE RETRIEVED VIA TAVILY SEARCH (OFFICIAL GAZETTES & REGISTRIES):
- Tavily Synthesis: {tavily_res.get('answer')}
- Official Gazette Filings & Cited Public Records:
{json.dumps(tavily_res.get('results'), ensure_ascii=False, indent=2)}

FORENSIC DICTUM REQUIREMENTS:
Issue the definitive Forensic Due Diligence Memorandum structured as:
1. Overall Risk Score (0 to 100).
2. Executive Verdict (APPROVED / ENHANCED MONITORING / IMMEDIATE FREEZE & DISQUALIFICATION).
3. Red Flags & Quantitative Correlations Matrix.
4. Triangulation between internal ledgers and Tavily gazette findings (BOE, BORM, tax liens).
5. CFO & Procurement 4-Point Mitigation Action Plan.
"""

        llm_res = self.nebius_client.complete(
            prompt=prompt,
            system_prompt=FORENSIC_AUDITOR_SYSTEM_PROMPT,
            model="nvidia/Nemotron-3_5-Lightning",
            temperature=0.25,
            max_tokens=3000
        )

        # Parse risk score heuristic from text if possible, or calculate combined index
        base_risk = 0.0
        if altman_res["zone"] == "DISTRESS_ZONE":
            base_risk += 45.0
        elif altman_res["zone"] == "GREY_ZONE":
            base_risk += 20.0

        if benford_res.get("anomaly_detected"):
            base_risk += 25.0

        if len(irregularities) > 0:
            base_risk += min(len(irregularities) * 8.0, 30.0)

        if counterparty_res.get("has_critical_discrepancy"):
            base_risk += 35.0

        # If Tavily found insolvency/bankruptcy
        ans_lower = tavily_res.get("answer", "").lower()
        if "bankruptcy" in ans_lower or "insolven" in ans_lower or "default" in ans_lower:
            base_risk = max(base_risk, 88.0)

        risk_score = min(round(base_risk), 98) if base_risk > 0 else 12
        audit_verdict = "IMMEDIATE FREEZE & DISQUALIFICATION" if risk_score >= 75 else ("ENHANCED MONITORING" if risk_score >= 40 else "APPROVED")
        erp_payload = self.forensic_engine.generate_erp_integration_payload(case, audit_verdict)

        return {
            "company_name": company_name,
            "cif": cif,
            "risk_score": risk_score,
            "risk_level": "CRITICAL" if risk_score >= 75 else ("MODERATE" if risk_score >= 40 else "LOW"),
            "audit_verdict": audit_verdict,
            "forensics": {
                "benford": benford_res,
                "altman_z": altman_res,
                "irregularities": irregularities,
                "counterparty": counterparty_res
            },
            "compliance": compliance_res,
            "external_intel": tavily_res,
            "erp_integration": erp_payload,
            "executive_report": llm_res["content"],
            "model_metadata": {
                "model": llm_res["model"],
                "latency_seconds": llm_res["latency_seconds"],
                "tokens": llm_res["completion_tokens"],
                "cloud": "Nebius Token Factory"
            }
        }
