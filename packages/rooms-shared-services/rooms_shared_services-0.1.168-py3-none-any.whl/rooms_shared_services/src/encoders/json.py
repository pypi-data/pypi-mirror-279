import json
from decimal import Decimal


class RawDynamodbEncoder(json.JSONEncoder):
    def default(self, encode_obj):
        match encode_obj:
            case Decimal():
                return str(encode_obj)
        return super().default(encode_obj)
