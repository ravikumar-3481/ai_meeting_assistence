import os
from typing import Optional
from api.config import Config
from utils.logger import Logger

_llm = None


class LLM:
    def __init__(self):
        self.logger = Logger()
        self.log = self.logger.get_logger()
        try:
            cfg = Config()
            self.mistral_api_key = cfg.mistral_api_key.get_secret_value() if cfg.mistral_api_key else None
            self.huggingface_api_token = cfg.huggingface_api_token.get_secret_value() if cfg.huggingface_api_token else None
        except Exception as e:
            self.log.warning(f"Config load notice in LLM: {e}")
            self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
            self.huggingface_api_token = os.getenv("HUGGINGFACE_API_TOKEN")

    def get_llm(self, temperature: float = 0.3):
        global _llm
        if _llm is not None:
            return _llm

        preferred_provider = os.getenv("LLM_PROVIDER", "auto").lower()

        # If Hugging Face is explicitly requested or Mistral key is not set
        if (preferred_provider == "huggingface" or not self.mistral_api_key) and self.huggingface_api_token:
            _llm = self._get_huggingface_llm(temperature)
            if _llm is not None:
                return _llm

        # Try Mistral AI
        if self.mistral_api_key:
            try:
                from langchain_mistralai import ChatMistralAI
                self.log.info("Initializing ChatMistralAI (model: mistral-small-latest)...")
                _llm = ChatMistralAI(
                    model="mistral-small-latest",
                    mistral_api_key=self.mistral_api_key,
                    temperature=temperature,
                )
                return _llm
            except Exception as e:
                self.log.warning(f"Mistral AI initialization failed: {e}. Attempting Hugging Face interface fallback...")

        # Fallback to Hugging Face models via Hugging Face interface
        if self.huggingface_api_token:
            _llm = self._get_huggingface_llm(temperature)
            if _llm is not None:
                return _llm

        err_msg = "No valid LLM provider available. Please set MISTRAL_API_KEY or HUGGINGFACE_API_TOKEN."
        self.log.error(err_msg)
        raise RuntimeError(err_msg)

    def _get_huggingface_llm(self, temperature: float = 0.3):
        """Initializes a chat model using Hugging Face interface (Inference API)."""
        try:
            from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
            hf_model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
            self.log.info(f"Initializing Hugging Face Chat Model via Hugging Face interface (model: {hf_model})...")
            endpoint = HuggingFaceEndpoint(
                repo_id=hf_model,
                temperature=max(0.01, temperature),
                huggingfacehub_api_token=self.huggingface_api_token,
                max_new_tokens=1024,
            )
            return ChatHuggingFace(llm=endpoint)
        except Exception as hf_err:
            self.log.error(f"Hugging Face interface initialization error: {hf_err}")
            return None