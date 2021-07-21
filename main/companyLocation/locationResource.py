from flask import request, jsonify, Blueprint
from datetime import datetime

location_api = Blueprint('location_api', __name__)

@location_api.route('/company-location', methods=['POST', 'GET'])
def companylocationsave():
    from models import companylocation,adminlog
    from app import db
    if request.method == 'POST':
        data = request.get_json()
        now = datetime.now()

        companylocation_old = companylocation.query.filter(companylocation.location == data['location'], companylocation.status == True).first()
        if companylocation_old:
            data = {"message": f"Location already present."}
            return jsonify(data), 500
        company_location = companylocation(location = data['location'], productioncapacity = data['productioncapacity'], latitude = data['latitude'], longitude = data['longitude'], status = True)

        db.session.add(company_location)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'location', activitydone = 'save', activityid = company_location.id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Location created successfully"}
        return jsonify(data), 200

    elif request.method == 'GET':
        things = companylocation.query.all()
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id": thing.id,
                        "location": thing.location,
                        "productioncapacity": thing.productioncapacity,
                        "longitude": thing.longitude,
                        "latitude": thing.latitude,
                        "status": thing.status
                    }
                    results.append(resultsObj)
        return jsonify(results)

@location_api.route('/company-location/<id>', methods=['GET', 'PUT'])
def companylocationUpdate(id):
    from models import companylocation,adminlog
    from app import db
    companylocationById = companylocation.query.get_or_404(id)
    now = datetime.now()

    if request.method == 'GET':
        response = {
            "id": companylocationById.id,
            "location": companylocationById.location,
            "productioncapacity": companylocationById.productioncapacity,
            "longitude": companylocationById.longitude,
            "latitude": companylocationById.latitude,
            "status": companylocationById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        companylocation_old = companylocation.query.filter(companylocation.location == data['location'], companylocation.status == True).first()
        if companylocation_old:
            if int(companylocation_old.id) != int(id):
                data = {"message": f"Location already present."}
                return jsonify(data), 500
        companylocationById.location = data['location']
        companylocationById.productioncapacity = data['productioncapacity']
        companylocationById.longitude = data['longitude']
        companylocationById.latitude = data['latitude']

        db.session.add(companylocationById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'location', activitydone = 'update', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Location updated successfully"}
        return jsonify(data), 200

@location_api.route('/company-location/<id>/<logger>', methods=['DELETE'])
def companylocationDelete(id, logger):
    from models import companylocation,adminlog
    from app import db
    companylocationById = companylocation.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'DELETE':

        db.session.delete(companylocationById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'location', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Location deleted successfully"}
        return jsonify(data), 200
