import secrets

import bson
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

    for key, value in data.copy().items():
        try:
            new_dict[key] = ObjectId(value)
        except bson.errors.InvalidId:
            new_dict[key] = value

    return new_dict.copy()

def string_to_objectid(value: str):
    """
        convert a string of id to ObjectId
    :param value: string
    :return:
    """

    return ObjectId(value)

def string_list_to_objectid(values: list) -> list:
    """
        convert a list of id string to ObjectId
    :param values: List containing string ids
    :return: a list where each string is converted to ObjectId
    """

    for value in values:
        if isinstance(value, str):
            values[values.index(value)] = ObjectId(value)

    return values

def build_insert_many_document_list(key_name: str, list_of_values: list):
    """
        To insert many documents when we only have a list of values\r
        we have to convert that list of values into a list\r
        documents.\r

        [value1, value2, ..., valuen] \n
        to\n
        [{"key_name": value1}, {"key_name": value2}, ..., {key_name": valuen}]

    :param key_name: the name of the document key
    :param list_of_values: list of values to process
    :return: list of documents
    """

    documents = []

    for value in list_of_values:
        documents.append({f"{key_name}": value})

    return documents




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