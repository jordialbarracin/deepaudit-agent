"""
Canonical Corporate & Vendor Audit Test Cases for DeepAudit.
Represents real-world balance sheets, invoice ledgers, and supplier profiles.
"""

from typing import Dict, Any, List

AUDIT_TEST_CASES: Dict[str, Dict[str, Any]] = {
    "iberia_logistics": {
        "id": "iberia_logistics",
        "company_name": "Iberia Logistics Global SL",
        "cif": "B-87654321",
        "sector": "Transporte y Logística de Carga",
        "annual_volume_invoiced": "845.000 €",
        "description": "Proveedor habitual de transporte logístico. Se audita por reiteradas solicitudes de anticipo de facturas y sospecha de solvencia.",
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
            "iso_27001": {"issuer": "Self-Declared Web Sello", "certificate_id": "FAKE-ISMS-2024", "expires_at": "2027-01-01", "fraudulent_unaccredited": True}
        },
        "labor_safety": {
            "prl_service_type": "Servicio de Prevención Ajeno (SPA)",
            "spa_provider": "Prevención Mediterránea SL (Contrato Vencido)",
            "itss_sanctions_count": 2,
            "itss_sanctions_amount_eur": 48500.0,
            "accident_frequency_index": "Severo (+34% sobre media sectorial)"
        },
        "invoices": [
            {"invoice_number": "IB-2026-081", "amount": 4950.00, "date": "2026-09-02", "concept": "Porte urgente Madrid-Valencia"},
            {"invoice_number": "IB-2026-082", "amount": 4920.00, "date": "2026-09-04", "concept": "Servicio de consolidación nocturno"},
            {"invoice_number": "IB-2026-089", "amount": 4980.00, "date": "2026-09-08", "concept": "Flete especial refrigerado"},
            {"invoice_number": "IB-2026-095", "amount": 9950.00, "date": "2026-09-12", "concept": "Operativa logística centro sur"},
            {"invoice_number": "IB-2026-104", "amount": 7500.00, "date": "2026-09-15", "concept": "Servicio de transporte intermodal"},
            {"invoice_number": "IB-2026-105", "amount": 7500.00, "date": "2026-09-15", "concept": "Servicio de transporte intermodal duplicado"},
            {"invoice_number": "IB-2026-112", "amount": 4890.00, "date": "2026-09-20", "concept": "Carga paletizada delegación norte"},
            {"invoice_number": "IB-2026-118", "amount": 4910.00, "date": "2026-09-23", "concept": "Distribución capilar última milla"},
            {"invoice_number": "IB-2026-125", "amount": 8400.00, "date": "2026-09-27", "concept": "Transporte de largo recorrido"},
            {"invoice_number": "IB-2026-130", "amount": 4975.00, "date": "2026-09-30", "concept": "Alquiler de semirremolque refuerzo"},
            {"invoice_number": "IB-2026-134", "amount": 3200.00, "date": "2026-10-03", "concept": "Descarga de contenedores puerto"},
            {"invoice_number": "IB-2026-140", "amount": 4990.00, "date": "2026-10-07", "concept": "Sobrecarga de combustible y peajes"},
            {"invoice_number": "IB-2026-141", "amount": 2850.00, "date": "2026-10-11", "time": "03:14:22", "concept": "Descarga nocturna sábado delegación Algeciras", "pod_verified": True, "pod_timestamp": "2026-10-11T02:51:00Z"}
        ]
    },

    "solaria_energy": {
        "id": "solaria_energy",
        "company_name": "Solaria Energy Soluciones SL",
        "cif": "B-99887766",
        "sector": "Instalaciones de Energías Renovables e Ingeniería",
        "annual_volume_invoiced": "2.450.000 €",
        "description": "Proveedor adjudicatario de la instalación fotovoltaica industrial. Se somete a due diligence preventiva previa a la firma del contrato marco.",
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
            "beneficiary_name": "Solaria Energy Soluciones SL"
        },
        "certifications": {
            "iso_27001": {"issuer": "AENOR", "certificate_id": "SI-0098/2023", "expires_at": "2027-11-20", "fraudulent_unaccredited": False},
            "iso_9001": {"issuer": "AENOR", "certificate_id": "ER-1244/2021", "expires_at": "2027-06-15", "fraudulent_unaccredited": False},
            "iso_14001": {"issuer": "Bureau Veritas", "certificate_id": "ES119842", "expires_at": "2027-09-30", "fraudulent_unaccredited": False},
            "iso_45001": {"issuer": "AENOR", "certificate_id": "SST-0044/2022", "expires_at": "2028-02-14", "fraudulent_unaccredited": False}
        },
        "labor_safety": {
            "prl_service_type": "Servicio de Prevención Mancomunado",
            "spa_provider": "Quirónprevención SLU",
            "itss_sanctions_count": 0,
            "itss_sanctions_amount_eur": 0.0,
            "accident_frequency_index": "Bajo (0 accidentes en últimos 24 meses)"
        },
        "invoices": [
            {"invoice_number": "SOL-26-001", "amount": 14230.50, "date": "2026-05-10", "concept": "Estudio topográfico y diseño de planta"},
            {"invoice_number": "SOL-26-015", "amount": 28450.00, "date": "2026-06-02", "concept": "Suministro de inversores trifásicos"},
            {"invoice_number": "SOL-26-024", "amount": 7890.25, "date": "2026-06-18", "concept": "Estructuras de soporte en aluminio anodizado"},
            {"invoice_number": "SOL-26-033", "amount": 62100.00, "date": "2026-07-05", "concept": "Hito 1: Entrega de módulos fotovoltaicos monocristalinos"},
            {"invoice_number": "SOL-26-041", "amount": 19350.80, "date": "2026-08-12", "concept": "Cableado solar y protecciones de continua"},
            {"invoice_number": "SOL-26-050", "amount": 34120.00, "date": "2026-09-01", "concept": "Hito 2: Montaje electromecánico"},
            {"invoice_number": "SOL-26-058", "amount": 11500.40, "date": "2026-09-22", "concept": "Certificación OCA y legalización de industria"},
            {"invoice_number": "SOL-26-065", "amount": 5420.00, "date": "2026-10-04", "concept": "Puesta en marcha y telemetría SCADA"}
        ]
    },

    "nexus_tech": {
        "id": "nexus_tech",
        "company_name": "Nexus Inversiones Tech SL",
        "cif": "B-11223344",
        "sector": "Consultoría y Servicios Tecnológicos",
        "annual_volume_invoiced": "120.000 €",
        "description": "Nueva empresa proveedora que solicita la homologación de urgencia con facturas de importes redondos y sin historial operativo previo.",
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
            "prl_service_type": "Servicio de Prevención Ajeno (SPA)",
            "spa_provider": "Valora Prevención SL",
            "itss_sanctions_count": 0,
            "itss_sanctions_amount_eur": 0.0,
            "accident_frequency_index": "N/A (Plantilla reducida < 5)"
        },
        "invoices": [
            {"invoice_number": "NEX-01", "amount": 10000.00, "date": "2026-07-15", "concept": "Asesoramiento estratégico inicial"},
            {"invoice_number": "NEX-02", "amount": 10000.00, "date": "2026-08-01", "concept": "Auditoría de sistemas y arquitectura de nube"},
            {"invoice_number": "NEX-03", "amount": 10000.00, "date": "2026-08-20", "concept": "Desarrollo de módulos de integración"},
            {"invoice_number": "NEX-04", "amount": 15000.00, "date": "2026-09-10", "concept": "Consultoría de transformación digital"},
            {"invoice_number": "NEX-05", "amount": 5000.00, "date": "2026-09-25", "concept": "Soporte y formación de personal"}
        ]
    },

    "trans_express_logistics": {
        "id": "trans_express_logistics",
        "company_name": "Trans-Express Paquetería Peninsular SL",
        "cif": "B-55443322",
        "sector": "Transporte y Logística Asset-Light",
        "annual_volume_invoiced": "3.100.000 €",
        "description": "PYME logística de paquetería urgente que subcontrata flotas. Presenta fondo de maniobra negativo por modelo operativo (cobra a 30 días, paga a autónomos a 85 días). Test clave para medir la tasa de falsos positivos.",
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
            "beneficiary_name": "Trans-Express Paquetería Peninsular SL"
        },
        "certifications": {
            "iso_9001": {"issuer": "AENOR", "certificate_id": "ER-1845/2020", "expires_at": "2027-04-10", "fraudulent_unaccredited": False},
            "iso_14001": {"issuer": "Applus+", "certificate_id": "MA-0922/2021", "expires_at": "2027-08-15", "fraudulent_unaccredited": False}
        },
        "labor_safety": {
            "prl_service_type": "Servicio de Prevención Ajeno (SPA)",
            "spa_provider": "Cualtis SL",
            "itss_sanctions_count": 0,
            "itss_sanctions_amount_eur": 0.0,
            "accident_frequency_index": "Normal (dentro de media sectorial)"
        },
        "invoices": [
            {"invoice_number": "TE-901", "amount": 12450.00, "date": "2026-08-01", "concept": "Rutas capilares Madrid Norte"},
            {"invoice_number": "TE-905", "amount": 18230.00, "date": "2026-08-15", "concept": "Refuerzo campaña verano"},
            {"invoice_number": "TE-912", "amount": 14780.00, "date": "2026-09-02", "concept": "Distribución B2B automoción"},
            {"invoice_number": "TE-920", "amount": 21500.00, "date": "2026-09-18", "concept": "Servicio nocturno transfer Barcelona"},
            {"invoice_number": "TE-931", "amount": 16900.00, "date": "2026-10-05", "concept": "Larga distancia Algeciras-Zaragoza"}
        ]
    },

    "medtech_iberica": {
        "id": "medtech_iberica",
        "company_name": "MedTech Suministros Hospitalarios SL",
        "cif": "B-77665544",
        "sector": "Distribución Sanitaria y Equipamiento Hospitalario",
        "annual_volume_invoiced": "1.850.000 €",
        "description": "Proveedor sanitario licitador en compras públicas. Alerta de certificación caducada e inclusiones en listas de apremio de la Seguridad Social.",
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
            "beneficiary_name": "MedTech Suministros Hospitalarios SL"
        },
        "certifications": {
            "iso_9001": {"issuer": "TÜV Rheinland", "certificate_id": "TR-0914-ES", "expires_at": "2023-12-31", "fraudulent_unaccredited": False},
            "iso_27001": {"issuer": "Sin Acreditar", "certificate_id": "FAKE-SEC-01", "expires_at": "2027-01-01", "fraudulent_unaccredited": True}
        },
        "labor_safety": {
            "prl_service_type": "Servicio de Prevención Ajeno",
            "spa_provider": "Antea Prevención",
            "itss_sanctions_count": 1,
            "itss_sanctions_amount_eur": 12500.0,
            "accident_frequency_index": "Moderado"
        },
        "invoices": [
            {"invoice_number": "MED-101", "amount": 9980.00, "date": "2026-07-10", "concept": "Suministro reactivos laboratorio"},
            {"invoice_number": "MED-102", "amount": 9940.00, "date": "2026-07-18", "concept": "Material fungible quirúrgico"},
            {"invoice_number": "MED-110", "amount": 15400.00, "date": "2026-08-05", "concept": "Equipamiento de monitorización"},
            {"invoice_number": "MED-119", "amount": 9920.00, "date": "2026-08-22", "concept": "Repuestos de electrobisturí"},
            {"invoice_number": "MED-125", "amount": 24800.00, "date": "2026-09-14", "concept": "Mantenimiento preventivo anual"}
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
