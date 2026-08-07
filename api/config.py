from pydantic import SecretStr, field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    mistral_api_key: SecretStr
    deepgram_api_key: SecretStr
    sarvam_api_key: SecretStr
    huggingface_api_token: SecretStr
    pinecone_api_key: SecretStr
    pinecone_index_name: str
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    sarvam_stt_translate_url: HttpUrl
    sarvam_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   
        extra="ignore",         
    )

    @field_validator(
        "mistral_api_key", "deepgram_api_key", "sarvam_api_key", "huggingface_api_token", "pinecone_api_key",  mode="after"
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
            "pinecone_api_key": "set" if self.pinecone_api_key else "MISSING",
            "pinecone_index_name": self.pinecone_index_name,
            "pinecone_cloud": self.pinecone_cloud,
            "pinecone_region": self.pinecone_region,
            "sarvam_stt_translate_url": str(self.sarvam_stt_translate_url),
            "sarvam_model": self.sarvam_model,
        }


