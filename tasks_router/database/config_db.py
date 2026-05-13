from pydantic_settings import BaseSettings, SettingsConfigDict

# placeholder for database configuration settings. Dummy values are provided for now.

class Settings(BaseSettings):

    host: str = "localhost"
    port: int = 5432
    username: str = "user"
    password: str = "password"
    database: str = "tasks_db"
    sslmode: str = "verify-full"
    sslrootcert: str = "./global-bundle.pem"

    model_config = SettingsConfigDict(env_file=".env")

    def get_db_url(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_conn_args(self) -> dict[str, str]:
        return {
            "sslmode": self.sslmode,
            "sslrootcert": self.sslrootcert
        }
    
settings: Settings = Settings()