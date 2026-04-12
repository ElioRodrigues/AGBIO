import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Toxicology Meta-Agent API"
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    PROMPTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "prompts")
    
    # LLM Parâmetros de Integração
    LLM_PROVIDER: str = "stub"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Feature Flags por Agente
    USE_GEMINI_STUDY_CLASSIFIER: bool = False
    USE_GEMINI_DATA_VALIDATOR: bool = False
    USE_GEMINI_PATTERN_DETECTOR: bool = False
    USE_GEMINI_BIOMARKER_INTERPRETER: bool = False
    USE_GEMINI_REPORT_GENERATOR: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

config = Settings()
