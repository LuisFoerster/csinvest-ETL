from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STEAM_USERNAME: str
    STEAM_PASSWORD: str
    STEAM_WEB_API_KEY: str

    model_config = {
        "env_file": "../../.env",
        "extra": "ignore",
        "env_ignore_empty": True,
    }


settings = Settings()
