"""
DeepAudit Forensic Accounting & Financial Health Engine.
Implements Benford's Law anomaly detection, Altman Z-Score bankruptcy prediction,
invoice threshold clustering, and liquidity ratios.
"""

import math
from typing import List, Dict, Any, Tuple

# Theoretical probabilities for first digits 1-9 under Benford's Law
BENFORD_DISTRIBUTION = {
    1: 0.3010,
    2: 0.1761,
    3: 0.1249,
    4: 0.0969,
    5: 0.0792,
    6: 0.0669,
    7: 0.0580,
    8: 0.0512,
    9: 0.0458
}

def clean_amount(val: Any) -> float:
    """Robust currency cleaner supporting European (1.234,56 €) and US formats."""
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace("€", "").replace("$", "").replace("£", "").replace(" ", "").replace("EUR", "")
    if "." in s and "," in s:
        if s.rfind(".") > s.rfind(","):
            # US format: 1,234.56
            s = s.replace(",", "")
        else:
            # European format: 1.234,56
            s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

class ForensicEngine:
    @staticmethod
    def analyze_benford(amounts: List[Any]) -> Dict[str, Any]:
        """
        Calculates first-digit distribution and Chi-Square anomaly score against Benford's Law.
        Deviations often reveal fabricated invoices or expense manipulation.
        """
        cleaned = [clean_amount(a) for a in amounts]
        valid_amounts = [abs(a) for a in cleaned if abs(a) >= 1.0]
        if len(valid_amounts) < 5:
            return {
                "sample_size": len(valid_amounts),
                "is_conclusive": False,
                "anomaly_detected": False,
                "chi_square": 0.0,
                "first_digit_counts": {},
                "explanation": "Insufficient sample size for Benford's Law statistical test (minimum 10 invoices recommended)."
            }

        counts = {d: 0 for d in range(1, 10)}
        for a in valid_amounts:
            # Extract first significant digit safely
            s = f"{a:.6f}".lstrip("0").replace(".", "").lstrip("0")
            if s:
                first_digit = int(s[0])
                if 1 <= first_digit <= 9:
                    counts[first_digit] += 1

        total = len(valid_amounts)
        observed_pct = {d: counts[d] / total for d in range(1, 10)}
        expected_counts = {d: BENFORD_DISTRIBUTION[d] * total for d in range(1, 10)}

        # Chi-Square calculation
        chi_square = 0.0
        for d in range(1, 10):
            exp = expected_counts[d]
            obs = counts[d]
            chi_square += ((obs - exp) ** 2) / exp

        # Critical value for 8 degrees of freedom at 95% confidence level is 15.51
        is_anomaly = chi_square > 15.51
        risk_level = "CRITICAL_MANIPULATION_RISK" if chi_square > 20.0 else ("ELEVATED_ANOMALY" if is_anomaly else "NORMAL_NATURAL_DISTRIBUTION")

        return {
            "sample_size": total,
            "is_conclusive": True,
            "chi_square_statistic": round(chi_square, 2),
            "critical_threshold_95pct": 15.51,
            "anomaly_detected": is_anomaly,
            "risk_classification": risk_level,
            "observed_distribution": {d: round(observed_pct[d] * 100, 1) for d in range(1, 10)},
            "theoretical_benford_pct": {d: round(BENFORD_DISTRIBUTION[d] * 100, 1) for d in range(1, 10)},
            "counts": counts
        }

    @staticmethod
    def calculate_cash_conversion_cycle(financials: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates Cash Conversion Cycle (CCC = DSO + DIO - DPO) to avoid false-positive
        insolvency classifications on asset-light logistics/service companies with negative working capital.
        """
        revenue = financials.get("revenue", 1.0)
        cogs = financials.get("cogs", revenue * 0.75)
        receivables = financials.get("accounts_receivable", financials.get("current_assets", 0.0) * 0.4)
        payables = financials.get("accounts_payable", financials.get("current_liabilities", 0.0) * 0.7)
        inventory = financials.get("inventory", 0.0)

        if revenue <= 0:
            revenue = 1.0
        if cogs <= 0:
            cogs = 1.0

        # Days Sales Outstanding (DSO)
        dso = (receivables / revenue) * 365.0
        # Days Inventory Outstanding (DIO)
        dio = (inventory / cogs) * 365.0
        # Days Payable Outstanding (DPO)
        dpo = (payables / cogs) * 365.0

        # Cash Conversion Cycle (CCC)
        ccc = dso + dio - dpo

        # Analysis
        is_asset_light_negative_wc = False
        if ccc < 0 and dso < 45.0:
            is_asset_light_negative_wc = True
            interpretation = (
                f"Favorable Cash Conversion Cycle ({ccc:.1f} days). "
                f"The firm collects receivables in {dso:.1f} days while settling payables to carriers in {dpo:.1f} days. "
                f"Negative working capital is structurally operational (asset-light logistics model), NOT immediate technical insolvency."
            )
        else:
            interpretation = (
                f"Cash Conversion Cycle at {ccc:.1f} days (DSO: {dso:.1f}d, DPO: {dpo:.1f}d). "
                f"Confirmed operating liquidity strain."
            )

        return {
            "cash_conversion_cycle_days": round(ccc, 1),
            "days_sales_outstanding_dso": round(dso, 1),
            "days_inventory_outstanding_dio": round(dio, 1),
            "days_payable_outstanding_dpo": round(dpo, 1),
            "is_asset_light_negative_wc": is_asset_light_negative_wc,
            "interpretation": interpretation
        }

    @staticmethod
    def calculate_altman_z_score(financials: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates Altman Z-Score for non-manufacturing/service private firms:
        Z' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
        Where:
        X1 = Working Capital / Total Assets
        X2 = Retained Earnings / Total Assets
        X3 = EBIT / Total Assets
        X4 = Book Value of Equity / Total Liabilities
        """
        total_assets = financials.get("total_assets", 1.0)
        current_assets = financials.get("current_assets", 0.0)
        current_liabilities = financials.get("current_liabilities", 0.0)
        retained_earnings = financials.get("retained_earnings", 0.0)
        ebit = financials.get("ebit", 0.0)
        equity = financials.get("equity", 0.0)
        total_liabilities = financials.get("total_liabilities", 1.0)

        if total_assets <= 0:
            total_assets = 1.0
        if total_liabilities <= 0:
            total_liabilities = 1.0

        working_capital = current_assets - current_liabilities

        x1 = working_capital / total_assets
        x2 = retained_earnings / total_assets
        x3 = ebit / total_assets
        x4 = equity / total_liabilities

        z_score = (6.56 * x1) + (3.26 * x2) + (6.72 * x3) + (1.05 * x4)

        ccc_data = ForensicEngine.calculate_cash_conversion_cycle(financials)

        if z_score < 1.1:
            zone = "DISTRESS_ZONE"
            if ccc_data["is_asset_light_negative_wc"] and ebit >= 0:
                description = "Mathematical warning due to negative working capital, but structurally mitigated by asset-light model with negative cash cycle and positive operational EBIT."
                score_color = "yellow"
            elif ccc_data["is_asset_light_negative_wc"] and ebit < 0:
                description = "Insolvency & bankruptcy distress: Asset-light model overwhelmed by cumulative operating losses (negative EBIT and depleted equity)."
                score_color = "red"
            else:
                description = "High probability of bankruptcy or debt default within 24 months due to structural balance sheet deficit."
                score_color = "red"
        elif 1.1 <= z_score < 2.6:
            zone = "GREY_ZONE"
            description = "Moderate financial strain; current liability restructuring recommended."
            score_color = "yellow"
        else:
            zone = "SAFE_ZONE"
            description = "Solvent balance sheet; minimal default risk."
            score_color = "green"

        return {
            "z_score": round(z_score, 2),
            "zone": zone,
            "description": description,
            "color": score_color,
            "ratios": {
                "working_capital_to_assets": round(x1, 3),
                "retained_earnings_to_assets": round(x2, 3),
                "ebit_to_assets_roa": round(x3, 3),
                "equity_to_debt_leverage": round(x4, 3)
            },
            "working_capital_euros": round(working_capital, 2),
            "current_ratio": round(current_assets / (current_liabilities if current_liabilities > 0 else 1.0), 2),
            "cash_conversion_cycle": ccc_data
        }

    @staticmethod
    def detect_invoice_irregularities(invoices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scans invoice records for suspicious patterns:
        - Invoices just below common approval thresholds (e.g., 4,900 - 4,999 € or 9,800 - 9,999 €)
        - Exact round-number payments
        - Near-duplicate invoices with identical amounts within short time intervals
        - Consecutive numbering discrepancies
        """
        anomalies: List[Dict[str, Any]] = []

        seen_amounts: Dict[float, List[Dict[str, Any]]] = {}

        for inv in invoices:
            amt = clean_amount(inv.get("amount", 0.0))
            num = inv.get("invoice_number", "UNKNOWN")
            date = inv.get("date", "")
            concept = inv.get("concept", "")

            # Check 1: Just below 5,000 threshold
            if 4800.0 <= amt < 5000.0:
                anomalies.append({
                    "severity": "HIGH",
                    "code": "THRESHOLD_AVOIDANCE_5K",
                    "invoice_number": num,
                    "amount": amt,
                    "date": date,
                    "description": f"Invoice amount of {amt:.2f} EUR suspiciously clustered just below the 5,000 EUR manager authorization ceiling."
                })

            # Check 2: Just below 10,000 threshold
            if 9600.0 <= amt < 10000.0:
                anomalies.append({
                    "severity": "HIGH",
                    "code": "THRESHOLD_AVOIDANCE_10K",
                    "invoice_number": num,
                    "amount": amt,
                    "date": date,
                    "description": f"Invoice split of {amt:.2f} EUR structured to bypass mandatory purchasing procurement audit (>10,000 EUR)."
                })

            # Check 3: Round numbers above 1,000
            if amt >= 1000.0 and amt.is_integer() and (amt % 1000 == 0):
                anomalies.append({
                    "severity": "MEDIUM",
                    "code": "ROUND_NUMBER_ESTIMATE",
                    "invoice_number": num,
                    "amount": amt,
                    "date": date,
                    "description": f"Perfect round figure ({amt:.2f} EUR); highly atypical in commercial logistics billing with standard VAT."
                })

            # Check 4: Potential duplicate billing
            if amt not in seen_amounts:
                seen_amounts[amt] = []
            seen_amounts[amt].append(inv)

            # Check 5: Weekend / Off-Hours POD Telemetry Cross-Validation
            inv_time = inv.get("time", "")
            if inv_time:
                try:
                    hour = int(inv_time.split(":")[0])
                    is_off_hours = hour >= 23 or hour < 6
                except Exception:
                    is_off_hours = False

                if is_off_hours:
                    if inv.get("pod_verified"):
                        anomalies.append({
                            "severity": "INFO",
                            "code": "VERIFIED_AUTO_POD_TELEMETRY",
                            "invoice_number": num,
                            "amount": amt,
                            "date": date,
                            "description": f"Submission at {inv_time} validated against electronic Proof-of-Delivery telemetry ({inv.get('pod_timestamp', 'Electronic Waybill')}). False-positive off-hours billing alert cleared by automated dispatch traceability."
                        })
                    else:
                        anomalies.append({
                            "severity": "MEDIUM",
                            "code": "UNVERIFIED_OFF_HOURS_SUBMISSION",
                            "invoice_number": num,
                            "amount": amt,
                            "date": date,
                            "description": f"Invoice submitted during off-hours ({inv_time}) without linked electronic POD/waybill telemetry. Dock receiving verification required."
                        })

        # Check 4: Potential duplicate billing
        for amt, group in seen_amounts.items():
            if len(group) > 1 and amt > 500.0:
                nums = [g.get("invoice_number") for g in group]
                anomalies.append({
                    "severity": "CRITICAL",
                    "code": "DUPLICATE_AMOUNT_SUSPICION",
                    "amount": amt,
                    "invoice_numbers": nums,
                    "description": f"Detected {len(group)} invoices with identical exact amount of {amt:.2f} EUR ({', '.join(nums)}). Potential duplicate payout or circular billing."
                })

        return anomalies

    @staticmethod
    def verify_payment_counterparty(company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits counterparty payment coordinates to prevent supplier impersonation,
        IBAN diversion fraud, and off-shore beneficiary masking.
        """
        company_name = company_profile.get("company_name", "")
        cif = company_profile.get("cif", "")
        bank_data = company_profile.get("bank_account", {})

        iban = bank_data.get("iban", "").replace(" ", "").upper()
        beneficiary = bank_data.get("beneficiary_name", "").strip()
        bank_name = bank_data.get("bank_name", "Desconocido")

        anomalies = []
        is_high_risk = False

        if not iban:
            return {
                "status": "MISSING_PAYMENT_DATA",
                "risk": "MEDIUM",
                "iban": "NO_REGISTRADO",
                "anomalies": ["Ficha de proveedor sin IBAN bancario verificado."]
            }

        country_code = iban[:2]
        expected_country = "ES" if cif.startswith(("A", "B", "C", "D", "E", "F", "G", "H", "J", "N", "P", "Q", "R", "S", "U", "V", "W")) else None

        # Cross-border check
        if expected_country and country_code != expected_country:
            is_high_risk = True
            anomalies.append({
                "severity": "CRITICAL",
                "code": "IBAN_CROSS_BORDER_DISCREPANCY",
                "description": (
                    f"Critical payment diversion risk: Entity domiciled in Spain ({cif}) "
                    f"requests remittance to a foreign banking jurisdiction ({country_code} - {bank_name}). "
                    f"Classic signature of business email compromise (BEC) or asset diversion fraud."
                )
            })

        # Beneficiary mismatch check
        if beneficiary:
            norm_comp = company_name.lower().replace("s.l.", "").replace("sl", "").replace("s.a.", "").replace("sa", "").strip()
            norm_ben = beneficiary.lower().replace("s.l.", "").replace("sl", "").replace("s.a.", "").replace("sa", "").replace("ltd", "").strip()
            if norm_comp not in norm_ben and norm_ben not in norm_comp:
                is_high_risk = True
                anomalies.append({
                    "severity": "CRITICAL",
                    "code": "BENEFICIARY_NAME_MISMATCH",
                    "description": (
                        f"Ownership mismatch: Invoicing supplier is '{company_name}', "
                        f"but registered bank beneficiary account holder is '{beneficiary}'. "
                        f"Direct liability exposure to invalid third-party payment."
                    )
                })

        return {
            "status": "COUNTERPARTY_ALERT" if is_high_risk else "COUNTERPARTY_VERIFIED",
            "iban_masked": f"{iban[:4]} •••• •••• {iban[-4:]}" if len(iban) >= 8 else iban,
            "iban_country": country_code,
            "bank_name": bank_name,
            "beneficiary_name": beneficiary,
            "has_critical_discrepancy": is_high_risk,
            "anomalies": anomalies
        }

    @staticmethod
    def generate_erp_integration_payload(company_profile: Dict[str, Any], audit_verdict: str) -> Dict[str, Any]:
        """
        Produces production-ready API payloads for enterprise ERPs (SAP Ariba, Coupa, Oracle Fusion)
        to trigger automated supplier holds or enhanced due diligence workflows.
        """
        vendor_id = company_profile.get("cif", "VND-UNKNOWN")
        company_name = company_profile.get("company_name", "Supplier")

        is_freeze = "FREEZE" in audit_verdict or "DISQUALIFICATION" in audit_verdict

        return {
            "sap_ariba_payload": {
                "event": "SupplierRiskStatusUpdated",
                "vendorId": vendor_id,
                "vendorName": company_name,
                "action": "FREEZE_PAYMENT_AND_PURCHASE_ORDERS" if is_freeze else "ENHANCED_DUE_DILIGENCE_REQUIRED",
                "riskLevel": "CRITICAL" if is_freeze else "MEDIUM",
                "reason": "DeepAudit Autonomous Risk Engine: Non-accredited certs / Counterparty mismatch / Solvency alert",
                "lockBankDetails": True if is_freeze else False,
                "timestamp": "2026-10-24T17:15:00Z"
            },
            "coupa_payload": {
                "supplier": {
                    "number": vendor_id,
                    "name": company_name,
                    "status": "inactive" if is_freeze else "under_review",
                    "hold_invoices": is_freeze,
                    "custom_fields": {
                        "deepaudit_flag": "QUARANTINED" if is_freeze else "REVIEW"
                    }
                }
            },
            "actionable_due_diligence_steps": [
                "1. Formal notification of precautionary payment freeze under UCC / civil contract protections.",
                "2. Demand for certified bank ownership certificate bearing official bank branch seal.",
                "3. Electronic validation via ENAC portal of official ISO accreditation and good-standing tax certificates."
            ]
        }
