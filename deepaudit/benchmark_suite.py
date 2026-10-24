"""
Quantitative Forensic Benchmark & Ground-Truth Backtest Engine for DeepAudit.
Evaluates detection precision, recall, and false-positive elimination across
canonical corporate risk profiles.
"""

from typing import Dict, Any, List
from deepaudit.forensic_engine import ForensicEngine, clean_amount
from deepaudit.compliance_engine import ComplianceEngine
from deepaudit.test_cases import AUDIT_TEST_CASES

class DeepAuditBenchmarkSuite:
    """
    Executes a formal statistical backtest across reference supplier ground-truth profiles.
    """
    
    GROUND_TRUTH = {
        "iberia_logistics": {"label": "FRAUD_OR_DISTRESS", "expected_verdict": "BLOQUEO Y RECHAZO"},
        "solaria_energy": {"label": "HEALTHY_SOLVENT", "expected_verdict": "APROBADO"},
        "nexus_tech": {"label": "SHELL_HIGH_RISK", "expected_verdict": "SUPERVISIÓN REFORZADA"},
        "trans_express_logistics": {"label": "HEALTHY_SOLVENT", "expected_verdict": "APROBADO"},
        "medtech_iberica": {"label": "FRAUD_OR_DISTRESS", "expected_verdict": "BLOQUEO Y RECHAZO"}
    }

    @classmethod
    def run_backtest(cls) -> Dict[str, Any]:
        engine = ForensicEngine()
        results = []
        
        tp = fp = tn = fn = 0
        ccc_false_positives_prevented = 0
        
        for case_id, case in AUDIT_TEST_CASES.items():
            financials = case.get("financials", {})
            invoices = case.get("invoices", [])
            amounts = [clean_amount(inv.get("amount", 0.0)) for inv in invoices]
            
            # Step 1: Benford
            benford = engine.analyze_benford(amounts)
            # Step 2: Altman Z'' with CCC
            altman = engine.calculate_altman_z_score(financials)
            # Step 3: Irregularities
            irregs = engine.detect_invoice_irregularities(invoices)
            # Step 4: Counterparty
            counterparty = engine.verify_payment_counterparty(case)
            # Step 5: Compliance
            compliance = ComplianceEngine.audit_certifications(case)
            
            # Compute heuristic score
            risk = 0.0
            if altman["zone"] == "DISTRESS_ZONE":
                risk += 45.0
            elif altman["zone"] == "GREY_ZONE":
                risk += 20.0
            
            # Track CCC correction effect
            if case_id == "trans_express_logistics":
                # Without CCC, negative working capital (-160k) would trigger distress zone in naive models
                if altman["zone"] != "DISTRESS_ZONE":
                    ccc_false_positives_prevented += 1
            
            if benford.get("anomaly_detected"):
                risk += 25.0
            if len(irregs) > 0:
                risk += min(len(irregs) * 8.0, 30.0)
            if counterparty.get("has_critical_discrepancy"):
                risk += 35.0
            if compliance.get("compliance_score", 100) < 50:
                risk += 30.0
                
            risk_score = min(round(risk), 98) if risk > 0 else 12
            predicted_verdict = "BLOQUEO Y RECHAZO" if risk_score >= 85 else ("SUPERVISIÓN REFORZADA" if risk_score >= 40 else "APROBADO")
            
            gt = cls.GROUND_TRUTH.get(case_id, {"label": "UNKNOWN"})
            is_positive = (gt["label"] != "HEALTHY_SOLVENT")
            is_predicted_positive = (predicted_verdict != "APROBADO")
            
            if is_positive and is_predicted_positive:
                tp += 1
            elif not is_positive and is_predicted_positive:
                fp += 1
            elif not is_positive and not is_predicted_positive:
                tn += 1
            elif is_positive and not is_predicted_positive:
                fn += 1
                
            results.append({
                "case_id": case_id,
                "company_name": case["company_name"],
                "sector": case["sector"],
                "risk_score": risk_score,
                "predicted_verdict": predicted_verdict,
                "expected_verdict": gt.get("expected_verdict"),
                "ground_truth_label": gt["label"],
                "altman_zone": altman["zone"],
                "benford_chi2": benford.get("chi_square_statistic"),
                "match": (predicted_verdict == gt.get("expected_verdict"))
            })
            
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 1.0
        accuracy = (tp + tn) / len(AUDIT_TEST_CASES)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        
        return {
            "total_benchmark_cases": len(AUDIT_TEST_CASES),
            "metrics": {
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1_score": round(f1_score, 4),
                "accuracy": round(accuracy, 4),
                "false_positive_rate": round(fpr, 4),
                "ccc_false_positives_prevented": ccc_false_positives_prevented
            },
            "confusion_matrix": {
                "true_positives": tp,
                "false_positives": fp,
                "true_negatives": tn,
                "false_negatives": fn
            },
            "detailed_case_evaluations": results
        }

if __name__ == "__main__":
    res = DeepAuditBenchmarkSuite.run_backtest()
    import json
    print(json.dumps(res, indent=2))
