from pydantic import BaseSettings


class Settings(BaseSettings):
    """Parses variables from environment on instantiation"""

    db_scheme: str
    db_host: str
    db_username: str
    db_password: str
    db_database: str

    class Config:
        env_file = "app/env/.env"

    @property
    def database_uri(self):
        return f"{self.db_scheme}://{self.db_username}:{self.db_password}@{self.db_host}/{self.db_database}"

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


setting = Settings()
