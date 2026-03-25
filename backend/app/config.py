"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: Connection string for the database.
        APP_ENV: Application environment (development, production, testing).
        DEBUG: Enable debug mode.
    """

    DATABASE_URL: str = "mssql+aioodbc:///?odbc_connect=Driver%3D%7BODBC+Driver+17+for+SQL+Server%7D%3BServer%3DDESKTOP-QBCI725%5CSQLEXPRESS%3BDatabase%3DTodoDb%3BTrusted_Connection%3Dyes%3BTrustServerCertificate%3Dyes%3BEncrypt%3Dyes"
    APP_ENV: str = "development"
    DEBUG: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
