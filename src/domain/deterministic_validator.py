from schemas.contracts import StudyPayload
from typing import Dict, Any, List

class DeterministicValidator:
    """
    Responsável por checagens estruturais e puramente formais nos dados.
    Não utiliza IA.
    """
    
    def validate_study_structure(self, payload: StudyPayload) -> Dict[str, Any]:
        errors = []
        warnings = []
        
        # Exemplo expandido de validação estrutural do MVP
        if not payload.study_metadata.title:
            errors.append("Title is missing in study_metadata.")
        
        if not payload.study_metadata.study_type:
            errors.append("Study type is missing in study_metadata.")

        if not payload.study_metadata.species:
            errors.append("Species is missing in study_metadata.")

        if not payload.experimental_groups:
            errors.append("No experimental groups provided.")

        if not payload.datasets:
            errors.append("No datasets provided.")
        else:
            for i, dataset in enumerate(payload.datasets):
                if not dataset.records:
                    errors.append(f"Dataset '{dataset.name}' (index {i}) has no records.")
                if not dataset.schema_definition:
                    errors.append(f"Dataset '{dataset.name}' (index {i}) has no schema definition.")
            
        quality_score = 100 if not errors else max(0, 100 - (len(errors)*15))
        requires_human_review = len(errors) > 0

        return {
            "quality_score": quality_score,
            "errors": errors,
            "warnings": warnings,
            "requires_human_review": requires_human_review,
            "status": "invalid" if errors else "valid"
        }
