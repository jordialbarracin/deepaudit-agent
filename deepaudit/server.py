"""
DeepAudit FastAPI Server: Web dashboard backend for autonomous corporate forensic audits.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from deepaudit.test_cases import list_cases, get_case, AUDIT_TEST_CASES
from deepaudit.auditor_agent import DeepAuditAgent

app = FastAPI(title="DeepAudit API", description="Autonomous Corporate Forensics & Due Diligence powered by NVIDIA Nemotron & Tavily")

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)

class AuditRequest(BaseModel):
    case_id: Optional[str] = "iberia_logistics"
    custom_company: Optional[Dict[str, Any]] = None

@app.get("/api/cases")
def get_cases():
    return {"cases": list_cases()}

@app.get("/api/case/{case_id}")
def get_case_detail(case_id: str):
    if case_id not in AUDIT_TEST_CASES:
        raise HTTPException(status_code=404, detail="Case not found")
    return AUDIT_TEST_CASES[case_id]

@app.get("/api/compliance/{case_id}")
def get_case_compliance(case_id: str):
    if case_id not in AUDIT_TEST_CASES:
        raise HTTPException(status_code=404, detail="Case not found")
    from deepaudit.compliance_engine import ComplianceEngine
    return ComplianceEngine.audit_certifications(AUDIT_TEST_CASES[case_id])

@app.post("/api/audit")
def execute_audit(req: AuditRequest):
    agent = DeepAuditAgent()
    target = req.custom_company if req.custom_company else req.case_id
    result = agent.run_audit(target)
    return result

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "engine": "DeepAudit v1.0",
        "llm_model": "nvidia/Nemotron-3_5-Lightning",
        "search_engine": "Tavily AI Search",
        "cloud_provider": "Nebius Token Factory"
    }

@app.get("/", response_class=HTMLResponse)
def index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>DeepAudit Forensic Dashboard Ready</h1>")

# Mount static directory
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
