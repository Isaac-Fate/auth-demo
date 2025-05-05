from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pathlib import Path
from dotenv import find_dotenv


class Config(BaseSettings):

    frontend_base_url: str

    # Postgres
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int
    postgres_data_dir: Path
    postgres_uri: str

    # Google OAuth
    google_client_id: str
    google_client_secret: str

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str

    # Configuration of this schema
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("postgres_data_dir", mode="after")
    @classmethod
    def resolve_path(cls, path: Path) -> Path:

        return path.expanduser().resolve()


def load_config() -> Config:

    # Find the dotenv file based on the ENV
    env_filepath = find_dotenv()

    # Load the configuration
    config = Config(_env_file=env_filepath)

    return config
