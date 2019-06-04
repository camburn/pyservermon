import dataclasses
import uuid
import json


class DataEncoder(json.JSONEncoder):
    """ Custom JSON encoder to handle nonstandard objects for serialisation """
    def default(self, obj: object) -> str:  # pylint: disable=arguments-differ,method-hidden
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if dataclasses.is_dataclass(obj):
            data = dataclasses.asdict(obj)
            data['type'] = obj.__class__.__name__
            return data
        return super().default(obj)

def create_token():
    return 'x1b2'
