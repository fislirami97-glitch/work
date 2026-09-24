from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./crawler.db"
    serper_api_key: str = ""
    request_timeout: int = 20
    user_agent: str = "ProductTrendCrawler/0.1 (+compliant-research)"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
