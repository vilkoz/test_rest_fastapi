from typing import Optional, List, Union
from pydantic import BaseSettings, validator, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str

    DB_URI: str

    API_V1_STR: str = "/api/v1"

    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        case_sensitive = True

settings = Settings()