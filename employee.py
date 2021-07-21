from flask import jsonify, Blueprint

employee_api = Blueprint('employee_api', __name__)


@employee_api.route("/employee")
def employee():
    return jsonify({"msg": "Im in employee file"})
