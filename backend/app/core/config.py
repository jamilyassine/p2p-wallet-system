from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()