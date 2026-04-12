from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

class StudyMetadata(BaseModel):
    title: str
    study_type: str
    species: str
    duration_days: int
    objective: str
    regulatory_target: List[str]

class ExperimentalGroup(BaseModel):
    group_id: str
    group_name: str
    description: str

class Dataset(BaseModel):
    dataset_id: str
    name: str
    domain: str
    type: str = "tabular"
    schema_definition: Dict[str, str] = Field(default_factory=dict, alias="schema")
    records: List[Dict[str, Any]]

class AnalysisConfig(BaseModel):
    language: str = "pt-BR"
    strict_validation: bool = True
    enable_pattern_detection: bool = True
    enable_interpretation: bool = True

class StudyPayload(BaseModel):
    study_id: str
    study_metadata: StudyMetadata
    protocol_summary: str
    experimental_groups: List[ExperimentalGroup]
    datasets: List[Dataset]
    analysis_config: AnalysisConfig = Field(default_factory=AnalysisConfig)

# Agent Output Base Requirements
class AgentResponseBase(BaseModel):
    confidence: Literal["high", "medium", "low", "unknown"] = "unknown"
    limitations: List[str] = Field(default_factory=list)
    requires_human_review: bool = False

# --- Agent Outputs ---

class StudyClassification(BaseModel):
    study_type: str
    domains_detected: List[str] = Field(default_factory=list)
    template_recommendation: str

class CompletenessAssessment(BaseModel):
    status: str
    missing_critical_fields: List[str] = Field(default_factory=list)

class StudyClassifierOutput(AgentResponseBase):
    study_classification: StudyClassification
    completeness_assessment: CompletenessAssessment

class DataValidatorOutput(AgentResponseBase):
    quality_score: float
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    summary: str

class PatternDetectorOutput(AgentResponseBase):
    outliers: List[Dict[str, Any]] = Field(default_factory=list)
    patterns: List[str] = Field(default_factory=list)
    group_comparisons: str
    biological_relevance_estimated: Literal["high", "medium", "low", "unknown"] = "unknown"

class BiomarkerInterpreterOutput(AgentResponseBase):
    domain_interpretations: Dict[str, str] = Field(default_factory=dict)
    cross_domain_summary: str
    points_requiring_confirmation: List[str] = Field(default_factory=list)

class ReportSections(BaseModel):
    study_summary: str
    data_quality_assessment: str
    results_overview: str
    technical_interpretation: str
    limitations: str
    preliminary_conclusion: str
    recommended_human_review_points: List[str] = Field(default_factory=list)

class ReportGeneratorOutput(AgentResponseBase):
    report_title: str
    sections: ReportSections
    appendices: List[str] = Field(default_factory=list)

class AuditAgentOutput(AgentResponseBase):
    traceability: List[str] = Field(default_factory=list)
    review_points: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    final_confidence: Literal["high", "medium", "low", "unknown"] = "unknown"
