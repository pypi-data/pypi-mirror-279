from pydantic_settings import SettingsConfigDict

from rooms_shared_services.src.settings.dynamodb.base import BaseDynamodbSettings


class Settings(BaseDynamodbSettings):
    model_config = SettingsConfigDict(env_prefix="product_source_")

    sku_indexname: str
    original_ident_indexname: str
    ident_code: str
    ident_key: str
