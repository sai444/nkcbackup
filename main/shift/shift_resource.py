from datetime import datetime,date

from flask import Blueprint, jsonify, request



shift_api = Blueprint('shift_api', __name__)


@shift_api.route('/shift')
def shift_get():
    from models import shift
    things = shift.query.all()
    print("shift")
    results = []

    for shiftObj in things:
        serial = shift.serialize(shiftObj)
        print(serial)
        results.append(serial)

    return jsonify(results), 200

@shift_api.route('/shift-by-plant/<plantId>')
def shift_get_plantId(plantId):
    from models import shift
    things = shift.query.filter(shift.plantId == plantId).all()
    print("shift")
    results = []
    if len(things)==0:
        # things = shift.query.all()
        pass

    for shiftObj in things:
        serial = shift.serialize(shiftObj)
        print(serial)
        results.append(serial)

    return jsonify(results), 200

@shift_api.route('/shift', methods=['POST'])
def add_shift():
    from app import db
    from models import shift
    if request.method == 'POST':
        data = request.get_json()
        shift_old = shift.query.filter(shift.name == data['shiftName'], shift.plantId == data['plantId']).first()
        if shift_old:
            data = {"message": f"Shift name already present."}
            return jsonify(data), 500
        # new_shift = shift(text = data['status'], completed = data['completed'], createdon = datetime.datetime.now())
        # new_shift = shift(status=data['status'],shift_name=data['shift_name'],start_time=data['start_time'],end_time=data['end_time'],company_location_id=data['company_location_id'])
        new_shift = shift(status=data['status'],name=data['shiftName'],starttime=data['startTime'],endtime=data['endTime'],plantId = data['plantId'])
        db.session.add(new_shift)
        db.session.commit()

        data = {"message": f"name created successfully"}
        return jsonify(data), 200

@shift_api.route('/shift/<id>', methods=['GET', 'PUT'])
def shiftUpdate(id):
    from app import db
    from models import shift,adminlog
    shiftObj = shift.query.get_or_404(id)
    now = datetime.now()

    if request.method == 'GET':
        response = shift.serialize(shiftObj)
        return jsonify(response)
    
    elif request.method == 'PUT':
        data = request.get_json()
        shift_old = shift.query.filter(shift.name == data['shiftName'] and shift.plantId == data['plantId']).first()
        if shift_old:           
            if int(shift_old.id) != int(id):
                data = {"message": f"shift name already exists"}
                return jsonify(data), 500
        shiftObj.status = True
        shiftObj.name = data['shiftName']
        shiftObj.starttime = data['startTime']
        shiftObj.endtime = data['endTime']
        shiftObj.plantId = data['plantId']

        db.session.add(shiftObj)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data["logger"], module = 'shift', activitydone = 'update', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"shift updated successfully"}
        return jsonify(data), 200

@shift_api.route('/shift/<id>/<logger>', methods=['DELETE'])
def shiftDelete(id, logger):
    from app import db
    from models import shift,adminlog
    shiftObj = shift.query.get_or_404(id)
    now = datetime.now()
    
    if request.method == 'DELETE':
        db.session.delete(shiftObj)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger, module = 'shift', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"name deleted successfully"}
        return jsonify(data), 200

@shift_api.route('/running-shift')
def shift_current():
    from models import shift
    things = shift.query.all()
    print("shift")
    results = []
    now = datetime.now().time()
    print(now)
    for shiftObj in things:
        serial = shift.serialize(shiftObj)
        print(serial)
        print(shiftObj)
        startTime = shiftObj.starttime
        endTime = shiftObj.endtime
        if now > startTime and now < endTime:
            print(serial)
            print(now)
            results.append(serial)

    return jsonify(results), 200