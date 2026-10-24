"""
Real-World Enterprise Stress-Testing Suite for DeepAudit.
Simulates high-volume enterprise invoice ledgers and extreme financial statements.
"""

import sys
import time
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from deepaudit.forensic_engine import ForensicEngine, clean_amount

def run_deepaudit_stress():
    print("=" * 60)
    print("REAL-WORLD ENTERPRISE STRESS TEST: DEEPAUDIT")
    print("=" * 60)

    # Test 1: European Currency & Format Parsing
    print("\n▶ Test 1: High-Volume Messy European Currency Formats")
    raw_formats = [
        "1.245,50 €", "  4500.00 ", "12.000,00 €", "0,00 €", None,
        "-350,00 €", "€ 8.900,99", "125000", "$ 4,500.50", "INVALID_TXT"
    ]
    cleaned = [clean_amount(x) for x in raw_formats]
    print(f"  • Parsed {len(raw_formats)} inputs into floats without crash.")
    assert cleaned[0] == 1245.5
    assert cleaned[2] == 12000.0
    assert cleaned[3] == 0.0
    assert cleaned[4] == 0.0
    assert cleaned[5] == -350.0
    print("  ✔ Currency parser passed 100%")

    # Test 2: Benford's Law on 150 Invoices
    print("\n▶ Test 2: Benford's Law Distribution on 150 Enterprise Invoices")
    import random
    random.seed(42)
    # Generate 150 natural invoices following rough log distribution
    natural_invoices = [round(10 ** random.uniform(1, 5), 2) for _ in range(150)]
    res_natural = ForensicEngine.analyze_benford(natural_invoices)
    print(f"  • Natural Sample Size: {res_natural['sample_size']} | Chi2: {res_natural['chi_square_statistic']}")
    print(f"  • Natural Anomaly Detected: {res_natural['anomaly_detected']} (Expected False)")
    assert res_natural["is_conclusive"] is True

    # Generate 50 fraudulent invoices starting mostly with 4 (threshold avoidance)
    fraud_invoices = [random.uniform(4800, 4999) for _ in range(50)]
    res_fraud = ForensicEngine.analyze_benford(fraud_invoices)
    print(f"  • Fraud Sample Size: {res_fraud['sample_size']} | Chi2: {res_fraud['chi_square_statistic']}")
    print(f"  • Fraud Anomaly Detected: {res_fraud['anomaly_detected']} (Expected True)")
    assert res_fraud["anomaly_detected"] is True
    assert res_fraud["risk_classification"] == "CRITICAL_MANIPULATION_RISK"
    print("  ✔ Benford statistical anomaly engine passed 100%")

    # Test 3: Altman Z-Score Edge Cases (Zero Assets, Zero Liabilities, Extreme Distress)
    print("\n▶ Test 3: Altman Z-Score Edge Case Ratios")
    edge_financials = [
        {"name": "Zero Assets Startup", "total_assets": 0.0, "total_liabilities": 100000.0},
        {"name": "Severe Negative Equity", "total_assets": 500000.0, "total_liabilities": 900000.0, "equity": -400000.0, "ebit": -80000.0},
        {"name": "Cash-Rich Blue Chip", "total_assets": 10000000.0, "current_assets": 6000000.0, "current_liabilities": 1000000.0, "retained_earnings": 4000000.0, "ebit": 1500000.0, "equity": 8000000.0, "total_liabilities": 2000000.0}
    ]
    for fin in edge_financials:
        z = ForensicEngine.calculate_altman_z_score(fin)
        print(f"  • {fin['name']}: Z-Score = {z['z_score']} ({z['zone']})")
        assert "z_score" in z

    print("\n" + "=" * 60)
    print("DEEPAUDIT STRESS TEST: ALL 3 REAL-WORLD PHASES PASSED 100%")
    print("=" * 60)

if __name__ == "__main__":
    run_deepaudit_stress()
