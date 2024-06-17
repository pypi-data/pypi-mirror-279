import json
from decimal import Decimal
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel

from rooms_shared_services.src.encoders.json import RawDynamodbEncoder

UNSET = Literal["UNSET"]


class BaseDynamodbModel(BaseModel):
    @classmethod
    def create_with_id(cls, **attributes):
        model_id = uuid4()
        value_dict = {"id": model_id, **attributes}
        return cls.model_validate(value_dict)

    def convert_value(self, item_value, exclude_unset: bool):
        match item_value:
            case BaseDynamodbModel():
                converted_item_value = item_value.dynamodb_dump(exclude_unset=exclude_unset)
            case int():
                converted_item_value = Decimal(item_value)
            case float():
                converted_item_value = Decimal(str(item_value))
            case dict():
                converted_item_value = self.convert_dict(item_value, exclude_unset=exclude_unset)
            case list():
                converted_item_value = [
                    self.convert_value(item_value_item, exclude_unset=exclude_unset) for item_value_item in item_value
                ]
            case Enum():
                converted_item_value = item_value.name
            case _:
                converted_item_value = str(item_value)
        return converted_item_value

    def convert_to_raw(self, data_dict: dict, root_level: bool = False) -> dict:
        return {
            item_key: self.convert_to_raw_value(item_value, root_level=root_level)
            for (item_key, item_value) in data_dict.items()
        }

    def convert_to_raw_value(self, item_value: Any, root_level: bool = False):
        match item_value:
            case Decimal():
                item_value_dict = {"N": str(item_value)}
            case dict():
                item_value_dict = {"M": json.dumps(item_value, cls=RawDynamodbEncoder)}
            case list():
                item_value_dict = {"L": json.dumps(item_value, cls=RawDynamodbEncoder)}
            case str():
                item_value_dict = {"S": item_value}
            case bool():
                item_value_dict = {"BOOL": "true" if item_value else "false"}
            case None:
                item_value_dict = {"NULL": ""}
            case _:
                raise ValueError("Invalid item value type")
        return item_value_dict if root_level else list(item_value_dict.values()).pop()

    def convert_dict(self, item_dict: dict, exclude_unset: bool):
        return {
            item_key: self.convert_value(item_value, exclude_unset=exclude_unset)
            for (item_key, item_value) in item_dict.items()
        }

    def dynamodb_dump(self, exclude_unset: bool = True, include: set[str] | None = None, raw: bool = False):
        item_dict = self.model_dump(exclude_unset=exclude_unset, include=include)
        converted = self.convert_dict(item_dict=item_dict, exclude_unset=exclude_unset)
        if raw:
            converted = self.convert_to_raw(converted, root_level=True)
        return converted

    @classmethod
    def validate_value(cls, item_value: Any) -> Any:
        match item_value:
            case list():
                validated_value = [cls.validate_value(item_value=product_elem) for product_elem in item_value]
            case "None":
                validated_value = None
            case dict():
                return {
                    elem_key: cls.validate_value(item_value=elem_value) for elem_key, elem_value in item_value.items()
                }
            case _:
                validated_value = item_value
        return validated_value

    @classmethod
    def parse_raw_record_attribute(cls, attr_dict: dict[str, str]) -> Any:
        item_key, item_value = list(attr_dict.items()).pop()
        match item_key:
            case "S":
                res = str(item_value)
            case "N":
                res = float(item_value)
            case "B":
                res = item_value
            case "BOOL":
                res = item_value == "true"
            case "NULL":
                res = None
            case "M" | "L":
                res = json.loads(item_value)
            case "SS" | "NS" | "BS":
                res = set(item_value)
            case _:
                raise ValueError("Invalid data type")
        return res

    @classmethod
    def validate_dynamodb_item(cls, data_dict: dict, from_raw: bool = False):
        key_value_dict = {}
        for product_key, product_value in data_dict.items():
            validated_key = product_key
            if from_raw:
                product_value = cls.parse_raw_record_attribute(attr_dict=product_value)
            match product_key:
                case _:
                    pass
            validated_value = cls.validate_value(item_value=product_value)
            key_value_dict.update({validated_key: validated_value})

        return cls.model_validate(key_value_dict)

    @classmethod
    def validate_from_raw_record(cls, data_dict: dict):
        key_value_dict = {}
        for product_key, product_value in data_dict.items():
            validated_key = product_key
            match product_key:
                case _:
                    pass
            validated_value = cls.validate_value(item_value=product_value)
            key_value_dict.update({validated_key: validated_value})

        return cls.model_validate(key_value_dict)
