"""
Audit Agent (MVP Stub)
Responsável pelo rastreamento centralizado da saúde do pipeline e por acionar gatilhos de controle humano.
Nesta versão (MVP), coleta a rota de agentes chamados e acusa limitação explícita por design.
"""
import logging
from core.prompt_loader import PromptLoader
from schemas.contracts import AuditAgentOutput

class AuditAgent:
    def __init__(self):
        try:
            self.prompt = PromptLoader.load_prompt("audit_agent")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do audit_agent não encontrado.")

    async def execute(self, pipeline_results: dict) -> AuditAgentOutput:
        return AuditAgentOutput(
            traceability=list(pipeline_results.keys()),
            review_points=["Atenção: como o motor está com os agentes operando em modo stub (sem IA real), uma revisão humana e análise interpretativa manual de todos os resultados são absolutamente necessárias."],
            conflicts=[],
            final_confidence="low",
            limitations=["Este registro de auditoria apenas corrobora que a arquitetura do motor transitou os dados."],
            requires_human_review=True
        )
