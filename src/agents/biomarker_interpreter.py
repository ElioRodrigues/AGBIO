"""
Biomarker Interpreter Agent
Analisa relatórios quantitativos (como de padrões) com semântica biológica cautelosa.
Integrado com a infraestrutura LLM, suportando fallback seguro para modo stub.
"""
import json
import logging
from pydantic import ValidationError

from schemas.contracts import StudyPayload, BiomarkerInterpreterOutput
from core.prompt_loader import PromptLoader
from llm.client import LLMClient

def _safe_dump(obj):
    if hasattr(obj, "model_dump_json"):
        return obj.model_dump_json(indent=2)
    elif hasattr(obj, "dict"):
        return json.dumps(obj.dict(), indent=2, ensure_ascii=False)
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    except Exception:
        return str(obj)

from core.config import config

class BiomarkerInterpreter:
    def __init__(self):
        self.llm_client = LLMClient(config.USE_GEMINI_BIOMARKER_INTERPRETER)
        try:
            self.prompt = PromptLoader.load_prompt("biomarker_interpreter")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do biomarker_interpreter não encontrado.")

    def _get_stub_fallback(self, limitations: str) -> BiomarkerInterpreterOutput:
        """Retorna uma saída simulada em caso de falha de conexão ou parser."""
        return BiomarkerInterpreterOutput(
            domain_interpretations={"GERAL": "Interpretação cruzada impossibilitada devido ao modo stub fixo da arquitetura."},
            cross_domain_summary="Nenhuma síntese ou correlação avaliada entre os achados na premissa atual.",
            points_requiring_confirmation=["A validação humana é obrigatoria diante de stubs vazios de interpretação."],
            confidence="unknown",
            limitations=["Motor IA em pausa. Fallback mecânico não produz inferência cognitiva.", limitations],
            requires_human_review=True
        )

    def _normalize_response(self, data: dict) -> dict:
        """Aplica normalização defensiva antes da validação Pydantic."""
        conf = data.get("confidence")
        if isinstance(conf, (int, float)):
            if conf >= 0.75: data["confidence"] = "high"
            elif conf >= 0.4: data["confidence"] = "medium"
            elif conf > 0: data["confidence"] = "low"
            else: data["confidence"] = "unknown"
            
        return data

    async def execute(self, payload: StudyPayload, pipeline_results: dict) -> BiomarkerInterpreterOutput:
        
        classification_data = _safe_dump(pipeline_results.get("classification", {}))
        ai_val_data = _safe_dump(pipeline_results.get("ai_validation", {}))
        patterns_data = _safe_dump(pipeline_results.get("patterns", {}))
        
        # Subamostragem de datasets focando só na raiz da estrutura, já que o validador lida com o pesado numérico
        datasets_preview = []
        for d in payload.datasets:
            datasets_preview.append({
                "domain": d.domain,
                "schema": d.schema_definition
            })

        prompt_input = (
            f"Analise e interprete os indícios para o seguinte estudo de segurança:\n\n"
            f"=== METADADOS E PROTOCOLO ===\n"
            f"{payload.study_metadata.model_dump_json(indent=2)}\n"
            f"Resumo: {payload.protocol_summary}\n\n"
            f"=== ANÁLISES PRELIMINARES DO PIPELINE ===\n"
            f"CLASSIFICAÇÃO: {classification_data}\n\n"
            f"AVALIAÇÃO DE CONTROLE DE QUALIDADE: {ai_val_data}\n\n"
            f"PADRÕES E OUTLIERS ENCONTRADOS ESTATISTICAMENTE: {patterns_data}\n\n"
            f"=== ESTRUTURA DOS DATASETS EXISTENTES ===\n"
            f"{json.dumps(datasets_preview, ensure_ascii=False, indent=2)}\n\n"
            f"LIMITAÇÃO DE ESCOPO OBRIGATÓRIA: Evite verbos absolutos de sentença médica. A resposta DEVE seguir os modais 'pode sugerir', 'requer confirmação adicional'. Você depende 100% dos relatórios expostos acima pelas suas IAs colegas."
        )

        try:
            raw_response = await self.llm_client.generate_text(
                prompt=prompt_input, 
                system_instruction=self.prompt
            )

            cleaned_response = raw_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            response_dict = json.loads(cleaned_response.strip())
            
            if response_dict.get("status") == "stub_mode_active":
                return self._get_stub_fallback("Interpretador bio-semântico desativado no momento.")
            
            response_dict = self._normalize_response(response_dict)
            return BiomarkerInterpreterOutput(**response_dict)

        except (json.JSONDecodeError, ValidationError) as e:
            logging.error(f"Erro no parse/estruturação LLM do BiomarkerInterpreter: {str(e)}")
            return self._get_stub_fallback(
                f"Alucinação/Quebra de schema no módulo interpretativo: {str(e)[:50]}."
            )
        except Exception as e:
            logging.error(f"Falha sistêmica no LLM dentro de BiomarkerInterpreter: {str(e)}")
            return self._get_stub_fallback(
                "Falha na API externa LLM ao traduzir anomalias bio-químicas."
            )
