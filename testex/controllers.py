from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

from testex.utils import get_diff
from testex.utils import set_data
from testex.utils import validate
from flasgger import swag_from

# Register flask blueprints for API
api = Blueprint('diff', __name__)


def reply(passed=None, errors=None, data_id=None, side=None):
    """
    Reply template for API
    :param passed: whether request passed or not
    :param errors: which errors happened if were
    :param data_id: index of Data object
    :param side: "left" or "right" parameter
    :return: json response

    """
    return jsonify(
        {"errors": errors,
         "success": passed,
         "action": "set",
         "side": side,
         "id": data_id})


@api.route('/')
def index():
    """
    Index page
    :return: template of index.html
    """
    return render_template("index.html")


@swag_from('left.yaml')
@api.route('/v1/diff/<int:data_id>/left', methods=['POST'])
def left(data_id):
    """
    POST request endpoint, receiving "left" parameter
    :param data_id: index of Data object
    :return: JSON reply template or 400 HTTP error in case of wrong request
    """
    data = validate(request.json)
    if not data:
        abort(400)
    else:
        s = set_data(data_id, "left", data['data'])
    if s:
        return reply(passed=True, errors=[], data_id=data_id, side="left")
    else:
        return reply(passed=False, errors=[], data_id=data_id, side="left")


@swag_from('right.yaml')
@api.route('/v1/diff/<int:data_id>/right', methods=['POST'])
def right(data_id):
    """
    POST request endpoint, receiving "right" parameter
    :param data_id: index of Data object
    :return: JSON reply template or 400 HTTP error in case of wrong request
    """
    data = validate(request.json)
    if not data:
        abort(400)
    else:
        s = set_data(data_id, "right", data['data'])
    if s:
        return reply(passed=True, errors=[], data_id=data_id, side="right")
    else:
        return reply(passed=False, errors=[], data_id=data_id, side="right")


@swag_from('diff.yaml')
@api.route('/v1/diff/<int:data_id>', methods=['GET'])
def calc_diff(data_id):
    """
    GET request, receiving Data index
    :param data_id: index of Data object
    :return: difference between right and left sieds, either 400 HTTP error in
            case of error.
    """
    diff = get_diff(data_id)
    if diff:
        return jsonify(diff)
    else:
        abort(400)
