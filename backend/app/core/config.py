import os
import secrets
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)


class Settings:
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ENV: str = os.getenv("ENV")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL")

    # AWS
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT")

    # MySQL
    DB_HOST: str = os.getenv("DB_HOST")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    # Neo4j
    NEO4J_ENDPOINT: str = os.getenv("NEO4J_ENDPOINT")
    NEO4J_USER: str = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")


settings = Settings()
