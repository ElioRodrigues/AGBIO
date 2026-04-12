"""
Report Generator Agent
Consolida os achados do pipeline em um formato narrativo padronizado usando LLM.
Integrado com a infraestrutura LLM, suportando fallback seguro para modo stub.
"""
import json
import logging
from pydantic import ValidationError

from schemas.contracts import StudyPayload, ReportGeneratorOutput, ReportSections
from core.prompt_loader import PromptLoader
from llm.client import LLMClient

def _safe_dump(obj):
    if hasattr(obj, "model_dump_json"):
        return obj.model_dump_json(indent=2)
    elif hasattr(obj, "dict"):
        return json.dumps(obj.dict(), indent=2, ensure_ascii=False)
    # Em um fallback final para tipos comuns, convertemos de forma simples
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    except Exception:
        return str(obj)

class ReportGenerator:
    def __init__(self):
        self.llm_client = LLMClient()
        try:
            self.prompt = PromptLoader.load_prompt("report_generator")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do report_generator não encontrado.")

    def _get_stub_fallback(self, payload: StudyPayload, limitations: str) -> ReportGeneratorOutput:
        """Retorna uma saída controlada com o fallback de gerador estático."""
        return ReportGeneratorOutput(
            report_title=f"Relatório Preliminar: {payload.study_metadata.title}",
            sections=ReportSections(
                study_summary=payload.protocol_summary,
                data_quality_assessment="Validação baseada em checagens limitadas a stub.",
                results_overview="Nenhuma observação detectada (agentes mantidos em stub).",
                technical_interpretation="Ausência de argumentação na ausência do motor de IA.",
                limitations="Limitação global do relatório por ausência de IA ativada de ponta a ponta.",
                preliminary_conclusion="Conclusões retidas para inferência especializada ou análise humana.",
                recommended_human_review_points=["Avaliação integral do documento recomendada."]
            ),
            appendices=["Erro/Aviso de Pipeline: rodou usando a arquitetura estrutural passiva/fallback."],
            confidence="low",
            limitations=["Sem LLM ativado real, não há síntese narrativa.", limitations],
            requires_human_review=True
        )

    def _normalize_response(self, data: dict) -> dict:
        """Aplica normalização defensiva antes da validação Pydantic."""
        # 1. Normalizar confidence para Literal (high, medium, low, unknown)
        conf = data.get("confidence")
        if isinstance(conf, (int, float)):
            if conf >= 0.75:
                data["confidence"] = "high"
            elif conf >= 0.4:
                data["confidence"] = "medium"
            elif conf > 0:
                data["confidence"] = "low"
            else:
                data["confidence"] = "unknown"
                
        # 2. Normalizar recommended_human_review_points de volta para Lista
        sections = data.get("sections", {})
        if isinstance(sections, dict):
            review_pts = sections.get("recommended_human_review_points")
            if isinstance(review_pts, str):
                sections["recommended_human_review_points"] = [review_pts]
                
        # 3. Normalizar appendices quando vem como dict para List[str]
        app = data.get("appendices")
        if isinstance(app, dict):
            normalized_app = []
            for k, v in app.items():
                if isinstance(v, list):
                    for item in v:
                        normalized_app.append(f"{str(k).capitalize()}: {item}")
                elif isinstance(v, str):
                    normalized_app.append(f"{str(k).capitalize()}: {v}")
                else:
                    normalized_app.append(f"{str(k).capitalize()}: {str(v)}")
            data["appendices"] = normalized_app
            
        return data

    async def execute(self, payload: StudyPayload, pipeline_results: dict) -> ReportGeneratorOutput:
        # Recuperar estruturas dos agentes anteriores dinamicamente
        classification_data = _safe_dump(pipeline_results.get("classification", {}))
        ai_val_data = _safe_dump(pipeline_results.get("ai_validation", {}))
        patterns_data = _safe_dump(pipeline_results.get("patterns", {}))
        interpre_data = _safe_dump(pipeline_results.get("interpretation", {}))

        prompt_input = (
            f"Consolide o Relatório Final para o seguinte estudo toxicológico:\n\n"
            f"=== 1. INTRODUÇÃO E METADADOS ===\n"
            f"Metadados do Estudo: {payload.study_metadata.model_dump_json(indent=2)}\n"
            f"Resumo do Protocolo: {payload.protocol_summary}\n\n"
            f"=== 2. RESULTADOS DO MÓDULO CLASSIFICADOR ===\n"
            f"{classification_data}\n\n"
            f"=== 3. RESULTADOS DO MÓDULO VALIDADOR ===\n"
            f"{ai_val_data}\n\n"
            f"=== 4. RESULTADOS DO DETECTOR DE PADRÕES ===\n"
            f"{patterns_data}\n\n"
            f"=== 5. RESULTADOS DO INTERPRETADOR ===\n"
            f"{interpre_data}\n\n"
            f"Por favor, produza o relatório. Não assuma conclusões toxicológicas profundas se os dados "
            f"agrupados acima refletirem falhas, inconsistências, ou não as fornecerem plenamente. Limite-se ao fato contido nas entradas."
        )

        try:
            # Invocar o cliente LLM
            raw_response = await self.llm_client.generate_text(
                prompt=prompt_input, 
                system_instruction=self.prompt
            )

            # Limpeza defensiva
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]
            
            # Decodificação segura
            response_dict = json.loads(cleaned_response.strip())
            
            if response_dict.get("status") == "stub_mode_active":
                return self._get_stub_fallback(
                    payload, 
                    "Sintetizador narrativo LLM em pausa no arquivo local de config. Operando modo stub."
                )
            
            # Normalização defensiva ativa
            response_dict = self._normalize_response(response_dict)
            
            # Validação nativa com o contrato
            return ReportGeneratorOutput(**response_dict)

        except (json.JSONDecodeError, ValidationError) as e:
            logging.error(f"Erro no parse/validação LLM do ReportGenerator: {str(e)}")
            return self._get_stub_fallback(
                payload, 
                "Alucinação ou falha de tipagem na síntese de relatórios (ValidationError / DecodeError)."
            )
        except Exception as e:
            logging.error(f"Falha sistêmica no LLM dentro de ReportGenerator: {str(e)}")
            return self._get_stub_fallback(
                payload, 
                "Gargalo de conexão/Timeout no LLM ao tentar consolidar grandes volumes de dados."
            )
