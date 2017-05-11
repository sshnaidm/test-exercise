import base64
import binascii
import json
from testex.models import Data
from testex.models import db


def set_data(data_id, side, data):
    """
    Add data to ``Data`` object if exists and create it if it doesn't
    :param data_id: ``Data`` index
    :param side: "left" or "right" parameter
    :param data: value of "left" or "right" parameter
    :return: True if succeeded and False if there was fail
    """
    d = Data.query.get(data_id)
    if d:
        setattr(d, side, data)
        db.session.add(d)
        db.session.commit()
        return True
    else:
        new_data = Data(int(data_id))
        setattr(new_data, side, data)
        try:
            db.session.add(new_data)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False


def get_diff(data_id):
    """
    Get diff between left and right from ``Data`` object
    :param data_id: index of ``Data`` object
    :return: either diff attribute of ``Data`` or None if it's None
    """
    d = Data.query.get(data_id)
    return d.diff if d else None


def validate(arg):
    """
    Validate input parameters for `left` and `right`
    :param arg: input from request
    :return: dictionary of {'data': base64encoded_stirng} if valid or
            False if not valid
    """
    if not arg:
        return False
    if isinstance(arg, str) or isinstance(arg, bytes):
        try:
            arg = json.loads(arg)
        except Exception as e:
            print(e)
            return False
    if not arg.get("data"):
        return False
    try:
        base64.b64decode(arg["data"])
    except binascii.Error:
        return False
    return arg
