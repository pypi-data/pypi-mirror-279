import logging
from decimal import Decimal
from typing import Any, Generator, Literal

import boto3
from boto3.dynamodb.conditions import Attr, Key
from more_itertools import batched
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table
from pydantic_settings import BaseSettings

from rooms_shared_services.src.exceptions.storage import MoreThanOneItemFound
from rooms_shared_services.src.storage.abstract import AbstractStorageClient
from rooms_shared_services.src.storage.models import BaseDynamodbModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ConditionLiteral = Literal["OR", "AND"]
FilterAttrCondition = Literal[
    "attribute_type",
    "begins_with",
    "between",
    "contains",
    "eq",
    "exists",
    "gt",
    "gte",
    "is_in",
    "lt",
    "lte",
    "ne",
    "not_exists",
    "size",
]


class DynamodbSettings(BaseSettings):
    table: str


class DynamodbStorageClient(AbstractStorageClient):
    def __init__(
        self,
        tablename: str,
        region_name: str = "us-east-1",
        endpoint_url: str | None = None,
        create_table_params: dict | None = None,
    ):
        """Set attributes.Create db table if needed.

        Args:
            tablename (str): _description_
            region_name (str): _description_. Defaults to "us-east-1".
            endpoint_url (str | None): _description_. Defaults to None.
            create_table_params (dict | None): _description_. Defaults to None.
        """
        resource_params = {
            "region_name": region_name,
        }
        if endpoint_url:
            resource_params.update({"endpoint_url": endpoint_url})
        dynamodb_resource: DynamoDBServiceResource = boto3.resource("dynamodb", **resource_params)  # type: ignore
        if create_table_params:
            if "ProvisionedThroughput" not in create_table_params:
                create_table_params.update(
                    {
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 5,
                            "WriteCapacityUnits": 5,
                        },
                    },
                )
            dynamodb_resource.create_table(TableName=tablename, **create_table_params)
        self.table: Table = dynamodb_resource.Table(tablename)  # type: ignore
        self.client: DynamoDBClient = boto3.client("dynamodb", **resource_params)
        logger.info("Dynamodb storage slient initiated with table {}".format(self.table.name))

    def __call__(self):
        logger.info("Hello world")

    def retrieve(self, key: dict, **call_params) -> dict | None:
        response = self.table.get_item(Key=key, **call_params)
        try:
            return response["Item"]
        except KeyError:
            return None

    def get_data_model(self, key: dict, model_type: type[BaseDynamodbModel], **call_params):
        data_item = self.retrieve(key=key, **call_params)
        if data_item is None:
            return None
        return model_type.validate_stored_item_with_none(data_item)

    def index_query(  # noqa: WPS211
        self,
        index_name: str,
        partition_key_name: str,
        partition_key_value: str,
        sort_key_name: str | None = None,
        sort_key_value: str | None = None,
        **call_params,
    ) -> dict:
        key_condition_expression = Key(partition_key_name).eq(partition_key_value)
        if sort_key_name and sort_key_value:
            key_condition_expression = key_condition_expression & Key(sort_key_name).eq(sort_key_value)
        return self.table.query(IndexName=index_name, KeyConditionExpression=key_condition_expression)

    def retrieve_from_index(self, index_name: str, partition_key_name: str, partition_key_value: str, **call_params):
        resp = self.index_query(
            index_name=index_name,
            partition_key_name=partition_key_name,
            partition_key_value=partition_key_value,
            **call_params,
        )
        match resp["Count"]:
            case 1:
                return resp["Items"][0]
            case 0:
                return None
            case _:
                raise MoreThanOneItemFound(resp["Items"])

    def list_from_index(self, index_name: str, partition_key_name: str, partition_key_value: str, **call_params):
        resp = self.index_query(
            index_name=index_name,
            partition_key_name=partition_key_name,
            partition_key_value=partition_key_value,
            **call_params,
        )
        match resp["Count"]:
            case 0:
                return []
            case _:
                return resp["Items"]

    def create(self, table_item: dict, **call_params) -> dict:
        return dict(self.table.put_item(Item=table_item, **call_params))

    def update(self, key: dict, attribute_updates: dict, **call_params) -> dict:
        update_expression = "SET "
        expression_attribute_values = {}
        attribute_update_items = attribute_updates.items()
        for idx, update in enumerate(attribute_update_items):
            value_name = ":val{}".format(idx)
            update_value = update[1]
            update_value = Decimal(str(update_value)) if isinstance(update_value, (int, float)) else update_value
            update_expression = "{} {} = {},".format(update_expression, update[0], value_name)
            expression_attribute_values[value_name] = update_value
        update_expression = update_expression[:-1]
        print(
            "update item: key {}, UpadteExspression {}, ExpressionAttributeValues {}".format(
                key,
                update_expression,
                expression_attribute_values,
            ),
        )
        return dict(
            self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                **call_params,
            ),
        )

    def delete(self, key: dict, **call_params) -> dict:
        return dict(self.table.delete_item(Key=key, **call_params))

    def bulk_retrieve(self, keys: list[dict], **call_params) -> list[dict | None]:
        return [self.retrieve(key=key, **call_params) for key in keys]

    def bulk_create(self, table_items: list[dict], **call_params) -> None:
        with self.table.batch_writer() as batch:
            for table_item in table_items:
                batch.put_item(Item=table_item, **call_params)

    def bulk_update(self, keys: list[dict[Any, Any]], attribute_updates_list: list[dict], **call_params) -> list[dict]:
        if len(keys) == len(attribute_updates_list):
            responses = []
            for key, attribute_updates in zip(keys, attribute_updates_list):
                responses.append(self.update(key=key, attribute_updates=attribute_updates, **call_params))
            return responses
        raise ValueError("Keys and attribute_updates_list must be of equal size")

    def bulk_delete(self, keys: list[dict], **call_params) -> None:
        with self.table.batch_writer() as batch:
            for key in keys:
                batch.delete_item(Key=key, **call_params)

    def bulk_get(
        self,
        filter_params: dict | None = None,
        condition: ConditionLiteral = "AND",
        filter_attr_condition: FilterAttrCondition = "eq",
        negate: bool = False,
    ):
        scan_params = self.create_scan_params(
            filter_params=filter_params,
            condition=condition,
            filter_attr_condition=filter_attr_condition,
            negate=negate,
        )
        resp = self.table.scan(**scan_params)
        return resp["Items"]

    def create_scan_params(
        self,
        filter_attr_condition: FilterAttrCondition,
        condition: ConditionLiteral,
        negate: bool,
        filter_params: dict | None = None,
    ):
        scan_params = {}
        if filter_params:
            FilterExpression = self.create_filter_expression(  # noqa: N806
                filter_params=filter_params,
                filter_attr_condition=filter_attr_condition,
                condition=condition,
                negate=negate,
            )  # noqa: N806
            scan_params.update({"FilterExpression": FilterExpression})
        return scan_params

    def create_filter_expression(
        self,
        filter_params: dict,
        filter_attr_condition: FilterAttrCondition,
        condition: ConditionLiteral,
        negate: bool = False,
    ):
        filter_params_list = list(filter_params.items())
        first_params_item = filter_params_list.pop(0)
        attr_method = getattr(Attr(first_params_item[0]), filter_attr_condition)
        FilterExpression = attr_method(first_params_item[1])  # noqa: N806
        for next_params_item in filter_params_list:
            match condition:
                case "AND":
                    FilterExpression = FilterExpression & Attr(next_params_item[0]).eq(  # type: ignore # noqa: N806
                        next_params_item[1],
                    )
                case "OR":
                    FilterExpression = FilterExpression | Attr(next_params_item[0]).eq(  # type: ignore # noqa: N806
                        next_params_item[1],
                    )
                case _:
                    raise ValueError("Invalid filter expression condition")
        if negate:
            FilterExpression = ~(FilterExpression)  # noqa: N806
        return FilterExpression

    def validate_data_elem(self, data_elem_value: dict) -> str | int | float | dict | list | None:
        data_type = list(data_elem_value.keys())[0]
        parsed_value = data_elem_value[data_type]
        validated_value: str | int | float | dict | list | None
        match data_type:
            case "S":
                assert isinstance(parsed_value, str)
                validated_value = parsed_value
                if validated_value == "None":
                    validated_value = None
            case "N":
                assert isinstance(parsed_value, str)
                if "." in parsed_value:
                    validated_value = float(parsed_value)
                else:
                    validated_value = int(parsed_value)
            case "BOOL":
                match parsed_value:
                    case "false":
                        validated_value = False  # noqa: WPS220
                    case "true":
                        validated_value = True  # noqa: WPS220
                    case _:
                        raise ValueError("invalid boolean")  # noqa: WPS220
            case "NULL":
                validated_value = None
            case "M":
                assert isinstance(parsed_value, dict)
                validated_value = {
                    elem_key: self.validate_data_elem(elem_value) for elem_key, elem_value in parsed_value.items()
                }
            case "L":
                validated_value = [self.validate_data_elem(elem_item) for elem_item in parsed_value]
        return validated_value

    def parse_annotated_response(self, data_item: dict):
        return {
            data_elem_key: self.validate_data_elem(data_elem_value)
            for data_elem_key, data_elem_value in data_item.items()
        }

    @staticmethod
    def create_value_type(attr_value):
        match attr_value:
            case int():
                return {"N": str(attr_value)}
            case str():
                return {"S": attr_value}

    def create_pagination_filter_expression(self, filter_params: dict):
        filter_elements = [
            ("{} = :name_{}".format(key, idx), (":name_{}".format(idx), self.create_value_type(key_value)))
            for idx, (key, key_value) in enumerate(filter_params.items())
        ]
        expression_elements = [elem[0] for elem in filter_elements]
        attribute_elements = [elem[1] for elem in filter_elements]
        filter_expression = ",".join(expression_elements)
        attribute_value_dict = dict(attribute_elements)
        return filter_expression, attribute_value_dict

    def list_for_partition_key(
        self,
        partition_key_name: str,
        partition_key_value: str,
        item_model_type: type[BaseDynamodbModel] | None = None,
        ascending: bool = True,
    ):
        key_condition_expression = Key(partition_key_name).eq(partition_key_value)
        resp = self.table.query(KeyConditionExpression=key_condition_expression, ScanIndexForward=ascending)
        table_items = resp["Items"]
        if item_model_type:
            return [item_model_type.validate_stored_item_with_none(data_dict=table_item) for table_item in table_items]
        return table_items

    def retrieve_for_partition_key(
        self,
        partition_key_name: str,
        partition_key_value: str,
        item_model_type: type[BaseDynamodbModel] | None = None,
        ascending: bool = True,
    ):
        query_list = self.list_for_partition_key(
            partition_key_name=partition_key_name,
            partition_key_value=partition_key_value,
            item_model_type=item_model_type,
            ascending=ascending,
        )
        return query_list[0]

    def batch_retrieve(self, keys: list[dict[Any, Any]]):
        res_list = []
        for chunk in batched(keys, 100):
            res = self.retrieve_by_chunk(keys=chunk)
            listed_res = [res[chunk_item["id"]] for chunk_item in chunk]
            res_list.extend(listed_res)
        return res_list

    def retrieve_by_chunk(
        self,
        keys: list[dict[Any, Any]] | None = None,
        table_items: list[dict] | None = None,
        request_items: dict[str, dict] | None = None,
    ):
        table_items = table_items or []
        if not request_items and keys is not None:
            key_list = [
                {key_item[0]: self.create_value_type(key_item[1]) for key_item in key_entry.items()}
                for key_entry in keys
            ]
            request_items = {self.table.name: {"Keys": key_list}}
        resp = self.client.batch_get_item(RequestItems=request_items)
        table_items.extend(resp["Responses"][self.table.name])
        if resp["UnprocessedKeys"]:
            return self.retrieve_by_chunk(table_items=table_items, request_items=resp["UnprocessedKeys"])
        parsed_response = [self.parse_annotated_response(data_item=table_item) for table_item in table_items]
        return {resp_item["id"]: resp_item for resp_item in parsed_response}

    def batch_update(self, keys: list[dict[Any, Any]], attribute_updates_list: list[dict], **call_params):
        if None in attribute_updates_list:
            raise ValueError("Null attribute update item is not allowed")
        stored_items = self.batch_retrieve(keys=keys)
        if None in stored_items:
            raise ValueError("Could not retrieve a table item for update")
        remove_keys = [
            [remove_key for remove_key in attribute_update_dict.keys() if attribute_update_dict[remove_key] is None]
            for attribute_update_dict in attribute_updates_list
        ]
        updated_items = [{**table_item, **update} for table_item, update in zip(stored_items, attribute_updates_list)]
        updated_items = [
            {item_key: item_value for item_key, item_value in updated_items.items() if item_key not in remove_key_elems}
            for updated_items, remove_key_elems in zip(updated_items, remove_keys)
        ]
        updated_items = [self.validate_item_values(updated_item) for updated_item in updated_items]
        with self.table.batch_writer() as batch:
            for updated_item in updated_items:
                batch.put_item(Item=updated_item)
        logger.info("Batch update completed at table {}".format(self.table.name))

    def validate_item_values(self, table_item_dict: dict):
        return {key: self.convert_value(item_value) for key, item_value in table_item_dict.items()}

    def convert_value(self, table_item_value: Any):
        match table_item_value:
            case float():
                return Decimal(str(table_item_value))
            case dict():
                return {key: self.convert_value(item_value) for key, item_value in table_item_value.items()}
            case _:
                return table_item_value

    def iterate_annotated_responses(self, table_items):
        for db_item in table_items:  # noqa: WPS526
            yield self.parse_annotated_response(db_item)

    def get_by_pages(
        self,
        batch_size: int | None = None,
        page_size: int = 100,
        consistent_read: bool = False,
        filter_by: dict | None = None,
    ):
        batch_size = batch_size or page_size
        yield from batched(
            self.iterate_table_items(
                page_size=page_size,
                consistent_read=consistent_read,
                filter_by=filter_by,
            ),
            batch_size,
        )

    def iterate_table_item_models(self, item_model_type: BaseDynamodbModel, table_items: list[dict]):
        for annotated_table_item in self.iterate_annotated_responses(table_items=table_items):  # noqa: WPS526
            yield item_model_type.validate_dynamodb_item(annotated_table_item)

    def clean_field(self, fieldname: str, key_fields: list[str] | None = None):
        key_fields = key_fields or ["id"]
        counter = 0
        for page in self.get_by_pages():
            keys = [{key_field: table_item[key_field] for key_field in key_fields} for table_item in page]
            attribute_updates_list = [{fieldname: None} for _ in keys]
            logger.info("Attribute update list creaed for cleaning.")
            self.batch_update(keys=keys, attribute_updates_list=attribute_updates_list)
            counter += len(page)
            logger.info("{} elements cleaned".format(counter))

    def iterate_table_items(
        self,
        page_size: int | None = 100,
        consistent_read: bool = False,
        filter_by: dict | None = None,
        item_model_type: BaseDynamodbModel | None = None,
    ) -> Generator[list[dict], None, None]:
        paginator = self.client.get_paginator("scan")
        scan_params = {"TableName": self.table.name}
        if filter_by:
            filter_expression, attribute_values = self.create_pagination_filter_expression(filter_params=filter_by)
            scan_params.update({"FilterExpression": filter_expression, "ExpressionAttributeValues": attribute_values})
        if page_size:
            scan_params.update({"PaginationConfig": {"PageSize": page_size}})
        for page in paginator.paginate(**scan_params, ConsistentRead=consistent_read):
            table_items = page["Items"]
            logger.info("Collected {} page items from dynamodb table {}".format(len(table_items), self.table.name))
            if item_model_type:
                yield from self.iterate_table_item_models(table_items=table_items, item_model_type=item_model_type)
            else:
                yield from self.iterate_annotated_responses(table_items=table_items)
