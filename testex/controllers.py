from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from testex.utils import get_diff
from testex.utils import set_data
from testex.utils import validate


api = Blueprint('diff', __name__)


def reply(passed=None, errors=None, data_id=None, side=None):
    return jsonify(
        {"errors": errors,
         "success": passed,
         "action": "set",
         "side": side,
         "id": data_id})


@api.route('/')
def index():
    return render_template("index.html")


@api.route('/v1/diff/<int:data_id>/left', methods=['POST'])
def left(data_id):
    data = validate(request.json)
    if not data:
        abort(400)
    else:
        s = set_data(data_id, "left", data['data'])
    if s:
        return reply(passed=True, errors=[], data_id=data_id, side="left")
    else:
        return reply(passed=False, errors=[], data_id=data_id, side="left")


@api.route('/v1/diff/<int:data_id>/right', methods=['POST'])
def right(data_id):
    data = validate(request.json)
    if not data:
        abort(400)
    else:
        s = set_data(data_id, "right", data['data'])
    if s:
        return reply(passed=True, errors=[], data_id=data_id, side="right")
    else:
        return reply(passed=False, errors=[], data_id=data_id, side="right")


@api.route('/v1/diff/<int:data_id>', methods=['GET'])
def calc_diff(data_id):
    diff = get_diff(data_id)
    if diff:
        return jsonify(diff)
    else:
        abort(400)
