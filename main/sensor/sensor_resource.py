from flask import jsonify, Blueprint, request
from datetime import datetime,date
import csv
import codecs

sensor_api = Blueprint('sensor_api', __name__)

@sensor_api.route('/sensor')
def get_sensors():
    from models import sensor
    things = sensor.query.filter(sensor.asset_sensor_allocation_id == None).all()
    results = []

    for sensorObj in things:
        serial = sensor.serialize(sensorObj)
        results.append(serial)

    return jsonify(results), 200

@sensor_api.route('/sensor-all')
def get_all_sensors():
    from models import sensor
    things = sensor.query.all()
    results = []
    for sensorObj in things:
        serial = sensor.serialize(sensorObj)
        results.append(serial)

    return jsonify(results), 200


@sensor_api.route('/sensor', methods=['POST'])
def add_sensor():
    from app import db
    from models import sensor, adminlog
    if request.method == 'POST':
        data = request.get_json()
        now = datetime.now()
        count = sensor.query.filter(sensor.name == data['name']).count()
        if count > 0:
            data = {"message": f"Sensor already exists"}
            return jsonify(data), 400

        new_sensor = sensor(status=True,
                            name=data['name'],
                            tag_name=data['tag_name'],
                            sensor_type =data['sensor_type'],
                            additional_info = data['additional_info'],
                            battery_life = data['battery_life'],
                            #in_use = data['in_use'],
                            in_use = False,
                            fw_version = data['fw_version'],
                            model = data['model'],
                            )

        db.session.add(new_sensor)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data["logger"], module = 'Sensor', activitydone = 'save', activityid = new_sensor.id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Sensor created successfully"}
        return jsonify(data), 200


@sensor_api.route('/sensor/<id>', methods=['GET', 'PUT'])
def sensorUpdate(id):
    from app import db
    from models import sensor, adminlog
    obj = sensor.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'GET':
        response = sensor.serialize(obj)
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        sensor_old = sensor.query.filter(sensor.name == data['name'], sensor.status == True).first()
        if sensor_old:
            if int(sensor_old.id) != int(id):
                data = {"message": f"sensor name already exists"}
                return jsonify(data), 500

        obj.status = data['status']
        obj.name = data['name']
        obj.tag_name = data['tag_name']
        obj.sensor_type = data['sensor_type']
        obj.additional_info = data['additional_info']
        obj.battery_life = data['battery_life']
        obj.in_use = data['in_use']
        obj.fw_version = data['fw_version']
        obj.model = data['model']
        # obj.asset_sensor_allocation_id = data['asset_sensor_allocation_id']

        db.session.add(obj)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data["logger"], module = 'Sensor', activitydone = 'update', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"sensor updated successfully"}
        return jsonify(data), 200

@sensor_api.route('/sensor/<id>/<logger>', methods=['DELETE'])
def sensorDelete(id, logger):
    from app import db
    from models import sensor, adminlog
    obj = sensor.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'DELETE':
        db.session.delete(obj)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'Sensor', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Sensor deleted successfully"}
        return jsonify(data), 200


@sensor_api.route('/asset-sensor-allocation')
def getsensorAllocation():
    from models import asset_sensor_allocation
    things = asset_sensor_allocation.query.all()
    results = []

    from models import asset
    results = [
        {
            "id": thing.id,
            "assetId": asset.query.filter(asset.id == thing.asset_id).value('id'),
            "status": thing.status
        } for thing in things]
    # for sensorObj in things:
    #     serial = sensor.serialize(sensorObj)
    #     print(serial)
    #     results.append(serial)

    return jsonify(results), 200

@sensor_api.route('/sensor-de-allocation/<id>', methods=['GET', 'PUT'])
def sensorDeAlloc(id):
    from app import db
    from models import sensor, adminlog
    obj = sensor.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'GET':
        obj.asset_sensor_allocation_id  = None

        db.session.add(obj)
        db.session.commit()
        response = sensor.serialize(obj)
        return jsonify(response),200

