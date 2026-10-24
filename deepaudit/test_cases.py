"""
Canonical Corporate & Vendor Audit Test Cases for DeepAudit.
Represents real-world balance sheets, invoice ledgers, and supplier profiles.
"""

from typing import Dict, Any, List

AUDIT_TEST_CASES: Dict[str, Dict[str, Any]] = {
    "iberia_logistics": {
        "id": "iberia_logistics",
        "company_name": "Iberia Global Logistics Ltd",
        "cif": "B-87654321",
        "sector": "Heavy Freight Transport & Logistics",
        "annual_volume_invoiced": "845,000 EUR",
        "description": "Routine freight logistics contractor. Audited due to repeated invoice factoring advances and liquidity warnings.",
        "financials": {
            "total_assets": 450000.0,
            "current_assets": 110000.0,
            "current_liabilities": 390000.0,
            "total_liabilities": 580000.0,
            "retained_earnings": -140000.0,
            "ebit": -35000.0,
            "equity": -130000.0,
            "revenue": 845000.0,
            "cogs": 620000.0,
            "accounts_receivable": 45000.0,
            "accounts_payable": 280000.0,
            "inventory": 0.0
        },
        "bank_account": {
            "iban": "LT89 3704 0044 0532 0130",
            "bank_name": "Revolut Payments Lithuania",
            "beneficiary_name": "Iberia Global Holding Ltd (Malta)"
        },
        "certifications": {
            "iso_9001": {"issuer": "AENOR", "certificate_id": "ER-0412/2018", "expires_at": "2026-05-15", "fraudulent_unaccredited": False},
            "iso_27001": {"issuer": "Unaccredited Web Seal", "certificate_id": "FAKE-ISMS-2024", "expires_at": "2027-01-01", "fraudulent_unaccredited": True}
        },
        "labor_safety": {
            "prl_service_type": "External Prevention Service (SPA)",
            "spa_provider": "Mediterranean Health & Safety Ltd (Contract Expired)",
            "itss_sanctions_count": 2,
            "itss_sanctions_amount_eur": 48500.0,
            "accident_frequency_index": "Severe (+34% above sector benchmark)"
        },
        "invoices": [
            {"invoice_number": "IB-2026-081", "amount": 4950.00, "date": "2026-09-02", "concept": "Urgent freight transport Madrid-Valencia"},
            {"invoice_number": "IB-2026-082", "amount": 4920.00, "date": "2026-09-04", "concept": "Overnight freight consolidation service"},
            {"invoice_number": "IB-2026-089", "amount": 4980.00, "date": "2026-09-08", "concept": "Special refrigerated container freight"},
            {"invoice_number": "IB-2026-095", "amount": 9950.00, "date": "2026-09-12", "concept": "Logistics hub distribution operations south"},
            {"invoice_number": "IB-2026-104", "amount": 7500.00, "date": "2026-09-15", "concept": "Intermodal transport forwarding service"},
            {"invoice_number": "IB-2026-105", "amount": 7500.00, "date": "2026-09-15", "concept": "Intermodal transport duplicate billing invoice"},
            {"invoice_number": "IB-2026-112", "amount": 4890.00, "date": "2026-09-20", "concept": "Palletized cargo north branch dispatch"},
            {"invoice_number": "IB-2026-118", "amount": 4910.00, "date": "2026-09-23", "concept": "Last-mile courier fulfillment routing"},
            {"invoice_number": "IB-2026-125", "amount": 8400.00, "date": "2026-09-27", "concept": "Long-haul cross-border transit haulage"},
            {"invoice_number": "IB-2026-130", "amount": 4975.00, "date": "2026-09-30", "concept": "Supplementary heavy semi-trailer lease"},
            {"invoice_number": "IB-2026-134", "amount": 3200.00, "date": "2026-10-03", "concept": "Harbor terminal container stevedoring"},
            {"invoice_number": "IB-2026-140", "amount": 4990.00, "date": "2026-10-07", "concept": "Fuel surcharge & toll highway tariffs"},
            {"invoice_number": "IB-2026-141", "amount": 2850.00, "date": "2026-10-11", "time": "03:14:22", "concept": "Saturday off-hours night discharge Algeciras", "pod_verified": True, "pod_timestamp": "2026-10-11T02:51:00Z"}
        ]
    },

    "solaria_energy": {
        "id": "solaria_energy",
        "company_name": "Solaria Clean Energy Solutions Ltd",
        "cif": "B-99887766",
        "sector": "Renewable Energy & Industrial Engineering",
        "annual_volume_invoiced": "2,450,000 EUR",
        "description": "Prime EPC contractor for commercial rooftop solar plant installation. Subject to proactive vendor vetting prior to framework agreement signing.",
        "financials": {
            "total_assets": 3200000.0,
            "current_assets": 1950000.0,
            "current_liabilities": 680000.0,
            "total_liabilities": 920000.0,
            "retained_earnings": 850000.0,
            "ebit": 420000.0,
            "equity": 2280000.0,
            "revenue": 2450000.0
        },
        "bank_account": {
            "iban": "ES44 2100 0418 4502 0005 1122",
            "bank_name": "CaixaBank",
            "beneficiary_name": "Solaria Clean Energy Solutions Ltd"
        },
        "certifications": {
            "iso_27001": {"issuer": "AENOR", "certificate_id": "SI-0098/2023", "expires_at": "2027-11-20", "fraudulent_unaccredited": False},
            "iso_9001": {"issuer": "AENOR", "certificate_id": "ER-1244/2021", "expires_at": "2027-06-15", "fraudulent_unaccredited": False},
            "iso_14001": {"issuer": "Bureau Veritas", "certificate_id": "ES119842", "expires_at": "2027-09-30", "fraudulent_unaccredited": False},
            "iso_45001": {"issuer": "AENOR", "certificate_id": "SST-0044/2022", "expires_at": "2028-02-14", "fraudulent_unaccredited": False}
        },
        "labor_safety": {
            "prl_service_type": "Joint Occupational Safety Service",
            "spa_provider": "Quiron Risk Prevention Group",
            "itss_sanctions_count": 0,
            "itss_sanctions_amount_eur": 0.0,
            "accident_frequency_index": "Low (0 workplace incidents in past 24 months)"
        },
        "invoices": [
            {"invoice_number": "SOL-26-001", "amount": 14230.50, "date": "2026-05-10", "concept": "Topographical survey and plant engineering design"},
            {"invoice_number": "SOL-26-015", "amount": 28450.00, "date": "2026-06-02", "concept": "Supply of three-phase utility grid inverters"},
            {"invoice_number": "SOL-26-024", "amount": 7890.25, "date": "2026-06-18", "concept": "Anodized aluminum mounting substructures"},
            {"invoice_number": "SOL-26-033", "amount": 62100.00, "date": "2026-07-05", "concept": "Milestone 1: Monocrystalline PV solar module shipment"},
            {"invoice_number": "SOL-26-041", "amount": 19350.80, "date": "2026-08-12", "concept": "Solar cabling and DC protection switchboards"},
            {"invoice_number": "SOL-26-050", "amount": 34120.00, "date": "2026-09-01", "concept": "Milestone 2: Electromechanical installation"},
            {"invoice_number": "SOL-26-058", "amount": 11500.40, "date": "2026-09-22", "concept": "Regulatory inspection & grid compliance filing"},
            {"invoice_number": "SOL-26-065", "amount": 5420.00, "date": "2026-10-04", "concept": "SCADA system telemetry commissioning"}
        ]
    },

    "nexus_tech": {
        "id": "nexus_tech",
        "company_name": "Nexus Tech Ventures Ltd",
        "cif": "B-11223344",
        "sector": "IT & Strategic Digital Advisory",
        "annual_volume_invoiced": "120,000 EUR",
        "description": "Newly established vendor requesting expedited onboarding with identical round-number invoices and zero verified corporate history.",
        "financials": {
            "total_assets": 12000.0,
            "current_assets": 8500.0,
            "current_liabilities": 7000.0,
            "total_liabilities": 9000.0,
            "retained_earnings": 1000.0,
            "ebit": 1500.0,
            "equity": 3000.0,
            "revenue": 120000.0
        },
        "certifications": {
            "iso_27001": {"issuer": "SGS", "certificate_id": "ES24/0912", "expires_at": "2026-11-28", "fraudulent_unaccredited": False}
        },
        "labor_safety": {
            "prl_service_type": "External Prevention Service (SPA)",
            "spa_provider": "Apex Occupational Health Ltd",
            "itss_sanctions_count": 0,
            "itss_sanctions_amount_eur": 0.0,
            "accident_frequency_index": "N/A (Micro-enterprise headcount < 5)"
        },
        "invoices": [
            {"invoice_number": "NEX-01", "amount": 10000.00, "date": "2026-07-15", "concept": "Initial strategic digital consulting"},
            {"invoice_number": "NEX-02", "amount": 10000.00, "date": "2026-08-01", "concept": "Cloud architecture systems audit"},
            {"invoice_number": "NEX-03", "amount": 10000.00, "date": "2026-08-20", "concept": "Integration connector module development"},
            {"invoice_number": "NEX-04", "amount": 15000.00, "date": "2026-09-10", "concept": "Executive digital transformation advisory"},
            {"invoice_number": "NEX-05", "amount": 5000.00, "date": "2026-09-25", "concept": "Staff enablement & training delivery"}
        ]
    },

    "trans_express_logistics": {
        "id": "trans_express_logistics",
        "company_name": "Trans-Express Freight & Logistics Ltd",
        "cif": "B-55443322",
        "sector": "Asset-Light Courier Logistics & Forwarding",
        "annual_volume_invoiced": "3,100,000 EUR",
        "description": "High-velocity asset-light courier SME. Operates with structural negative working capital due to business model (receives receivables in 30 days, settles sub-contractor payables in 85 days). Canonical benchmark to test false-positive avoidance.",
        "financials": {
            "total_assets": 1100000.0,
            "current_assets": 380000.0,
            "current_liabilities": 540000.0,
            "total_liabilities": 650000.0,
            "retained_earnings": 280000.0,
            "ebit": 165000.0,
            "equity": 450000.0,
            "revenue": 3100000.0,
            "cogs": 2200000.0,
            "accounts_receivable": 255000.0,
            "accounts_payable": 510000.0,
            "inventory": 0.0
        },
        "bank_account": {
            "iban": "ES82 0049 1500 0512 3456 7890",
            "bank_name": "Banco Santander",
            "beneficiary_name": "Trans-Express Freight & Logistics Ltd"
        },
        "certifications": {
            "iso_9001": {"issuer": "AENOR", "certificate_id": "ER-1845/2020", "expires_at": "2027-04-10", "fraudulent_unaccredited": False},
            "iso_14001": {"issuer": "Applus+", "certificate_id": "MA-0922/2021", "expires_at": "2027-08-15", "fraudulent_unaccredited": False}
        },
        "labor_safety": {
            "prl_service_type": "External Prevention Service (SPA)",
            "spa_provider": "Cualtis Occupational Health Ltd",
            "itss_sanctions_count": 0,
            "itss_sanctions_amount_eur": 0.0,
            "accident_frequency_index": "Normal (Within logistics industry average)"
        },
        "invoices": [
            {"invoice_number": "TE-901", "amount": 12450.00, "date": "2026-08-01", "concept": "Last-mile courier routes Madrid North"},
            {"invoice_number": "TE-905", "amount": 18230.00, "date": "2026-08-15", "concept": "Summer campaign express delivery surge"},
            {"invoice_number": "TE-912", "amount": 14780.00, "date": "2026-09-02", "concept": "Automotive spare parts B2B courier"},
            {"invoice_number": "TE-920", "amount": 21500.00, "date": "2026-09-18", "concept": "Overnight trunk line transfer Barcelona"},
            {"invoice_number": "TE-931", "amount": 16900.00, "date": "2026-10-05", "concept": "Long-distance freight transfer Algeciras-Zaragoza"}
        ]
    },

    "medtech_iberica": {
        "id": "medtech_iberica",
        "company_name": "MedTech Hospital Supplies Ltd",
        "cif": "B-77665544",
        "sector": "Medical Devices & Hospital Supply Procurement",
        "annual_volume_invoiced": "1,850,000 EUR",
        "description": "Public tender medical equipment supplier. Flagged for expired ISO medical quality seals and active public tax debt enforcement notices.",
        "financials": {
            "total_assets": 980000.0,
            "current_assets": 410000.0,
            "current_liabilities": 720000.0,
            "total_liabilities": 890000.0,
            "retained_earnings": -45000.0,
            "ebit": -12000.0,
            "equity": 90000.0,
            "revenue": 1850000.0,
            "cogs": 1350000.0,
            "accounts_receivable": 210000.0,
            "accounts_payable": 610000.0,
            "inventory": 85000.0
        },
        "bank_account": {
            "iban": "ES12 0182 2200 4501 2345 6789",
            "bank_name": "BBVA",
            "beneficiary_name": "MedTech Hospital Supplies Ltd"
        },
        "certifications": {
            "iso_9001": {"issuer": "TÜV Rheinland", "certificate_id": "TR-0914-ES", "expires_at": "2023-12-31", "fraudulent_unaccredited": False},
            "iso_27001": {"issuer": "Unaccredited Web Seal", "certificate_id": "FAKE-SEC-01", "expires_at": "2027-01-01", "fraudulent_unaccredited": True}
        },
        "labor_safety": {
            "prl_service_type": "External Prevention Service",
            "spa_provider": "Vanguard Risk Management Ltd",
            "itss_sanctions_count": 1,
            "itss_sanctions_amount_eur": 12500.0,
            "accident_frequency_index": "Moderate"
        },
        "invoices": [
            {"invoice_number": "MED-101", "amount": 9980.00, "date": "2026-07-10", "concept": "Clinical laboratory reagent batch delivery"},
            {"invoice_number": "MED-102", "amount": 9940.00, "date": "2026-07-18", "concept": "Sterile surgical consumables replenishment"},
            {"invoice_number": "MED-110", "amount": 15400.00, "date": "2026-08-05", "concept": "Patient vitals monitoring equipment unit"},
            {"invoice_number": "MED-119", "amount": 9920.00, "date": "2026-08-22", "concept": "Electrosurgical replacement modules"},
            {"invoice_number": "MED-125", "amount": 24800.00, "date": "2026-09-14", "concept": "Annual preventive autoclave maintenance"}
        ]
    }
}

def get_case(case_id: str) -> Dict[str, Any]:
    return AUDIT_TEST_CASES.get(case_id, AUDIT_TEST_CASES["iberia_logistics"])

def list_cases() -> List[Dict[str, Any]]:
    return [
        {
            "id": c["id"],
            "company_name": c["company_name"],
            "cif": c["cif"],
            "sector": c["sector"],
            "annual_volume_invoiced": c["annual_volume_invoiced"],
            "description": c["description"]
        }
        for c in AUDIT_TEST_CASES.values()
    ]
