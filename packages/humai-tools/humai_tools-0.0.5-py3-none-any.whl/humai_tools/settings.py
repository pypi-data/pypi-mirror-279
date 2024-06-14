from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding='utf-8', env_ignore_empty=True)

    directus_access_token: str
    directus_base_url: str = Field(default='https://directus-dev-mrek6efuua-uc.a.run.app')

    tito_api_key: str
    tito_base_url: str = Field(default='http://tito.humai.com.ar')

    campus_base_url: str = Field(default='https://estudiantes.campus.humai.com.ar')
    campus_client_id: str = Field(pattern=r'\w+')
    campus_client_secret: str = Field(pattern=r'\w+')
    campus_access_token: str = Field(default=None, validate_default=False)
