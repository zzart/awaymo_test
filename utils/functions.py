""" Helper functions for dealing with JSON and time conversions """

import datetime
import decimal
import uuid
import json
from typing import Any


def json_handler(obj: Any)-> str:
    """
    Json Handler for formatting different python types into json
    :param obj: object of any type which needs to be serialized to json
    :return: json serializable type
    """
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, (decimal.Decimal, uuid.UUID)):
        return "{}".format(obj)
    if isinstance(obj, set):
        return ", ".join(obj)
    return json.JSONEncoder().default(obj)


def format_time(time_str: str, format_str: str)-> datetime.time:
    """
    Given time_string converts to valid datetime.time
    :param time_str: ie. '20:34' or '23/02/2019 20:32'
    :param format_str: ie '%H:%M' or any other datetime/time format
    :return: valid datetime.time or raises ValueError
    """
    try:
        return datetime.datetime.strptime(time_str, format_str).time()
    except ValueError:
        raise ValueError
