import secrets

from bson import ObjectId


def api_response(success=True, data=None, message="Success"):
    """
        Api response structure
    """
    return {
        "success": success,
        "message": message,
        "data": data
    }

def code_generator():
    """
        Generate 6 digit code for email validation
    """
    return f"{secrets.randbelow(1_000_000):06}"

def dict_string_to_objectid(data: dict):
    """
        convert a dictionary of id strings to ObjectId
    :param data: dictionary
    :return:
    """

    new_dict = {}

    for key, value in data.items():
        new_dict[key] = ObjectId(value)

    return new_dict

def string_to_objectid(value: str):
    """
        convert a string of id to ObjectId
    :param value: string
    :return:
    """

    return ObjectId(value)


class DictObj:
    """
        Convert dictionaries to Object
    """
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)