@sensor_api.route('/asset-sensor-allocation', methods=['POST'])
def asset_sensor_allocation():
    from app import db
    from models import asset_sensor_allocation,asset,sensor
    if request.method == 'POST':
        data = request.get_json()
        assetId = data['asset']
        
        asset = asset.query.filter(asset.id == assetId).first()
        new_asset_allocation = asset_sensor_allocation(True,asset.id)

        sensorsNonAssigned = []
        sensorsSelected = data['sensors']
        
        for sensorObj in sensorsSelected:
            if sensorObj['assetSensorAllocationId'] !=  None:
                data = {"message": f"Sensor already allocated."}
                return jsonify(data), 400
            else:
                sensorsNonAssigned.append(sensorObj)

        db.session.add(new_asset_allocation)
        db.session.commit()
        
        for sensorObj in sensorsNonAssigned:
            sensorObjOld = sensor.query.filter(sensor.id==sensorObj['id']).first()
            sensorObjOld.asset_sensor_allocation_id = new_asset_allocation.id
            sensorObjOld.in_use = True
            db.session.add(sensorObjOld)
            db.session.commit()
        data = {"message": f"name created successfully"}
        return jsonify(data), 200


@sensor_api.route('/assigned-sensors/<assetId>', methods=['GET'])
def get_asset_sensor_allocation(assetId):
    from models import asset_sensor_allocation,sensor
    # car = asset_sensor_allocation.query.get_or_404(id)
    # assetSensorAllocationObj = asset_sensor_allocation.query.get_or_404(assetId)
    assetSensorAllocationObj = asset_sensor_allocation.query.filter(asset_sensor_allocation.asset_id == assetId).all()

    sensorsSer =[]
    for allocation in assetSensorAllocationObj:
        sensors = sensor.query.filter(sensor.asset_sensor_allocation_id == allocation.id).all()
        for senObj in sensors:
            serial = sensor.serialize(senObj)
            sensorsSer.append(serial)
    
    if request.method == 'GET':
        response = {
            "sensors": sensorsSer,
            "assetId": assetId
        }
        return jsonify(response)


@sensor_api.route('/sensor-configuration-import', methods=['POST'])
def upload_sensor():
    from models import sensor
    # data = request.get_json()
    flask_file = request.files['file']
    if not flask_file:
        return 'Upload a CSV file'
    # filename = flask_file.filename

    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    csv_test = csv.reader(stream, dialect=csv.excel)
    sensor_response = []
    rowNo = 0
    for row in csv_test:
        if row:
            if rowNo > 0:
                sensorid_old = 0
                sensorExcelRowFieldValidaton(row, rowNo)
                sensorid_old = sensor.query.filter(sensor.name == row[0], sensor.status == True).count()
                if sensorid_old > 0:
                    data = {"message": f"Sensor name for row number {rowNo} already present!"}
                    return jsonify(data), 500
                response_data = {
                    'name': row[0],
                    'tag_name': row[1],
                    'sensor_type': row[2],
                    'battery_life': row[3],
                    'fw_version': row[4],
                    'model': row[5],
                    'additional_info': row[6]
                }
                sensor_response.append(response_data)
            rowNo = rowNo + 1
    return jsonify(sensor_response), 200

def sensorExcelRowFieldValidaton(row, rowNo):
    if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '' or row[6] == '' :
        data = {"message": f"Please enter all data in row number {rowNo}"}
        return jsonify(data), 500
    if type(row[0]) != str or type(row[1]) != str or type(row[2]) != str or type(row[3]) != int or type(row[4]) != int or type(row[5]) != int or type(row[6]) != str:
        data = {"message": f"Please check all data in row number {rowNo}"}
        return jsonify(data), 500

@sensor_api.route('/sensor-configuration-save-import/<logger>', methods=['POST'])
def save_sensor_import(logger):
    from models import sensor,adminlog
    from app import db
    now = datetime.now()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            for dataObj in data:
                sensor_save = sensor(status = True,name = dataObj['name'], tag_name = dataObj['tag_name'], sensor_type = dataObj['sensor_type'], additional_info = dataObj['additional_info'], battery_life = dataObj['battery_life'], in_use = False, fw_version = dataObj['fw_version'], model = dataObj['model'])

                db.session.add(sensor_save)
                db.session.commit()

                adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'asset', activitydone = 'save', activityid = sensor_save.id)
                db.session.add(adminlogObj)
                db.session.commit()

            data = {"message": f"Sensor created successfully"}
            return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}


@sensor_api.route('/sensor-first-sheet-cloumn-export', methods=['GET'])
def assetFirstSheetColumnNames():
    if request.method == 'GET':
        response_data = {
            'col0': 'Sensor Name',
            'col1': 'Tag Name',
            'col2': 'Sensor Type',
            'col3': 'Battery Life',
            'col4': 'Frame Work Version',
            'col5': 'Mode',
            'col6': 'Aditional Info'
        }
        return jsonify(response_data), 200
