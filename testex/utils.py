import base64
import binascii
import json
from testex.models import Data
from testex.models import db


def set_data(data_id, side, data):
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
    d = Data.query.get(data_id)
    return d.diff if d else None


def validate(arg):
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
