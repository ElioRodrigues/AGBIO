"""
Biomarker Interpreter Agent (MVP Stub)
Responsável por interpretação preliminar de achados, operando com linguagem cautelosa.
Nesta versão (MVP), abstém-se deliberadamente de induzir significados que não possam ser sustentados pela lógica atual.
"""
import logging
from schemas.contracts import StudyPayload, BiomarkerInterpreterOutput, PatternDetectorOutput
from core.prompt_loader import PromptLoader

class BiomarkerInterpreter:
    def __init__(self):
        try:
            self.prompt = PromptLoader.load_prompt("biomarker_interpreter")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do biomarker_interpreter não encontrado.")

    async def execute(self, payload: StudyPayload, pattern_results: PatternDetectorOutput) -> BiomarkerInterpreterOutput:
        return BiomarkerInterpreterOutput(
            domain_interpretations={
                "general": "Nenhuma interpretação explícita formulada nesta fase da pipeline em MVP."
            },
            cross_domain_summary="Faltam bases quantitativas concretas trans-domínio no MVP.",
            points_requiring_confirmation=["A totalidade da análise exige revisão laboratorial/clínica prévia."],
            confidence="low",
            limitations=["Interpretador cognitivo desligado por precaução técnica em MVP."],
            requires_human_review=True
        )
