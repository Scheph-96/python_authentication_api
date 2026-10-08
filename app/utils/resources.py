import secrets
from uuid import UUID

from sqlalchemy import Table


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
        Generate 6 a digit code for email validation
    """
    return f"{secrets.randbelow(1_000_000):06}"


def dict_string_to_uuid(data: dict):
    """
        convert a dictionary of id strings to UUID
    :param data: dictionary
    :return:
    """

    new_dict = {}

    for key, value in data.items():
        try:
            new_dict[key] = UUID(value)
        except ValueError:
            new_dict[key] = value

    return new_dict.copy()


def string_to_uuid(value: str):
    """
        convert a string of id to UUID
    :param value: string
    :return:
    """

    return UUID(value)


def string_list_to_uuid(values: list) -> list:
    """
        convert a list of string ids to UUID
    :param values: List containing string ids
    :return: a list where each string is converted to UUID
    """

    for value in values:
        if isinstance(value, str):
            try:
                values[values.index(value)] = UUID(value)
            except ValueError:
                values[values.index(value)] = value

    return values


def build_insert_many_document_list(key_name: str, list_of_values: list):
    """
        To insert many documents when we only have a list of values\r
        we have to convert that list of values into a list\r
        of documents.\r

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


async def drop_all_indexes(db):
    collection_list = await db.list_collection_names()
    for collection_name in collection_list:
        collection = db[collection_name]

        # drop all indexes except _id
        await collection.drop_indexes()


def build_sql_expression_from_dict(table: Table, data: dict) -> list:
    """
        Document can't be used for SQL query so we have
        to convert them into SQL expression.

        {"name": "computer"} => table.columns[computer] == computer
    :param table: The table onto which the query will be performed
    :param data: The document 
    :return:
    """
    expression = []

    for key, value in data.items():
        expression.append((table.columns[key] == value))

    return expression


class DictObj:
    """
        Convert dictionaries to Object
    """

    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val) if isinstance(val, dict) else val)
