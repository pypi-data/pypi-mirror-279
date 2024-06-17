from pydantic_settings import BaseSettings


class BaseDynamodbSettings(BaseSettings):
    tablename: str
    region_name: str
    endpoint_url: str | None = None
