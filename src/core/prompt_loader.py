import os
from core.config import config

class PromptLoader:
    """
    Responsible for loading system prompts from the prompts/ directory.
    """
    @classmethod
    def load_prompt(cls, agent_name: str, file_name: str = "system.txt") -> str:
        prompt_path = os.path.join(config.PROMPTS_DIR, agent_name, file_name)
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
