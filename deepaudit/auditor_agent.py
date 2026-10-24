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

FORENSIC_AUDITOR_SYSTEM_PROMPT = """Eres el Socio Director de Auditoría Forense, Due Diligence y Prevención de Delitos Económicos en una firma de primer nivel internacional.
Tu trabajo es auditar proveedores y empresas sospechosas cruzando los datos contables internos con la inteligencia externa en tiempo real.
Eres implacable, técnicamente impecable, riguroso y cuantitativo.
Debes emitir un dictamen formal de Due Diligence estructurado, con:
1. PUNTUACIÓN DE RIESGO CORPORATIVO (0 a 100, donde 0 es solvencia total y 100 es fraude o quiebra inminente).
2. DICTAMEN EJECUTIVO (APROBADO, EN OBSERVACIÓN, o BLOQUEO Y RECHAZO INMEDIATO).
3. MATRIZ DE EVIDENCIAS Y RED FLAGS (internas y externas).
4. CORRELACIÓN FORENSE: Cómo se conectan los datos numéricos internos (Benford, Altman Z, facturas sospechosas) con la realidad externa descubierta por Tavily (BOE, BORM, litigios, registros).
5. RECOMENDACIONES DE MITIGACIÓN Y ACCIÓN INMEDIATA PARA EL DIRECTOR FINANCIERO (CFO).
Responde en un español formal, técnico y contundente."""

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

        company_name = case.get("company_name", "Empresa Auditada")
        cif = case.get("cif", "N/A")
        financials = case.get("financials", {})
        invoices = case.get("invoices", [])

        # Step 1: Internal Quantitative Forensics
        amounts = [clean_amount(inv.get("amount", 0.0)) for inv in invoices]
        benford_res = self.forensic_engine.analyze_benford(amounts)
        altman_res = self.forensic_engine.calculate_altman_z_score(financials)
        irregularities = self.forensic_engine.detect_invoice_irregularities(invoices)

        # Step 2: ISO Standards, Labor Safety (PRL) & Regulatory Compliance
        compliance_res = ComplianceEngine.audit_certifications(case)

        # Step 3: External Web Intelligence via Tavily
        tavily_query = f"{company_name} {cif} concurso acreedores BORM morosidad Hacienda insolvencias ISO prevencion riesgos"
        tavily_res = self.tavily_client.search(tavily_query, search_depth="advanced", max_results=3)

        # Step 4: LLM Synthesis with NVIDIA Nemotron on Nebius
        prompt = f"""
AUDITORÍA FORENSE, COMPLIANCE REGULATORIO Y DUE DILIGENCE DE EMPRESA PROVEEDORA

DATOS DE LA ENTIDAD AUDITADA:
- Razón Social: {company_name}
- NIF/CIF: {cif}
- Sector: {case.get('sector', 'Comercial')}
- Volumen Facturado en Revisión: {case.get('annual_volume_invoiced', 'N/A')}
- Contexto de la Solicitud: {case.get('description', '')}

EVIDENCIAS CUANTITATIVAS INTERNAS (ANÁLISIS DE LIBROS Y FACTURAS):
1. Test de Benford (Detección de Manipulación en Primeros Dígitos de Facturas):
   - Muestra analizada: {benford_res.get('sample_size')} facturas.
   - Estadístico Chi-Cuadrado: {benford_res.get('chi_square_statistic')} (Umbral crítico 95%: 15.51).
   - Diagnóstico Benford: {benford_res.get('risk_classification')}.

2. Modelo Altman Z''-Score (Solvencia y Probabilidad de Quiebra a 24 Meses - PYMES PGC):
   - Z''-Score Calculado: {altman_res.get('z_score')}
   - Clasificación de Zona: {altman_res.get('zone')} ({altman_res.get('description')})
   - Fondo de Maniobra (Capital Circulante): {altman_res.get('working_capital_euros')} €
   - Ratio de Liquidez Corriente: {altman_res.get('current_ratio')}

3. Irregularidades Concretas Detectadas en Facturas:
   - Total anomalías detectadas: {len(irregularities)}
   - Detalle: {json.dumps(irregularities, ensure_ascii=False, indent=2)}

4. Auditoría de Certificaciones Oficiales ISO y Prevención de Riesgos Laborales (PRL):
   - Índice de Cumplimiento Regulatorio: {compliance_res.get('compliance_score')}% ({compliance_res.get('maturity_level')})
   - Estado de Normas ISO: {json.dumps(compliance_res.get('certifications'), ensure_ascii=False, indent=2)}
   - Auditoría de Seguridad Laboral / Sanciones ITSS: {json.dumps(compliance_res.get('labor_safety_audit'), ensure_ascii=False, indent=2)}

EVIDENCIAS EXTERNAS OBTENIDAS EN TIEMPO REAL VÍA TAVILY SEARCH (REGISTROS OFICIALES Y PRENSA):
- Resumen Tavily: {tavily_res.get('answer')}
- Fuentes y Boletines Oficiales Consultados:
{json.dumps(tavily_res.get('results'), ensure_ascii=False, indent=2)}

INSTRUCCIONES DE DICTAMEN:
Emite el Informe Pericial Forense definitivo con:
1. Puntuación de Riesgo de 0 a 100.
2. Dictamen Oficial (APROBADO / SUPERVISIÓN REFORZADA / BLOQUEO Y RECHAZO).
3. Matriz de Banderas Rojas (Red Flags).
4. Correlación entre los números internos y los hallazgos en el BOE/BORM/Tavily.
5. Plan de acción de 4 puntos para compras y tesorería.
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

        # If Tavily found insolvency/concurso
        if "concurso" in tavily_res.get("answer", "").lower() or "morosos" in tavily_res.get("answer", "").lower():
            base_risk = max(base_risk, 88.0)

        risk_score = min(round(base_risk), 98) if base_risk > 0 else 12

        return {
            "company_name": company_name,
            "cif": cif,
            "risk_score": risk_score,
            "risk_level": "CRÍTICO" if risk_score >= 75 else ("MODERADO" if risk_score >= 40 else "BAJO"),
            "forensics": {
                "benford": benford_res,
                "altman_z": altman_res,
                "irregularities": irregularities
            },
            "compliance": compliance_res,
            "external_intel": tavily_res,
            "executive_report": llm_res["content"],
            "model_metadata": {
                "model": llm_res["model"],
                "latency_seconds": llm_res["latency_seconds"],
                "tokens": llm_res["completion_tokens"],
                "cloud": "Nebius Token Factory"
            }
        }
