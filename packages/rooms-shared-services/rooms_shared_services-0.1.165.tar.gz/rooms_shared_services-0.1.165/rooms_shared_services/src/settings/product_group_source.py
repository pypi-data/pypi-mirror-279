from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="product_group_source_")

    tablename: str
    region_name: str = "us-east-1"
    name_indexname: str
