"""
Unit and regression tests for DeepAudit Forensic Engine & Benchmark Suite.
"""

import pytest
from deepaudit.forensic_engine import ForensicEngine, clean_amount
from deepaudit.compliance_engine import ComplianceEngine
from deepaudit.benchmark_suite import DeepAuditBenchmarkSuite
from deepaudit.test_cases import AUDIT_TEST_CASES


def test_clean_amount():
    assert clean_amount("$1,234.56") == 1234.56
    assert clean_amount("EUR 50,000.00") == 50000.00
    assert clean_amount("1.234,56 €") == 1234.56
    assert clean_amount(1500) == 1500.0


def test_altman_z_score_calculation():
    fe = ForensicEngine()
    # Solaria clean energy: safe zone financials
    case = AUDIT_TEST_CASES["solaria_energy"]["financials"]
    res = fe.calculate_altman_z_score(case)
    assert res["zone"] == "SAFE_ZONE"
    assert res["z_score"] > 2.6

    # Iberia logistics: distress zone financials
    distress_case = AUDIT_TEST_CASES["iberia_logistics"]["financials"]
    distress_res = fe.calculate_altman_z_score(distress_case)
    assert distress_res["zone"] == "DISTRESS_ZONE"
    assert distress_res["z_score"] < 1.1


def test_benford_law_detection():
    fe = ForensicEngine()
    # Anomaly distribution
    irregular_amounts = [9800.0, 9900.0, 9950.0, 9850.0, 9999.0] * 5
    res = fe.analyze_benford(irregular_amounts)
    assert res["chi_square_statistic"] > 15.0 or res["risk_classification"] in ("ANOMALY_DETECTED", "HIGH_RISK")


def test_compliance_engine():
    # Expired certs in Iberia Logistics
    case = AUDIT_TEST_CASES["iberia_logistics"]
    audit = ComplianceEngine.audit_certifications(case)
    assert any(c["status"] == "EXPIRED" for c in audit["certifications"])
    assert audit["labor_safety_audit"]["itss_sanctions_count"] >= 1


def test_benchmark_suite_backtest():
    res = DeepAuditBenchmarkSuite.run_backtest()
    assert res["total_benchmark_cases"] == 5
    assert res["metrics"]["precision"] == 1.0
    assert res["metrics"]["recall"] == 1.0
    assert res["metrics"]["f1_score"] == 1.0
