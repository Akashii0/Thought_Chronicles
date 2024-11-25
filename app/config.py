from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # BACKEND_CORS_ORIGINS: Annotated[
    #     list[AnyUrl] | str, BeforeValidator(parse_cors)
    # ] = []
    # FRONTEND_HOST: str = "http://localhost:3000"
    
    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def all_cors_origins(self) -> list[str]:
    #     return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
    #         self.FRONTEND_HOST
    #     ]
    class Config:
        env_file = ".env"
        
settings = Settings()