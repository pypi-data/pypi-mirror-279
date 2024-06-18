from pydantic_settings import SettingsConfigDict

from rooms_shared_services.src.settings.dynamodb.base import BaseDynamodbSettings


class Settings(BaseDynamodbSettings):
    model_config = SettingsConfigDict(env_prefix="dialog_messages_")
