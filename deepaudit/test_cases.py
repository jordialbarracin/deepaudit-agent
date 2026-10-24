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
            "revenue": 845000.0
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
            {"invoice_number": "IB-2026-140", "amount": 4990.00, "date": "2026-10-07", "concept": "Sobrecarga de combustible y peajes"}
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
        "invoices": [
            {"invoice_number": "NEX-01", "amount": 10000.00, "date": "2026-07-15", "concept": "Asesoramiento estratégico inicial"},
            {"invoice_number": "NEX-02", "amount": 10000.00, "date": "2026-08-01", "concept": "Auditoría de sistemas y arquitectura de nube"},
            {"invoice_number": "NEX-03", "amount": 10000.00, "date": "2026-08-20", "concept": "Desarrollo de módulos de integración"},
            {"invoice_number": "NEX-04", "amount": 15000.00, "date": "2026-09-10", "concept": "Consultoría de transformación digital"},
            {"invoice_number": "NEX-05", "amount": 5000.00, "date": "2026-09-25", "concept": "Soporte y formación de personal"}
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
