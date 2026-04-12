from fastapi import APIRouter
from schemas.contracts import StudyPayload
from orchestrator.engine import OrchestratorEngine

router = APIRouter(prefix="/study", tags=["Study Analysis"])
engine = OrchestratorEngine()

@router.post("/analyze")
async def analyze_study(payload: StudyPayload) -> dict:
    """
    Receives a study payload and orchestrates the multi-agent analysis pipeline.
    """
    result = await engine.run_pipeline(payload)
    return {"status": "success", "data": result}
