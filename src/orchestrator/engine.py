from schemas.contracts import StudyPayload
from domain.deterministic_validator import DeterministicValidator
from agents.study_classifier import StudyClassifier
from agents.data_validator import DataValidator
from agents.pattern_detector import PatternDetector
from agents.biomarker_interpreter import BiomarkerInterpreter
from agents.report_generator import ReportGenerator
from agents.audit_agent import AuditAgent

class OrchestratorEngine:
    """
    Orchestra o pipeline do sistema de acordo com:
    1. Deterministic validation
    2. Study classification
    3. Data Validation (AI)
    4. Pattern Detection
    5. Biomarker Interpretation
    6. Report Generator
    7. Audit Agent
    """
    
    def __init__(self):
        self.deterministic_validator = DeterministicValidator()
        self.classifier = StudyClassifier()
        self.ai_validator = DataValidator()
        self.pattern_detector = PatternDetector()
        self.interpreter = BiomarkerInterpreter()
        self.reporter = ReportGenerator()
        self.auditor = AuditAgent()

    async def run_pipeline(self, payload: StudyPayload) -> dict:
        results = {}
        
        # 1. Deterministic Checks
        det_validation = self.deterministic_validator.validate_study_structure(payload)
        results["deterministic_validation"] = det_validation
        
        # If critical errors stop pipeline
        if det_validation.get("status") == "invalid":
            results["pipeline_status"] = "aborted_due_to_structural_errors"
            results["audit"] = await self.auditor.execute(results)
            return results
        
        # 2. Agent Workflow
        results["classification"] = await self.classifier.execute(payload)
        results["ai_validation"] = await self.ai_validator.execute(payload, det_validation)
        results["patterns"] = await self.pattern_detector.execute(payload)
        results["interpretation"] = await self.interpreter.execute(payload, results["patterns"])
        results["report"] = await self.reporter.execute(payload, results)
        results["audit"] = await self.auditor.execute(results)
        
        return results
