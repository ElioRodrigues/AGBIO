import logging
from core.config import config

class LLMClient:
    """
    Cliente centralizado para interações com LLMs no pipeline.
    Gerencia o fallback entre conectores reais e o modo stub (seguro/MVP).
    """
    def __init__(self, agent_flag: bool = False):
        if config.LLM_PROVIDER == "gemini" and agent_flag:
            self.provider = "gemini"
        else:
            self.provider = "stub"
        
        if self.provider == "gemini":
            from google import genai
            if not config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY deve estar preenchida quando LLM_PROVIDER='gemini'")
            
            # Inicializando a versão nova e recomendada do SDK da Google
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            self.model_name = config.GEMINI_MODEL
        else:
            self.client = None
            logging.info("LLMClient operando em modo 'stub' (protegido).")

    async def generate_text(self, prompt: str, system_instruction: str = "") -> str:
        """
        Executa requisições de prompt em direção ao modelo correspondente ou stub.
        """
        if self.provider == "stub":
            return '{"status": "stub_mode_active", "message": "Execução protegida no MVP. Nenhum LLM real foi invocado."}'
            
        elif self.provider == "gemini":
            from google.genai import types
            
            # Construindo parâmetros de configuração de maneira maleável
            config_params = {}
            if system_instruction:
                config_params["system_instruction"] = system_instruction
                
            gen_config = types.GenerateContentConfig(**config_params)
            
            # Acionando o serviço subjacente assincronamente 
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=gen_config
            )
            return response.text
            
        else:
            raise ValueError(f"Provedor LLM não suportado localmente: '{self.provider}'")
