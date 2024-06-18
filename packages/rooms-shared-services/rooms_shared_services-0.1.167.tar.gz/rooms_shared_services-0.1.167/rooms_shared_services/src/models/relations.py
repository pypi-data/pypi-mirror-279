from enum import Enum

from rooms_shared_services.src.storage.models import BaseDynamodbModel


class CurrencyCode(str, Enum):
    ILS = "ILS"
    EUR = "EUR"
    RUB = "RUB"
    USD = "USD"
    PLN = "PLN"
    GBP = "GBP"


class GeoRelatedValues(BaseDynamodbModel):
    IL: str | float | int | None = None
