import datetime
import decimal
import uuid
import json


def JSONhandler(obj):
    """
    Json Handler for formatting different python types into json
    :param obj: object of any type which needs to be serialized to json
    :return: json serializable type (usually str)
    """
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, (decimal.Decimal, uuid.UUID)):
        return "{}".format(obj)
    if isinstance(obj, set):
        return ", ".join(obj)
    if isinstance(obj, memoryview):
        return bytes(obj)
    return json.JSONEncoder().default(obj)
