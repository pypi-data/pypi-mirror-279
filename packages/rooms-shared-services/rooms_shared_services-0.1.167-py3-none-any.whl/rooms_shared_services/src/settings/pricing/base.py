from tempfile import NamedTemporaryFile

import boto3
from pydantic import create_model
from pydantic_settings import BaseSettings
from yaml import load as yaml_load

try:
    from yaml import CLoader as Loader  # noqa: WPS433
except ImportError:
    from yaml import Loader  # noqa: WPS440, WPS433
s3_client = boto3.client("s3")

with NamedTemporaryFile(suffix=".yaml") as ntf:
    s3_client.download_file("rooms-setup-data", "attributes.yaml", ntf.name)
    with open(ntf.name) as attr_fileobj:
        attributes = yaml_load(attr_fileobj.read(), Loader=Loader)
        furniture_types = attributes["furniture_types"]


FurnitureTypeAttributeCollection = create_model(
    "FurnitureTypeAttributeCollection",
    **{furniture_type: (int, ...) for furniture_type in furniture_types},
)


class PriceMarginSettings(BaseSettings, FurnitureTypeAttributeCollection):
    ...
