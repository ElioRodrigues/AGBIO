"""
Study Classifier Agent
Responsável por classificar o estudo recebido e determinar o contexto analítico.
Integrado com a infraestrutura LLM, suportando fallback seguro para modo stub.
"""
import json
import logging
from pydantic import ValidationError

from schemas.contracts import StudyPayload, StudyClassifierOutput, StudyClassification, CompletenessAssessment
from core.prompt_loader import PromptLoader
from llm.client import LLMClient

class StudyClassifier:
    def __init__(self):
        self.llm_client = LLMClient()
        try:
            self.prompt = PromptLoader.load_prompt("study_classifier")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do study_classifier não encontrado.")

    def _get_stub_fallback(self, payload: StudyPayload, limitations: str) -> StudyClassifierOutput:
        """Retorna uma saída de stub controlada e previsível."""
        return StudyClassifierOutput(
            study_classification=StudyClassification(
                study_type=payload.study_metadata.study_type,
                domains_detected=[d.domain for d in payload.datasets] if payload.datasets else [],
                template_recommendation="standard_tox"
            ),
            completeness_assessment=CompletenessAssessment(
                status="complete" if payload.datasets else "insufficient_data",
                missing_critical_fields=[]
            ),
            confidence="unknown",
            limitations=[limitations],
            requires_human_review=True
        )

    async def execute(self, payload: StudyPayload) -> StudyClassifierOutput:
        # 1. Montar a entrada textual combinada
        prompt_input = (
            f"Analise os seguintes dados do estudo:\n"
            f"Metadados: {payload.study_metadata.model_dump_json()}\n"
            f"Resumo do Protocolo: {payload.protocol_summary}\n"
            f"Grupos Experimentais: {[g.group_name for g in payload.experimental_groups]}\n"
            f"Datasets Disponíveis: {[d.domain for d in payload.datasets]}\n"
            f"Configurações: {payload.analysis_config.model_dump_json()}\n"
        )
        
        try:
            # 2. Invocar o cliente LLM
            raw_response = await self.llm_client.generate_text(
                prompt=prompt_input, 
                system_instruction=self.prompt
            )

            # 3. Limpeza de markdown caso o LLM adicione bloco ```json
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            # 4. Decodificação segura
            response_dict = json.loads(cleaned_response.strip())
            
            # Se a resposta vier expressamente do mock do LLMClient
            if response_dict.get("status") == "stub_mode_active":
                return self._get_stub_fallback(
                    payload, 
                    "Classificação estática ativada mecanicamente por segurança (motor LLM desativado no ambiente)."
                )
            
            # 5. Validação com o contrato
            return StudyClassifierOutput(**response_dict)

        except (json.JSONDecodeError, ValidationError) as e:
            logging.error(f"Erro ao parsear saída da IA no StudyClassifier: {str(e)}")
            return self._get_stub_fallback(
                payload, 
                "Falha ao interpretar estruturalmente a resposta da IA. Aplicando fallback conservador."
            )
        except Exception as e:
            logging.error(f"Falha sistêmica no processamento do StudyClassifier: {str(e)}")
            return self._get_stub_fallback(
                payload, 
                "Indisponibilidade ou erro isolado no motor de IA. Status reduzido a stub temporário."
            )
