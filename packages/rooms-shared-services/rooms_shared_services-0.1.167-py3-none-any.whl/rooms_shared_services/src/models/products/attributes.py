from enum import Enum
from uuid import UUID, uuid4

from pydantic import Field, field_validator

from rooms_shared_services.src.models.texts.languages import Language
from rooms_shared_services.src.storage.models import BaseDynamodbModel


class AttributeVariant(Enum):
    FURNITURE_TYPES = "FURNITURE_TYPES"
    MATERIALS = "MATERIALS"
    COUNTRY_OF_ORIGIN = "COUNTRY_OF_ORIGIN"
    DELIVERY_TERM = "DELIVERY_TERM"


class ProductAttribute(BaseDynamodbModel):
    id: UUID = Field(default_factory=uuid4)
    attr_language: Language
    attr_name: str
    attr_terms: list[str]

    @field_validator("attr_language", mode="before")
    def attr_language(cls, field_value):
        if isinstance(field_value, str):
            try:
                return getattr(Language, field_value)
            except AttributeError:
                pass
        return field_value

    def translate_raw_term(self, raw_attr: "ProductAttribute", raw_term: str):
        term_index = raw_attr.attr_terms.index(raw_term)
        return self.attr_terms[term_index]
