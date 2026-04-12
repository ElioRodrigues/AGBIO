"""
Data Validator Agent
Complementa a validação determinística com validações semânticas baseadas em IA.
Integrado com a infraestrutura LLM, suportando fallback seguro para modo stub.
A validação estrutural determinística continua sendo a base absoluta.
"""
import json
import logging
from pydantic import ValidationError

from schemas.contracts import StudyPayload, DataValidatorOutput
from core.prompt_loader import PromptLoader
from llm.client import LLMClient

from core.config import config

class DataValidator:
    def __init__(self):
        self.llm_client = LLMClient(config.USE_GEMINI_DATA_VALIDATOR)
        try:
            self.prompt = PromptLoader.load_prompt("data_validator")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do data_validator não encontrado.")

    def _get_stub_fallback(self, deterministic_results: dict, extra_limitations: str) -> DataValidatorOutput:
        """Retorna uma saída controlada mantendo os resultados determinísticos."""
        return DataValidatorOutput(
            quality_score=deterministic_results.get("quality_score", 100),
            errors=deterministic_results.get("errors", []),
            warnings=deterministic_results.get("warnings", []) + ["Validação semântica de IA em stand-by/falha."],
            summary="Avaliação embasada exclusivamente no validador estrutural determinístico.",
            confidence="medium",
            limitations=["As checagens semânticas via LLM não foram ativadas.", extra_limitations],
            requires_human_review=deterministic_results.get("requires_human_review", False)
        )

    async def execute(self, payload: StudyPayload, deterministic_results: dict) -> DataValidatorOutput:
        # 1. Montar a entrada textual simplificada combinando payload e checagem determinística
        prompt_input = (
            f"Analise semanticamente os seguintes dados do estudo:\n\n"
            f"=== VALIDAÇÃO ESTRUTURAL (Base Imutável) ===\n"
            f"{json.dumps(deterministic_results, ensure_ascii=False, indent=2)}\n\n"
            f"=== DADOS DO ESTUDO ===\n"
            f"Metadados: {payload.study_metadata.model_dump_json()}\n"
            f"Resumo do Protocolo: {payload.protocol_summary}\n"
            f"Grupos Experimentais: {[g.group_name for g in payload.experimental_groups]}\n"
            f"Tipos de Datasets Disponíveis: {[d.domain for d in payload.datasets]}\n\n"
            f"ATENÇÃO DA ARQUITETURA: Você NÃO está recebendo nesta etapa as linhas de registros em blocos brutos, mas "
            f"apenas os metadados lógicos do pipeline listados acima. Portanto, NÃO extrapole nem emita laudos afirmativos "
            f"sobre averiguações em campo (como nulos, tipagem e duplicidades profundas) e repouse esse peso sobre o Validator Determinístico original e na chave 'limitations'."
        )
        
        try:
            # 2. Invocar o cliente LLM
            raw_response = await self.llm_client.generate_text(
                prompt=prompt_input, 
                system_instruction=self.prompt
            )

            # 3. Limpeza defensiva
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            # 4. Decodificação segura
            response_dict = json.loads(cleaned_response.strip())
            
            # Checagem de modo Stub
            if response_dict.get("status") == "stub_mode_active":
                return self._get_stub_fallback(
                    deterministic_results, 
                    "Validador semântico em pausa local."
                )
            
            # 5. Mesclagem Estrutural vs Semântica (Regra Ouro)
            # A IA não tem permissão para descartar os erros matemáticos achados antes
            final_errors = list(set(deterministic_results.get("errors", []) + response_dict.get("errors", [])))
            final_warnings = list(set(deterministic_results.get("warnings", []) + response_dict.get("warnings", [])))
            
            response_dict["errors"] = final_errors
            response_dict["warnings"] = final_warnings
            
            # O quality score não mascara furos estruturais (escolha pela via mais segura)
            ai_score = response_dict.get("quality_score", 100)
            det_score = deterministic_results.get("quality_score", 100)
            response_dict["quality_score"] = min(ai_score, det_score)
            
            # Nível de revisão
            response_dict["requires_human_review"] = (
                deterministic_results.get("requires_human_review", False) or 
                response_dict.get("requires_human_review", False)
            )
            
            # 6. Validação do contrato Pydantic
            return DataValidatorOutput(**response_dict)

        except (json.JSONDecodeError, ValidationError) as e:
            logging.error(f"Erro no parse/validação LLM do DataValidator: {str(e)}")
            return self._get_stub_fallback(
                deterministic_results, 
                "Alucinação ou corrupção na resposta semântica. Operando apenas com base estrutural."
            )
        except Exception as e:
            logging.error(f"Falha sistêmica no LLM dentro de DataValidator: {str(e)}")
            return self._get_stub_fallback(
                deterministic_results, 
                "Instabilidade de provedor. Operando apenas com base estrutural."
            )
