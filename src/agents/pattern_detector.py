"""
Pattern Detector Agent (MVP Stub)
Responsável por identificar tendências e outliers nos datasets alimentados.
Nesta versão (MVP), não impõe achados analíticos, garantindo segurança ao retornar estado neutro.
"""
import logging
from schemas.contracts import StudyPayload, PatternDetectorOutput
from core.prompt_loader import PromptLoader

class PatternDetector:
    def __init__(self):
        try:
            self.prompt = PromptLoader.load_prompt("pattern_detector")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do pattern_detector não encontrado.")

    async def execute(self, payload: StudyPayload) -> PatternDetectorOutput:
        return PatternDetectorOutput(
            outliers=[],
            patterns=["Nenhum padrão biológico calculado (agente base provisório)."],
            group_comparisons="Computação de divergência intergrupos está pendente de implementação LLM.",
            biological_relevance_estimated="low",
            confidence="unknown",
            limitations=["Sem suporte estatístico ou IA conectado neste momento."],
            requires_human_review=True
        )
