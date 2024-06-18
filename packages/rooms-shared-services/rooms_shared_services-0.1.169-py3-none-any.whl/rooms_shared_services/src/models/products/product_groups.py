from uuid import UUID

from rooms_shared_services.src.models.relations import GeoRelatedValues
from rooms_shared_services.src.storage.models import UNSET, BaseDynamodbModel


class ProductGroup(BaseDynamodbModel):
    id: UUID | UNSET = "UNSET"
    group_name: str | UNSET = "UNSET"
    brands: list[str] | UNSET = "UNSET"
    base_margins: GeoRelatedValues | UNSET = "UNSET"

    @classmethod
    def create_with_id(cls, base_margins: GeoRelatedValues | None = None, **attributes):
        if base_margins is None:
            base_margins = GeoRelatedValues()
        return super().create_with_id(base_margins=base_margins, **attributes)
