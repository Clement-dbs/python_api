from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings (BaseSettings):
    app_name: str = Field("ML Iris API", description="Nom de l'app")
    debug: bool = Field(False, description="Booleen debug")
    log_level: str = Field("INFO", description="Niveau des logs")
    model_path: str = Field("models/iris_model.pkl", description="Chemin du model")
    report_path: str = Field("models/training_report.json", description="Rapport d'entrainement")

    model_config = SettingsConfigDict(env_file="/.env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
    

