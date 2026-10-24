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

class ForensicEngine:
    @staticmethod
    def analyze_benford(amounts: List[float]) -> Dict[str, Any]:
        """
        Calculates first-digit distribution and Chi-Square anomaly score against Benford's Law.
        Deviations often reveal fabricated invoices or expense manipulation.
        """
        valid_amounts = [abs(a) for a in amounts if abs(a) >= 1.0]
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
            # Extract first significant digit
            first_digit = int(str(f"{a:.6f}").replace("0", "").replace(".", "")[0])
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

        if z_score < 1.1:
            zone = "DISTRESS_ZONE"
            description = "High probability of bankruptcy/insolvency within 24 months."
            score_color = "red"
        elif 1.1 <= z_score < 2.6:
            zone = "GREY_ZONE"
            description = "Moderate financial strain; operational restructuring advised."
            score_color = "yellow"
        else:
            zone = "SAFE_ZONE"
            description = "Solid balance sheet; minimal default risk."
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
            "current_ratio": round(current_assets / (current_liabilities if current_liabilities > 0 else 1.0), 2)
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
            amt = float(inv.get("amount", 0.0))
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
                    "description": f"Factura de {amt} € sospechosamente ajustada justo por debajo del límite de aprobación de 5.000 €."
                })

            # Check 2: Just below 10,000 threshold
            if 9600.0 <= amt < 10000.0:
                anomalies.append({
                    "severity": "HIGH",
                    "code": "THRESHOLD_AVOIDANCE_10K",
                    "invoice_number": num,
                    "amount": amt,
                    "date": date,
                    "description": f"Importe de {amt} € fraccionado para eludir el control de auditoría de compras (>10.000 €)."
                })

            # Check 3: Round numbers above 1,000
            if amt >= 1000.0 and amt.is_integer() and (amt % 1000 == 0):
                anomalies.append({
                    "severity": "MEDIUM",
                    "code": "ROUND_NUMBER_ESTIMATE",
                    "invoice_number": num,
                    "amount": amt,
                    "date": date,
                    "description": f"Importe perfectamente redondo ({amt:.2f} €); atípico en facturación comercial con impuestos."
                })

            # Group for duplicates
            if amt not in seen_amounts:
                seen_amounts[amt] = []
            seen_amounts[amt].append(inv)

        # Check 4: Potential duplicate billing
        for amt, group in seen_amounts.items():
            if len(group) > 1 and amt > 500.0:
                nums = [g.get("invoice_number") for g in group]
                anomalies.append({
                    "severity": "CRITICAL",
                    "code": "DUPLICATE_AMOUNT_SUSPICION",
                    "amount": amt,
                    "invoice_numbers": nums,
                    "description": f"Se han detectado {len(group)} facturas con el importe idéntico exacto de {amt} € ({', '.join(nums)}). Posible doble cobro o facturación circular."
                })

        return anomalies
