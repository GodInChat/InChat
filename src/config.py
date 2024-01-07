from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from langchain.vectorstores.pgvector import PGVector

load_dotenv()


class Settings(BaseSettings):
    postgres_db: str = Field()
    postgres_vector_db: str = Field()
    postgres_user: str = Field()
    postgres_password: str = Field()
    postgres_port: int = Field()
    postgres_host: str = Field()

    redis_host: str = Field()
    redis_port: str = Field()

    secret_key: str = Field()
    algorithm: str = Field()

    mail_username: str = Field()
    mail_password: str = Field()
    mail_from: str = Field()
    mail_port: int = Field()
    mail_server: str = Field()
    mail_from_name: str = Field()

    ollama_url: str = Field()
    ollama_model: str = Field()


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()


vector_connection_string = PGVector.connection_string_from_db_params(
    driver="psycopg2",
    host=settings.postgres_host,
    port=settings.postgres_port,
    database=settings.postgres_vector_db,
    user=settings.postgres_user,
    password=settings.postgres_password)
