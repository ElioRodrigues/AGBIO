"""
Pattern Detector Agent
Identifica tendências, discrepâncias estatísticas e agrupamentos nos datasets validados.
Integrado com a infraestrutura LLM, suportando fallback seguro para modo stub.
"""
import json
import logging
from pydantic import ValidationError

from schemas.contracts import StudyPayload, PatternDetectorOutput
from core.prompt_loader import PromptLoader
from llm.client import LLMClient

from core.config import config

class PatternDetector:
    def __init__(self):
        self.llm_client = LLMClient(config.USE_GEMINI_PATTERN_DETECTOR)
        try:
            self.prompt = PromptLoader.load_prompt("pattern_detector")
        except FileNotFoundError:
            self.prompt = ""
            logging.warning("Prompt do pattern_detector não encontrado.")

    def _get_stub_fallback(self, limitations: str) -> PatternDetectorOutput:
        """Retorna uma saída controlada com o fallback simulado."""
        return PatternDetectorOutput(
            outliers=[],
            patterns=["Nenhum padrão biológico calculado (agente preservado em modo stub ativo)."],
            group_comparisons="Computação de divergência intergrupos pendente (motor IA offline/falho).",
            biological_relevance_estimated="unknown",
            confidence="low",
            limitations=["Sem suporte iterativo da IA ativado estatisticamente.", limitations],
            requires_human_review=True
        )

    def _normalize_response(self, data: dict) -> dict:
        """Aplica normalização defensiva antes da validação Pydantic."""
        # 1. Normalizar confidence para Literal ("high", "medium", "low", "unknown")
        conf = data.get("confidence")
        if isinstance(conf, (int, float)):
            if conf >= 0.75: data["confidence"] = "high"
            elif conf >= 0.4: data["confidence"] = "medium"
            elif conf > 0: data["confidence"] = "low"
            else: data["confidence"] = "unknown"
            
        biological = data.get("biological_relevance_estimated")
        if not biological or biological not in ["high", "medium", "low", "unknown"]:
            data["biological_relevance_estimated"] = "unknown"
            
        group_comp = data.get("group_comparisons")
        if not group_comp or not isinstance(group_comp, str) or group_comp.strip() == "":
            data["group_comparisons"] = "O levantamento cruzado não revelou ou não possuiu volume suficiente para sustentar divergências analíticas notórias entre grupos."
            
        # 2. Converter patterns se vier incorretamente como lista de objetos do prompt antigo
        patterns = data.get("patterns")
        if isinstance(patterns, list):
            norm_pat = []
            for item in patterns:
                if isinstance(item, dict):
                    # Tentar montar uma string extraindo os valores
                    desc = item.get("description", str(item))
                    norm_pat.append(desc)
                elif isinstance(item, str):
                    norm_pat.append(item)
                else:
                    norm_pat.append(str(item))
            data["patterns"] = norm_pat

        return data

    async def execute(self, payload: StudyPayload) -> PatternDetectorOutput:
        # 1. Montar entrada defensiva cortando excesso absoluto de registros 
        # (Para o MVP com LLM, extrairemos até 50 amostras brutas para ele não exaurir o limite de tokens)
        datasets_preview = []
        for d in payload.datasets:
            records = d.records[:50]
            datasets_preview.append({
                "domain": d.domain,
                "name": d.name,
                "schema": d.schema_definition,
                "records_sample": records,
                "total_records": len(d.records)
            })

        prompt_input = (
            f"Processe e detete padrões e outliers para o seguinte estudo:\n\n"
            f"=== METADADOS DO ESTUDO ===\n"
            f"{payload.study_metadata.model_dump_json(indent=2)}\n\n"
            f"Resumo do Protocolo: {payload.protocol_summary}\n\n"
            f"=== GRUPOS EXPERIMENTAIS ===\n"
            f"{[g.model_dump() for g in payload.experimental_groups]}\n\n"
            f"=== AMOSTRA DE DATASETS (MÁX 50 LINHAS) ===\n"
            f"{json.dumps(datasets_preview, indent=2, ensure_ascii=False)}\n\n"
            f"Lembre-se: ATENÇÃO! Você deve focar puramente nas estatísticas e diferenças quantitativas. "
            f"NÃO afirme causalidades, NÃO realize laudos definitivos de toxicidade médica, puramente aponte "
            f"eventuais comportamentos diferentes entre os grupos de variáveis exibidas."
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
            
            if response_dict.get("status") == "stub_mode_active":
                return self._get_stub_fallback("Detector quantitativo IA pausado localmente via ENV.")
            
            # 5. Normalização defensiva ativa
            response_dict = self._normalize_response(response_dict)
            
            # 6. Validação nativa com o Pydantic
            return PatternDetectorOutput(**response_dict)

        except (json.JSONDecodeError, ValidationError) as e:
            logging.error(f"Erro no parse/validação LLM do PatternDetector: {str(e)}")
            return self._get_stub_fallback(
                f"Alucinação/Quebra de estrutura estatística pela IA: {str(e)[:50]}."
            )
        except Exception as e:
            logging.error(f"Falha sistêmica no LLM dentro de PatternDetector: {str(e)}")
            return self._get_stub_fallback(
                "Falha na API externa impeditiva da computação dos subgrupos estatísticos."
            )
