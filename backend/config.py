from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  host: str = "0.0.0.0"
  port: int = 8000
  reload: bool = True
  network: str = "mainnet"

settings = Settings()