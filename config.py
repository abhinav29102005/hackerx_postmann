# hackrx_app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Loads and validates application settings from environment variables."""
    
    # Load settings from a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # API Keys
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    AUTH_BEARER_TOKEN: str

    # Model Configuration
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o"
    PINECONE_INDEX_NAME: str = "hackrx-retrieval-system"
    EMBEDDING_DIMENSION: int = 1536
    CHUNK_SIZE_TOKENS: int = 500
    CHUNK_OVERLAP_TOKENS: int = 50

# Create a single settings instance to be used across the application
settings = Settings()