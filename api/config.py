from pydantic import SecretStr, field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    mistral_api_key: SecretStr
    deepgram_api_key: SecretStr
    sarvam_api_key: SecretStr
    huggingface_api_token: SecretStr

    sarvam_stt_translate_url: HttpUrl
    sarvam_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   
        extra="ignore",         
    )

    @field_validator(
        "mistral_api_key", "deepgram_api_key", "sarvam_api_key", "huggingface_api_token",  mode="after"
    )
    @classmethod
    def not_empty(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("API key cannot be empty")
        return value

    def masked(self) -> dict:
       
        return {
            "mistral_api_key": "set" if self.mistral_api_key else "MISSING",
            "deepgram_api_key": "set" if self.deepgram_api_key else "MISSING",
            "sarvam_api_key": "set" if self.sarvam_api_key else "MISSING",
            "huggingface_api_token": "set" if self.huggingface_api_token else "MISSING",
            "sarvam_stt_translate_url": str(self.sarvam_stt_translate_url),
            "sarvam_model": self.sarvam_model,
        }


