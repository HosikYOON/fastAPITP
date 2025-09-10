from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str = "root"
    db_password: str = "12345"
    db_host: str = "localhost"
    db_port: str = "3306"
    db_name: str = "mall"

    class Config:
        case_sensitive = True
        extra = "allow"
        populate_by_name = True

    @property
    def db_url(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property  # 비동기 DB URL
    def async_db_url(self) -> str:
        return f"mysql+asyncmy://{self.db_url}"

    @property  # 동기 DB URL
    def sync_db_url(self) -> str:
        return f"mysql+pymysql://{self.db_url}"


settings = Settings()
