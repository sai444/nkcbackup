from flask import jsonify, Blueprint

role_api = Blueprint('role_api',__name__)

@role_api.route('/role')
def roles():
        from models import role
        things = role.query.all()
        results = []

        for shiftObj in things:
            serial = role.serialize(shiftObj)
            print(serial)
            results.append(serial)
        return jsonify(results)

@role_api.route('/plant')
def shift_get():
    from models import companylocation
    things = companylocation.query.all()
    print("shift")
    results = []

    for shiftObj in things:
        serial = companylocation.serialize(shiftObj)
        print(serial)
        results.append(serial)

    return jsonify(results), 200