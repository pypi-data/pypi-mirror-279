from typing import Any
from uuid import UUID, uuid4

from pydantic import Field, HttpUrl, field_validator

from rooms_shared_services.src.models.texts.languages import Language
from rooms_shared_services.src.models.texts.translations import TextTranslations
from rooms_shared_services.src.storage.models import BaseDynamodbModel


class ProductCategory(BaseDynamodbModel):
    name: str
    id: int
    parent_id: int | None = None
    parent_name: str | None = None
    description: str | None = None
    image: HttpUrl | None = None
    name_translations: TextTranslations | None = None
    description_translations: TextTranslations | None = None

    @field_validator(
        "image",
        mode="before",
    )
    def coerce_image(cls, item_value: Any):
        if isinstance(item_value, dict):
            return item_value.get("image", None)
        return item_value


class ProductCategoryTranslation(BaseDynamodbModel):
    id: UUID = Field(default_factory=uuid4)
    cat_name: str
    cat_language: Language
    cat_description: str | None = None
    cat_image: HttpUrl | None = None

    @field_validator("cat_name", mode="before")
    def remove_underscores(cls, name_value: Any):
        if isinstance(name_value, str):
            return name_value.replace("_", " ").lower()
        return name_value

    @field_validator("cat_language", mode="before")
    def coerce_language(cls, language_name: Any):
        if isinstance(language_name, str):
            try:
                return getattr(Language, language_name)
            except AttributeError:
                pass
        return language_name
