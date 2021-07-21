import codecs
import csv
import json
import time
from datetime import datetime, timedelta, date

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from influxdb import InfluxDBClient

nkc = Flask(__name__)

nkc.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@123@localhost:5433/mytestdb"
nkc.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
nkc.config['SQLALCHEMY_POOL_SIZE'] = 5000

db = SQLAlchemy(nkc)

with open('config.json', 'r') as c:
    influxConnection = json.load(c)["influxDBDetails"]

influxdb = InfluxDBClient(influxConnection['influxHost'],influxConnection['influxPort'],influxConnection['indluxId'],influxConnection["influxPassword"],influxConnection['influxDBName'])
influxdb.create_database(influxConnection['influxDBName'])
influxdb.get_list_database()
influxdb.switch_database(influxConnection['influxDBName'])

# scheduler = APScheduler()

cors = CORS(nkc, resources= {
    r"/*":{
        "origins":"*",
        "Access-Control-Allow-Origin":"*"
    }
})



# nkc.register_blueprint(admins, url_prefix='/admin')
# nkc.register_blueprint(alert, url_prefix='/alert')
# nkc.register_blueprint(assets, url_prefix='/assets')
# nkc.register_blueprint(assetcategory, url_prefix='/assetcategory')
# nkc.register_blueprint(location, url_prefix='/location')
# nkc.register_blueprint(influxdata, url_prefix='/influxdata')
# nkc.register_blueprint(lossanalysiss, url_prefix='/lossanalysiss')
# nkc.register_blueprint(pm, url_prefix='/pm')

#setInterval(pm,5)
#------------------------------Admin--------------------------------------------------

class shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    starttime = db.Column(db.DateTime())
    endtime = db.Column(db.DateTime())
    status = db.Column(db.Boolean)

    def __init__(self, name, starttime, endtime, status):
        self.name = name
        self.starttime = starttime
        self.endtime = endtime
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'starttime': self.starttime,
            'endtime': self.endtime,
            'status': self.status
        }

#------------------------------Location-----------------------------------------------

class companylocation(db.Model):
    __tablename__ = 'companylocation'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String())
    productioncapacity = db.Column(db.Integer)
    longitude = db.Column(db.String())
    latitude = db.Column(db.String())
    status = db.Column(db.Boolean)

    def __init__(self, location, productioncapacity, longitude, latitude, status):
        self.location = location
        self.productioncapacity = productioncapacity
        self.longitude = longitude
        self.latitude = latitude
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'location': self.location,
            'productioncapacity': self.productioncapacity,
            'latitude': self.latitude,
            'longitude':self.longitude,
            'status': self.status
        }

@nkc.route('/company-location', methods=['POST', 'GET'])
def companylocationsave():
    if request.method == 'POST':
        data = request.get_json()
        company_location = companylocation(location = data['location'], productioncapacity = data['productioncapacity'], latitude = data['latitude'], longitude = data['longitude'], status = True)

        db.session.add(company_location)
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
                        "id" : thing.id,
                        "location" : thing.location,
                        "productioncapacity" : thing.productioncapacity,
                        "longitude":thing.longitude,
                        "latitude":thing.latitude,
                        "status" : thing.status
                    }
                    results.append(resultsObj)
        return  jsonify(results)

@nkc.route('/company-location/<id>', methods=['GET', 'PUT', 'DELETE'])
def companylocationUpdate(id):
    companylocationById = companylocation.query.get_or_404(id)

    if request.method == 'GET':
        response =   {
                "id" : companylocationById.id,
                "location" : companylocationById.location,
                "productioncapacity" : companylocationById.productioncapacity,
                "longitude": companylocationById.longitude,
                "latitude" : companylocationById.latitude,
                "status" : companylocationById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        companylocationById.location = data['location']
        companylocationById.productioncapacity = data['productioncapacity']
        companylocationById.longitude = data['longitude']
        companylocationById.latitude = data['latitude']
        
        db.session.add(companylocationById)
        db.session.commit()
        data = {"message": f"Location updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
        
        db.session.delete(companylocationById)
        db.session.commit()
    
        data = {"message": f"Location deleted successfully"}
        return jsonify(data), 200

#------------------------------Asset Category-----------------------------------------

class assetcategory(db.Model):
    __tablename__ = 'assetcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    keyvalue = db.Column(db.Integer)
    status = db.Column(db.Boolean)

    def __init__(self, name, keyvalue, status):
        self.name = name
        self.keyvalue = keyvalue
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'keyvalue': self.keyvalue,
            'status': self.status
        }

@nkc.route('/asset-category', methods=['POST', 'GET'])
def assetcategorysave():
    if request.method == 'POST':
        data = request.get_json()
        asset_category = assetcategory(name = data['name'], keyvalue = data['keyvalue'], status = True)

        db.session.add(asset_category)
        db.session.commit()

        data = {"message": f"Asset category created successfully"}
        return jsonify(data), 200

    elif request.method == 'GET':
        things = assetcategory.query.all()
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id" : thing.id,
                        "name" : thing.name,
                        "keyvalue" : thing.keyvalue,                        
                        "status" : thing.status
                    }
                    results.append(resultsObj)
        return  jsonify(results)

@nkc.route('/asset-category/<id>', methods=['GET', 'PUT', 'DELETE'])
def assetcategoryUpdate(id):
    assetcategoryById = assetcategory.query.get_or_404(id)

    if request.method == 'GET':
        response =   {
                "id" : assetcategoryById.id,
                "name" : assetcategoryById.name,
                "keyvalue" : assetcategoryById.keyvalue,
                "status" : assetcategoryById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        assetcategoryById.name = data['name']
        assetcategoryById.keyvalue = data['keyvalue']
        
        db.session.add(assetcategoryById)
        db.session.commit()
        data = {"message": f"Asset category updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
    
        db.session.delete(assetcategoryById)
        db.session.commit()
    
        data = {"message": f"Asset category deleted successfully"}
        return jsonify(data), 200

#------------------------------Asset--------------------------------------------------

class asset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable = False)
    companylocation = db.Column(db.Integer, db.ForeignKey('companylocation.id'), nullable = False)
    status = db.Column(db.Boolean)

    def __init__(self, name, description, assetcategory, companylocation, status):
        self.name = name
        self.description = description
        self.assetcategory = assetcategory
        self.companylocation = companylocation
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'assetcategory': self.assetcategory,
            'companylocation': self.companylocation,
            'status': self.status
        }

@nkc.route('/asset', methods=['POST', 'GET'])
def assetsave():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            count = asset.query.filter(asset.name == data['name'], asset.status == True).count()
            if count > 0:
                data = {"message": f"Asset name already exists"}
                return jsonify(data), 400
            else:
                assetcategory_id = assetcategory.query.filter(assetcategory.name == data['assetcategory']).value('id')
                companylocation_id = companylocation.query.filter(companylocation.location == data['companylocation']).value('id')
                asset_data = asset(name = data['name'], description = data['description'], assetcategory = assetcategory_id, companylocation = companylocation_id, status = True)

                db.session.add(asset_data)
                db.session.commit()
                data = {"message": f"Asset created successfully"}
                return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = asset.query.all()
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id" : thing.id,
                        "name" : thing.name,
                        "description" : thing.description,
                        "assetcategory" : assetcategory.query.filter(assetcategory.id == thing.assetcategory).value('name'),
                        "companylocation" : companylocation.query.filter(companylocation.id == thing.companylocation).value('location'),
                        "status" : thing.status
                    }
                    results.append(resultsObj)
        return  jsonify(results)

@nkc.route('/asset/<id>', methods=['GET', 'PUT', 'DELETE'])
def assetUpdate(id):
    assetById = asset.query.get_or_404(id)

    if request.method == 'GET':
        response =   {
                "id" : assetById.id,
                "name" : assetById.name,
                "description" : assetById.description,
                "assetcategory" : assetcategory.query.filter(assetcategory.id == assetById.assetcategory).value('name'),
                "companylocation" : companylocation.query.filter(companylocation.id == assetById.companylocation).value('location'),
                "status" : assetById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        assetById.name = data['name']
        assetById.description = data['description']
        assetById.assetcategory = assetcategory.query.filter(assetcategory.name == data['assetcategory']).value('id')
        assetById.companylocation = companylocation.query.filter(companylocation.location == data['companylocation']).value('id')
        
        db.session.add(assetById)
        db.session.commit()
        data = {"message": f"Asset updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':

        db.session.delete(assetById)
        db.session.commit()
    
        data = {"message": f"Asset deleted successfully"}
        return jsonify(data), 200

@nkc.route('/asset-by-assetcategory-location', methods=['GET'])
def assetDetails():
    if request.method == 'GET':
        data = request.get_json()
        assetcategory_id = assetcategory.query.filter(assetcategory.name == data['assetcategory'], assetcategory.status == True).value('id')
        companylocation_id = companylocation.query.filter(companylocation.location == data['companylocation'], companylocation.status == True).value('id')
        asset_data = asset.query.filter(asset.companylocation == companylocation_id, asset.assetcategory == assetcategory_id)
        if asset_data is None :
            response_list=[]
            for assetObj in asset_data:
                    response =   {
                        "id" : assetObj.id,
                        "name" : assetObj.name,
                        "description" : assetObj.description,
                        "assetcategory" : data['assetcategory'],
                        "companylocation" : data['companylocation'],
                        "status" : assetObj.status
                    }
                    response_list.append(response)
            return jsonify(response_list)
        else:
            data = {"message": f"There is no data"}
            return jsonify(data), 500

#------------------------------Alert rule--------------------------------------------------

class alarmconfiguration(db.Model):
    __tablename__ = 'alarmconfiguration'

    id = db.Column(db.Integer, primary_key=True)
    companylocation = db.Column(db.Integer, db.ForeignKey('companylocation.id'), nullable = False)
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable = False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable = False)
    alertsubcategory = db.Column(db.String())
    alertlimittype = db.Column(db.String())
    configvalue = db.Column(db.Integer)
    alarm = db.Column(db.String())
    severity = db.Column(db.String())
    createdon = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    
    def __init__(self, companylocation, assetcategory, asset, alertsubcategory, alertlimittype, configvalue, alarm, severity,createdon,status):
        self.companylocation = companylocation
        self.assetcategory = assetcategory
        self.asset = asset
        self.alertsubcategory = alertsubcategory
        self.alertlimittype = alertlimittype
        self.configvalue = configvalue
        self.alarm = alarm
        self.severity = severity
        self.createdon = createdon
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'companylocation': self.companylocation,
            'assetcategory': self.assetcategory,
            'asset': self.asset,
            'alertsubcategory': self.alertsubcategory,
            'alertlimittype': self.alertlimittype,
            'configvalue': self.configvalue,
            'alarm': self.alarm,
            'severity': self.severity,
            'createdon': self.createdon,
            'status': self.status
        }

class alert(db.Model):
    __tablename__ = 'alert'

    id = db.Column(db.Integer, primary_key=True)
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable = False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable = False)
    alertsubcategory = db.Column(db.String())
    alertlimittype = db.Column(db.String())
    trackvalue = db.Column(db.Float)
    alarm = db.Column(db.String())
    alertstatus = db.Column(db.Boolean)
    triggeredon = db.Column(db.DateTime)
    

    def __init__(self, assetcategory, asset, alertsubcategory, alertlimittype, trackvalue, alarm, alertstatus,triggeredon):
        self.assetcategory = assetcategory
        self.asset = asset
        self.alertsubcategory = alertsubcategory
        self.alertlimittype = alertlimittype
        self.trackvalue = trackvalue
        self.alarm = alarm
        self.alertstatus = alertstatus
        self.triggeredon = triggeredon

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'assetcategory': self.assetcategory,
            'asset': self.asset,
            'alertsubcategory': self.alertsubcategory,
            'alertlimittype': self.alertlimittype,
            'trackvalue': self.trackvalue,
            'alarm': self.alarm,
            'alertstatus': self.alertstatus,
            'triggeredon': self.triggeredon
        }

def createAlert():
    getTabes = "show measurements"
    result = influxdb.query(getTabes)
    points = list(result.get_points())
    for table in points:
        dataQuery = 'SELECT * FROM %s ORDER BY time DESC LIMIT 1'
        result = influxdb.query((dataQuery) % (table['name'],))
        points = list(result.get_points())
        assetLiveData = points[0]
        assetId = assetLiveData["asset_id"]
        alarmRules = alarmconfiguration.query.filter(alarmconfiguration.asset == assetId, alarmconfiguration.status == True).value('all')
    
        alertValidation(assetLiveData, alarmRules)
    return '', 204

def alertValidation(assetLiveData, alarmRules):
    for alarm in alarmRules:
            if alarm.alertsubcategory == "TL_Comm_Status":
                if assetLiveData["tl_comm_status"] == True:
                    currentValue = 1
                else:
                    currentValue = 0
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "POWER_LINE_1":
                currentValue = float(assetLiveData["power_line1_value"])/1000
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "POWER_LINE_2":
                currentValue = float(assetLiveData["power_line2_value"])/1000
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "POWER_LINE_3":                
                currentValue = float(assetLiveData["power_line3_value"])/1000
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "MOTOR_VIBRATION_X_AXIS":
                currentValue = float(assetLiveData["motor_vibration_x_axis"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "MOTOR_VIBRATION_Z_AXIS":
                currentValue = float(assetLiveData["motor_vibration_z_axis"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "MAST_VIBRATION_X_AXIS":
                currentValue = float(assetLiveData["mast_vibration_x_axis"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "MAST_VIBRATION_Z_AXIS":
                currentValue = float(assetLiveData["mast_vibration_z_axis"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "VOLTAGE_LINE_1":
                currentValue = float(assetLiveData["voltage_line1_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "VOLTAGE_LINE_2":
                currentValue = float(assetLiveData["voltage_line2_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "VOLTAGE_LINE_3":
                currentValue = float(assetLiveData["voltage_line3_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "CURRENT_LINE_1":
                currentValue = float(assetLiveData["current_line1_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "CURRENT_LINE_2":
                currentValue = float(assetLiveData["current_line2_value"])
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "CURRENT_LINE_3":
                currentValue = float(assetLiveData["current_line3_value"])
                oldAlertVerification(assetLiveData, alarm, currentValue)
            
            if alarm.alertsubcategory == "FREQUENCY_LINE_1":
                currentValue = float(assetLiveData["frequency_line1_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "FREQUENCY_LINE_2":
                currentValue = float(assetLiveData["frequency_line2_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "FREQUENCY_LINE_3":
                currentValue = float(assetLiveData["frequency_line3_value"])/10
                oldAlertVerification(assetLiveData, alarm, currentValue)
            if alarm.alertsubcategory == "TEMPERATURE":
                currentValue = float(assetLiveData["temperature_value"])/100
                oldAlertVerification(assetLiveData, alarm, currentValue)

def oldAlertVerification(assetLiveData, alarm, currentValue):
    now = datetime.now()
    assetId = assetLiveData["asset_id"]
    alert_sub_category = alarm.alertsubcategory
    #currentHr = now.strftime("%d/%m/%Y %H:%M:%S")
    #latestAretHr = str(int(alertLatest[7].strftime("%H")) + 2)
    alertlist = alert.query.filter(alert.asset == assetId, alert.alertsubcategory == alert_sub_category)
    for alertObj in alertlist:
        alertLatest = alertObj
    if alertLatest:        
        latestAretHr = alertLatest.triggeredon+ timedelta(hours=2)
        if now > latestAretHr:
            calculateAlert(assetLiveData, alarm, currentValue)
        else:
            print("***************Alerm already exit***************")

def calculateAlert(assetLiveData, alarm, currentValue):
    now = datetime.now()
    if alarm.alertlimittype == "Greater_Than":
        if currentValue > alarm.trackvalue:
            alert = alert(assetcategory = alarm[10], asset = alarm[9], alertsubcategory = alarm[4], alertlimittype = alarm[3], trackvalue = currentValue, alarm = alarm[1], alertstatus = True, triggeredon = now)
            db.session.add(alert)
            db.session.commit()
    elif alarm.alertlimittype == "Less_Than":
        if currentValue < alarm.trackvalue:
            alert = alert(assetcategory = alarm[10], asset = alarm[9], alertsubcategory = alarm[4], alertlimittype = alarm[3], trackvalue = currentValue, alarm = alarm[1], alertstatus = True, triggeredon = now)
            db.session.add(alert)
            db.session.commit()
    elif alarm.alertlimittype == "Equal_To":
        if currentValue == alarm.trackvalue:
            alert = alert(assetcategory = alarm[10], asset = alarm[9], alertsubcategory = alarm[4], alertlimittype = alarm[3], trackValue = currentValue, alarm = alarm[1], alertstatus = True, triggeredon = now)
            db.session.add(alert)
            db.session.commit()

@nkc.route('/alert-current-day', methods=['GET'])
def alertForCurrentDay():
    if request.method == 'GET':
        now = datetime.now()
        currentDay = now.strftime("%d")
        currentMonth = now.strftime("%m")
        currentYear = now.strftime("%Y")
        alertList = alert.query.all()
        alert_response = []
        for alertObj in alertList:
            alertDay = (alertObj.triggeredon).strftime("%d")
            alertMonth = (alertObj.triggeredon).strftime("%m")
            alertYear = (alertObj.triggeredon).strftime("%Y")
            if alertDay == currentDay and alertMonth == currentMonth and alertYear == currentYear:
                data = {
                    "id":alertObj.id,
                    "assetcategory":assetcategory.query.filter(assetcategory.id == alertObj.assetcategory).value("name"),
                    "asset": asset.query.filter(asset.id == alertObj.asset).value("name"),
                    "alertsubcategory":alertObj.alertsubcategory,
                    "alertlimittype":alertObj.alertlimittype,
                    "trackvalue":alertObj.trackvalue,
                    "alarm":alertObj.alarm,
                    "alertstatus":alertObj.alertstatus,
                    "triggeredon":alertObj.triggeredon
                }
                alert_response.append(data)
        if len(alert_response) < 1:
            data = {"message": f"There is no Alert."}
            return jsonify(data), 500
        alert_response.reverse()
        return jsonify(alert_response), 200

@nkc.route('/alert-assetcategory-asset', methods=['POST'])
def alertbycategoryAndAssetForCurrentMonth():
    if request.method == 'POST':
        data = request.get_json()
        now = datetime.now()
        currentMonth = now.strftime("%m")
        currentYear = now.strftime("%Y")
        alert_response = []
        assetCategoryId = assetcategory.query.filter(assetcategory.name == data['assetcategory'], assetcategory.status == True).value("id")
        assetId = asset.query.filter(asset.name == data['asset'],asset.status ==True).value("id")
        alerts = alert.query.filter(alert.assetcategory == assetCategoryId, alert.asset == assetId, alert.alertstatus == True)
        for alertObj in alerts:            
            alertMonth = (alertObj.triggeredon).strftime("%m")
            alertYear = (alertObj.triggeredon).strftime("%Y")
            if alertMonth == currentMonth and alertYear == currentYear:
                response = {
                    "id":alertObj.id,
                    "assetcategory":assetcategory.query.filter(assetcategory.id == alertObj.assetcategory).value("name"),
                    "asset": asset.query.filter(asset.id == alertObj.asset).value("name"),
                    "alertsubcategory":alertObj.alertsubcategory,
                    "alertlimittype":alertObj.alertlimittype,
                    "trackvalue":alertObj.trackvalue,
                    "alarm":alertObj.alarm,
                    "alertstatus":alertObj.alertstatus,
                    "triggeredon":alertObj.triggeredon
                }
                alert_response.append(response)
        if len(alert_response) < 1:
            data_error = {"message": f"There is no Alert."}
            return jsonify(data_error), 500
        alert_response.reverse()
        return jsonify(alert_response), 200

@nkc.route('/alarm-configuration-import', methods = ['POST'])
def upload_alertrule():
    #data = request.get_json()
    flask_file = request.files['file']
    if not flask_file:
        return 'Upload a CSV file'
    #filename = flask_file.filename
    
    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    csv_test = csv.reader(stream, dialect=csv.excel)
    alarm_response = []
    rowNo = 0
    for row in csv_test:
        if row:
            if rowNo > 0:
                excelRowFieldValidaton(row, rowNo)
                response_data = {
                        #'assetcategory': assetcategory.query.filter(assetcategory.name == data['assetcategory'], assetcategory.status == True).value("id"),
                        #'asset': asset.query.filter(asset.name == data['asset'], asset.status == True).value("id"),
                        'alertsubcategory': row[0],
                        'alertlimittype': row[1],
                        'configvalue': row[2],
                        'alarm': row[3],
                        'severity': row[4],
                        'createdon': datetime.now(),
                        'status': True
                }
                alarm_response.append(response_data)
            rowNo = rowNo + 1
    return jsonify(alarm_response), 200

def excelRowFieldValidaton(row, rowNo):
    if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '':        
        data = {"message": f"Please enter all data in row number {rowNo}"}
        return jsonify(data), 500
    if type(row[0]) != str or type(row[1]) != str or type(row[2]) != int or type(row[3]) != str or type(row[4]) != str:
        data = {"message": f"Please check all data in row number {rowNo}"}
        return jsonify(data), 500

@nkc.route('/alarm-configuration-save-import', methods = ['POST','GET'])
def save_alertrule():
    if request.method == 'POST':
        if request.is_json:
            now = datetime.now()
            data = request.get_json()
            for dataObj in data:
                companylocationId = companylocation.query.filter(companylocation.location == dataObj['companylocation'], companylocation.status == True).value("id")
                assetcategoryId = assetcategory.query.filter(assetcategory.name == dataObj['assetcategory'], assetcategory.status == True).value("id")
                assetId = asset.query.filter(asset.name == dataObj['asset'], asset.assetcategory == assetcategoryId, asset.status ==True).value("id")

                alarmconfiguration_save = alarmconfiguration(companylocation = companylocationId,assetcategory = assetcategoryId,asset = assetId,alertsubcategory = dataObj['alertsubcategory'],alertlimittype = dataObj['alertlimittype'],configvalue = dataObj['configvalue'],alarm = dataObj['alarm'],severity = dataObj['severity'],createdon = now,status = True)
                db.session.add(alarmconfiguration_save)
                db.session.commit()
                data = {"message": f"Alert rule created successfully"}
                return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

#------------------------------Loss Analysis--------------------------------------------------

class losscategory(db.Model):
    __tablename__ = 'losscategory'

    id = db.Column(db.Integer, primary_key=True)
    losscategory = db.Column(db.String())
    description = db.Column(db.String())
    status = db.Column(db.Boolean)

    def __init__(self, losscategory, description, status):
        self.losscategory = losscategory
        self.description = description
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'losscategory': self.losscategory,
            'description': self.description,
            'status': self.status
        }

class losssubcategory(db.Model):
    __tablename__ = 'losssubcategory'

    id = db.Column(db.Integer, primary_key=True)
    losssubcategory = db.Column(db.String())
    description = db.Column(db.String())
    status = db.Column(db.Boolean)
    losscategory = db.Column(db.Integer, db.ForeignKey('losscategory.id'), nullable = False)

    def __init__(self, losssubcategory, description, status, losscategory):
        self.losssubcategory = losssubcategory
        self.description = description
        self.status = status
        self.losscategory = losscategory

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'losssubcategory': self.losssubcategory,
            'description': self.description,
            'status': self.status,
            'losscategory': self.losscategory
        }

class lossanalysis(db.Model):
    __tablename__ = 'lossanalysis'

    id = db.Column(db.Integer, primary_key=True)
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable = False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable = False)
    losscategory = db.Column(db.Integer, db.ForeignKey('losscategory.id'), nullable = False)
    losssubcategory = db.Column(db.Integer, db.ForeignKey('losssubcategory.id'), nullable = False)
    shift = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable = False)
    fromtime = db.Column(db.TIME())
    totime = db.Column(db.TIME())
    losstime = db.Column(db.Integer)
    createdon = db.Column(db.DateTime)
    status = db.Column(db.Boolean)

    def __init__(self, assetcategory, asset, losscategory, losssubcategory, shift, fromtime, totime, losstime, createdon, status):
        self.assetcategory = assetcategory
        self.asset = asset
        self.losscategory = losscategory
        self.losssubcategory = losssubcategory
        self.shift = shift
        self.fromtime = fromtime
        self.totime = totime
        self.losstime = losstime
        self.createdon = createdon
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'assetcategory': self.assetcategory,
            'asset': self.asset,
            'losscategory': self.losscategory,
            'losssubcategory': self.losssubcategory,
            'shift': self.shift,
            'fromtime': self.fromtime,
            'totime': self.totime,
            'losstime': self.losstime,
            'createdon': self.createdon,
            'status': self.status            
        }

@nkc.route('/loss-category', methods=['POST', 'GET'])
def losscategorysave():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            losscategory_data = losscategory(losscategory = data['losscategory'], description = data['description'], status = True)

            db.session.add(losscategory_data)
            db.session.commit()

            data = {"message": f"Loss category created successfully"}
            return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = losscategory.query.all()
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id" : thing.id,
                        "losscategory" : thing.losscategory,
                        "description" : thing.description,
                        "status" : thing.status
                    }
                    results.append(resultsObj)
        return  jsonify(results)

@nkc.route('/loss-category/<id>', methods=['GET', 'PUT', 'DELETE'])
def losscategoryUpdate(id):
    losscategoryById = losscategory.query.get_or_404(id)

    if request.method == 'GET':
        response =   {
                "id" : losscategoryById.id,
                "losscategory" : losscategoryById.losscategory,
                "description" : losscategoryById.description,
                "status" : losscategoryById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        losscategoryById.losscategory = data['losscategory']
        losscategoryById.description = data['description']
        
        db.session.add(losscategoryById)
        db.session.commit()
        data = {"message": f"Loss category updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
    
        db.session.delete(losscategoryById)
        db.session.commit()
    
        data = {"message": f"Loss category deleted successfully"}
        return jsonify(data), 200


@nkc.route('/loss-sub-category', methods=['POST', 'GET'])
def losssubcategorysave():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            count = losssubcategory.query.filter(losssubcategory.losssubcategory == data['losssubcategory'], losssubcategory.status == True).count()
            if count > 0:
                data = {"message": f"This loss subcategory name already exists"}
                return jsonify(data), 400
            else:
                losscategory_id = losscategory.query.filter(losscategory.losscategory == data['losscategory'], losscategory.status == True).value('id')
                losssubcategory_data = losssubcategory(losssubcategory = data['losssubcategory'], description = data['description'], status = True, losscategory = losscategory_id)

                db.session.add(losssubcategory_data)
                db.session.commit()
                data = {"message": f"Loss subcategory created successfully"}
                return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = losssubcategory.query.all()
        #losscategoryById = losscategory.query.get_or_404(id)
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id" : thing.id,
                        "losssubcategory" : thing.losssubcategory,
                        "description" : thing.description,
                        "status" : True,
                        "losscategory":losscategory.query.filter(losscategory.id == thing.losscategory, losscategory.status == True).value('losscategory')
                    }
                    results.append(resultsObj)
        return  jsonify(results)

@nkc.route('/loss-sub-category/<id>', methods=['GET', 'PUT', 'DELETE'])
def losssubcategoryUpdate(id):
    losssubcategoryById = losssubcategory.query.get_or_404(id)

    if request.method == 'GET':
        response =   {
                "id" : losssubcategoryById.id,
                "losssubcategory" : losssubcategoryById.losssubcategory,
                "description" : losssubcategoryById.description,
                "status" : losssubcategoryById.status,
                "losscategory": losscategory.query.filter(losscategory.id == losssubcategoryById.losscategory, losscategory.status == True).value('losscategory')
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        losssubcategoryById.losssubcategory = data['losssubcategory']
        losssubcategoryById.description = data['description']
        losssubcategoryById.losscategory = losscategory.query.filter(losscategory.losscategory == data['losscategory'], losscategory.status == True).value('id')
        
        db.session.add(losssubcategoryById)
        db.session.commit()
        data = {"message": f"Loss subcategory updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
    
        db.session.delete(losssubcategoryById)
        db.session.commit()
    
        data = {"message": f"Loss subcategory deleted successfully"}
        return jsonify(data), 200

@nkc.route('/loss-sub-category-by-losscategory/<losscategoryid>', methods=['GET'])
def losssubcategoryBylosssCategory(losscategoryid):
    if request.method == 'GET':
        losscategoryById = losscategory.query.get_or_404(losscategoryid)
        losssubcategory_list = losssubcategory.query.filter(losssubcategory.losscategory == losscategoryid, losssubcategory.status == True)
        response =[]
        for losssubcategoryObj in losssubcategory_list:
            data = {
                "id": losssubcategoryObj.id,
                "losssubcategory": losssubcategoryObj.losssubcategory,
                "description": losssubcategoryObj.description,
                "status": losssubcategoryObj.status,
                "losscategory": losscategory.query.filter(losscategory.id == losscategoryid, losscategory.status == True).value('losscategory')
            }
            response.append(data)
        return jsonify(response), 200

@nkc.route('/loss-analysis-current-day', methods=['GET'])
def getLossAnalysisCurrentDay():
    if request.method == 'GET':
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")
        curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        lossanalysis_data = lossanalysis.query.filter(lossanalysis.createdon == curerntDate, lossanalysis.status == True).all()
        if len(lossanalysis_data) > 0:
            lossanalysis_data.reverse()
            response_list = []
            for lossanalysisObj in lossanalysis_data:
                response_data = {
                    'id' : lossanalysisObj.id,
                    'assetcategory': assetcategory.query.filter(assetcategory.id == lossanalysisObj.assetcategory, assetcategory.status == True).value('name'),
                    'asset': asset.query.filter(asset.id == lossanalysisObj.asset, asset.assetcategory == lossanalysisObj.assetcategory, asset.status == True).value('name'),
                    'losscategory': losscategory.query.filter(losscategory.id == lossanalysisObj.losscategory, losscategory.status == True).value('losscategory'),
                    'losssubcategory': losssubcategory.query.filter(losssubcategory.id == lossanalysisObj.losssubcategory, losssubcategory.losscategory == lossanalysisObj.losscategory, losssubcategory.status == True).value('losssubcategory'),
                    'shift': shift.query.filter(shift.id == lossanalysisObj.shift,shift.status == True ).value('name'),
                    'fromtime': lossanalysisObj.fromtime.strftime("%H:%M:%S"),
                    'totime': lossanalysisObj.totime.strftime("%H:%M:%S"),
                    'losstime': lossanalysisObj.losstime,
                    'createdon': lossanalysisObj.createdon.strftime("%d-%m-%Y %H:%M:%S"),
                    'status': lossanalysisObj.status
                }
                response_list.append(response_data)
            return jsonify(response_list)
        else:
            data = {"message": f"There is no loss for current day."}
            return jsonify(data), 500

@nkc.route('/loss-analysis-by-shift-date-for-total-time', methods=['POST'])
def getLossAnalysisShiftDateTotalTime():
    if request.method == 'POST':
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")
        curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        data = request.get_json()
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        totalRunTime = 0
        totalLossTime = 0
        totalTimeStr = str(datetime.combine(date.min, shiftObj.endtime) - datetime.combine(date.min, shiftObj.starttime))
        t=totalTimeStr.split(':')
        totalTime= int(t[0])*60+int(t[1])*1 +int(t[2])/60
        lossanalysis_data = lossanalysis.query.filter(lossanalysis.createdon == curerntDate, lossanalysis.shift == shiftObj.id, lossanalysis.status == True).all()
        for lossanalysisObj in lossanalysis_data:
            totalLossTime = totalLossTime + lossanalysisObj.losstime
        totalRunTime = totalTime - totalLossTime
        response = {
            "totaltime": totalTime,
            "totalruntime": totalRunTime,
            "totallosstime": totalLossTime
        }
        return jsonify(response), 200

@nkc.route('/loss-analysis-by-shift-date-for-category-loss-time', methods=['POST'])
def getLossAnalysisCurrentMonthForCategoryLossTime():
    if request.method == 'POST':
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")
        curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        data = request.get_json()
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        losscategory_list = losscategory.query.all()
        lossanalysis_list = lossanalysis.query.filter(lossanalysis.createdon == curerntDate, lossanalysis.shift == shiftObj.id, lossanalysis.status == True).all()
        response_data = []
        for losscategory_Obj in losscategory_list:
            totalCategoryLossTime = 0
            losscategoryObj = None
            for lossanalysisObj in lossanalysis_list:
                if lossanalysisObj.losscategory == losscategory_Obj.id:
                    totalCategoryLossTime = totalCategoryLossTime + lossanalysisObj.losstime
                    losscategoryObj = losscategory_Obj
            if losscategoryObj:
                dataObj = {
                    "losscategory":losscategoryObj.losscategory,
                    "totalCategoryLossTime":totalCategoryLossTime
                }
                response_data.append(dataObj)
        return jsonify(response_data), 200

@nkc.route('/loss-analysis-by-shift-date-for-subcategory-loss-time', methods=['POST'])
def getLossAnalysisByShiftByDateBySubcategory():
    if request.method == 'POST':
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")
        curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        data = request.get_json()
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        losscategoryObj = losscategory.query.filter(losscategory.losscategory == data['losscategory'], losscategory.status == True).first()
        losssubcategory_list = losssubcategory.query.filter(losssubcategory.losscategory == losscategoryObj.id, losssubcategory.status == True).all()
        lossanalysis_list = lossanalysis.query.filter(lossanalysis.createdon == curerntDate, lossanalysis.shift == shiftObj.id, lossanalysis.status == True).all()
        response = []
        for losssubcategory_Obj in losssubcategory_list:
            totalSubCategoryTime = 0
            losssubcategoryObj = None
            for lossanalysisObj in lossanalysis_list:
                if lossanalysisObj.losssubcategory == losssubcategory_Obj.id:
                    totalSubCategoryTime = totalSubCategoryTime + lossanalysisObj.losstime
                    losssubcategoryObj = losssubcategory_Obj
            if losssubcategoryObj:
                data = {
                    "losssubcategory":losssubcategoryObj.losssubcategory,
                    "totalsubcategorylosstime":totalSubCategoryTime
                }
                response.append(data)
        return jsonify(response), 200

@nkc.route('/loss-analysis', methods=['POST'])
def saveLossAnalysis():
    if request.method == 'POST':
        now = datetime.now()
        curerntDate = now.strftime("%d/%m/%Y")
        data = request.get_json()
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status ==True).first()
        assetcategoryObj = assetcategory.query.filter(assetcategory.name == data['assetcategory'], assetcategory.status == True).first()
        assetObj = asset.query.filter(asset.name == data['asset'], asset.status == True).first()
        losscategoryObj = losscategory.query.filter(losscategory.losscategory == data['losscategory'], losscategory.status == True).first()
        losssubcategoryObj = losssubcategory.query.filter(losssubcategory.losssubcategory == data['losssubcategory'], losssubcategory.status == True).first()
        lossanalysis_list = lossanalysis.query.filter(lossanalysis.assetcategory == assetcategoryObj.id, lossanalysis.asset == assetObj.id, lossanalysis.shift == shiftObj.id, lossanalysis.status == True).all()
        startTime = 0
        endTime = 0
        for lossanalysis_obj in lossanalysis_list:
            losscreatedon = (lossanalysis_obj.createdon).strftime("%d/%m/%Y")
            if (losscreatedon == curerntDate) == True:
                if startTime == 0 or startTime > lossanalysis_obj.fromtime:
                    startTime = lossanalysis_obj.fromtime
                if endTime == 0 or endTime < lossanalysis_obj.totime:
                    endTime = lossanalysis_obj.totime
        if (data['fromtime'] > data['totime']) == True:
            data = {"message": f"From time is greater than to time."}
            return jsonify(data), 500
        elif (data['fromtime'] >= shiftObj.starttime.strftime("%H:%M:%S")) == True and (data['totime'] <= shiftObj.endtime.strftime("%H:%M:%S")) == True:
            if startTime != 0 and endTime != 0:
                if (data['fromtime'] < endTime.strftime("%H:%M:%S")) == True:
                    data = {"message": f"Loss already present for this time range."}
                    return jsonify(data), 500
                else:
                    losstimeStr = str(datetime.strptime(data['totime'], '%H:%M:%S') - datetime.strptime(data['fromtime'], '%H:%M:%S'))
                    t=losstimeStr.split(':')
                    losstime = int(t[0])*60+int(t[1])*1 +int(t[2])/60
                    lossanalysisObj = lossanalysis(assetcategory = assetcategoryObj.id, asset = assetObj.id, losscategory = losscategoryObj.id, losssubcategory = losssubcategoryObj.id, shift = shiftObj.id, fromtime = data['fromtime'], totime = data['totime'], losstime = losstime, createdon = now, status =  True)
                    db.session.add(lossanalysisObj)
                    db.session.commit()
            else:
                losstimeStr = str(datetime.strptime(data['totime'], '%H:%M:%S') - datetime.strptime(data['fromtime'], '%H:%M:%S'))
                t=losstimeStr.split(':')
                losstime= int(t[0])*60+int(t[1])*1 +int(t[2])/60
                lossanalysisObj = lossanalysis(assetcategory = assetcategoryObj.id, asset = assetObj.id, losscategory = losscategoryObj.id, losssubcategory = losssubcategoryObj.id, shift = shiftObj.id, fromtime = data['fromtime'], totime = data['totime'], losstime = losstime, createdon = now, status =  True)
                db.session.add(lossanalysisObj)
                db.session.commit()
        else:
            data = {"message": f"Please enter time between current shift time range."}
            return jsonify(data), 500
        data = {"message": f"Loss saved successfully."}
        return jsonify(data), 200

#------------------------------Preventive Maintenance--------------------------------------------------

class durationtype(db.Model):
    __tablename__ = 'durationtype'

    id = db.Column(db.Integer, primary_key=True)
    durationtype = db.Column(db.String())
    lowlimit = db.Column(db.Integer)
    highlimit = db.Column(db.Integer)
    status = db.Column(db.Boolean)

    def __init__(self, durationtype, lowlimit, highlimit, status):
        self.durationtype = durationtype
        self.lowlimit = lowlimit
        self.highlimit = highlimit
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'durationtype': self.durationtype,
            'lowlimit': self.lowlimit,
            'highlimit': self.highlimit,
            'status': self.status
        }

class checklistmaster(db.Model):
    __tablename__ = 'checklistmaster'

    id = db.Column(db.Integer, primary_key=True)
    checkpart = db.Column(db.String())
    checkpoint = db.Column(db.String())
    description = db.Column(db.String())
    standardvalue = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    createdon = db.Column(db.DateTime)
    updatedon = db.Column(db.DateTime)

    def __init__(self, checkpart, checkpoint, description, standardvalue, status, createdon, updatedon):
        self.checkpart = checkpart
        self.checkpoint = checkpoint
        self.description = description
        self.standardvalue = standardvalue
        self.status = status
        self.createdon = createdon
        self.updatedon = updatedon

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'checkpart': self.checkpart,
            'checkpoint': self.checkpoint,
            'description': self.description,
            'standardvalue': self.standardvalue,
            'status': self.status,
            'createdon': self.createdon,
            'updatedon': self.updatedon
        }

class checklist(db.Model):
    __tablename__ = 'checklist'

    id = db.Column(db.Integer, primary_key=True)
    checkpart = db.Column(db.String())
    checkpoint = db.Column(db.String())
    checkpointstatus = db.Column(db.Boolean)
    description = db.Column(db.String())
    standardvalue = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    remark = db.Column(db.String())
    submittedon = db.Column(db.DateTime)
    submittedby = db.Column(db.String())

    def __init__(self, checkpart, checkpoint, checkpointstatus, description, standardvalue, status, remark, submittedon, submittedby):
        self.checkpart = checkpart
        self.checkpoint = checkpoint
        self.checkpointstatus = checkpointstatus
        self.description = description
        self.standardvalue = standardvalue
        self.status = status
        self.remark = remark
        self.submittedon = submittedon
        self.submittedby = submittedby

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'checkpart': self.checkpart,
            'checkpoint': self.checkpoint,
            'checkpointstatus': self.checkpointstatus,
            'description': self.description,
            'standardvalue': self.standardvalue,
            'status': self.status,
            'remark': self.remark,
            'submittedon': self.submittedon,
            'submittedby': self.submittedby
        }

class preventivemaintenancemaster(db.Model):
    __tablename__ = 'preventivemaintenancemaster'

    id = db.Column(db.Integer, primary_key=True)
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable = False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable = False)
    durationtype = db.Column(db.Integer, db.ForeignKey('durationtype.id'), nullable = False)
    durationvalue = db.Column(db.Integer)
    uploadedby = db.Column(db.String())
    createdon = db.Column(db.DateTime)
    lastupdatedon = db.Column(db.DateTime)

    def __init__(self, assetcategory, asset, durationtype, durationvalue, uploadedby, createdon, lastupdatedon):
        self.assetcategory = assetcategory
        self.asset = asset
        self.durationtype = durationtype
        self.durationvalue = durationvalue
        self.uploadedby = uploadedby
        self.createdon = createdon
        self.lastupdatedon = lastupdatedon

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'assetcategory': self.assetcategory,
            'asset': self.asset,
            'durationtype': self.durationtype,
            'durationvalue': self.durationvalue,
            'uploadedby': self.uploadedby,
            'createdon': self.createdon,
            'lastupdatedon': self.lastupdatedon
        }

class preventivemaintenance(db.Model):
    __tablename__ = 'preventivemaintenance'

    id = db.Column(db.Integer, primary_key=True)
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable = False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable = False)
    durationtype = db.Column(db.Integer, db.ForeignKey('durationtype.id'), nullable = False)
    durationvalue = db.Column(db.Integer)
    allchecklistcompleted = db.Column(db.Boolean)
    submittedyear = db.Column(db.Integer)
    submittedon = db.Column(db.DateTime)
    submittedby = db.Column(db.String())
    isautosubmit = db.Column(db.Boolean)
    assignedon = db.Column(db.DateTime)
    submittedbysupervisor = db.Column(db.String())

    def __init__(self, assetcategory, asset, allchecklistcompleted, durationtype, durationvalue, submittedyear, submittedon, submittedby, isautosubmit, assignedon, submittedbysupervisor):
        self.assetcategory = assetcategory
        self.asset = asset
        self.durationtype = durationtype
        self.allchecklistcompleted = allchecklistcompleted        
        self.durationvalue = durationvalue
        self.submittedyear = submittedyear
        self.submittedon = submittedon
        self.submittedby = submittedby
        self.isautosubmit = isautosubmit
        self.assignedon = assignedon
        self.submittedbysupervisor = submittedbysupervisor

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'assetcategory': self.assetcategory,
            'asset': self.asset,
            'durationtype': self.durationtype,
            'allchecklistcompleted': self.allchecklistcompleted,
            'durationvalue': self.durationvalue,
            'submittedyear': self.submittedyear,
            'submittedon': self.submittedon,
            'submittedby': self.submittedby,
            'isautosubmit': self.isautosubmit,
            'assignedon': self.assignedon,
            'submittedbysupervisor': self.submittedbysupervisor
        }

class preventivemaintenancemaster_checklistmaster(db.Model):
    __tablename__ = 'preventivemaintenancemaster_checklistmaster'
    
    id = db.Column(db.Integer, primary_key=True)
    preventivemaintenancemaster = db.Column(db.Integer, db.ForeignKey('preventivemaintenancemaster.id'), nullable = False)
    checklistmaster = db.Column(db.Integer, db.ForeignKey('checklistmaster.id'), nullable = False)

    def __init__(self, preventivemaintenancemaster,checklistmaster):
        self.preventivemaintenancemaster = preventivemaintenancemaster
        self.checklistmaster = checklistmaster

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'preventivemaintenancemaster': self.preventivemaintenancemaster,
            'checklistmaster': self.checklistmaster
        }

class preventivemaintenance_checklist(db.Model):
    __tablename__ = 'preventivemaintenance_checklist'

    id = db.Column(db.Integer, primary_key=True)
    preventivemaintenance = db.Column(db.Integer, db.ForeignKey('preventivemaintenance.id'), nullable = False)
    checklist = db.Column(db.Integer, db.ForeignKey('checklist.id'), nullable = False)

    def __init__(self, preventivemaintenance, checklist):
        self.preventivemaintenance = preventivemaintenance
        self.checklist = checklist

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'preventivemaintenance': self.preventivemaintenance,
            'checklist': self.checklist
        }

@nkc.route('/duration-type', methods=['POST', 'GET'])
def durationTypeSave():
    if request.method == 'POST':
        data = request.get_json()
        duration_type = durationtype(durationtype = data['durationtype'], lowlimit = data['lowlimit'], highlimit = data['highlimit'], status = True)

        db.session.add(duration_type)
        db.session.commit()

        data = {"message": f"Duration created successfully"}
        return jsonify(data), 200

    elif request.method == 'GET':
        things = durationtype.query.all()
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id" : thing.id,
                        "durationtype" : thing.durationtype,
                        "lowlimit" : thing.lowlimit,
                        "highlimit" : thing.highlimit,
                        "status" : thing.status
                    }
                    results.append(resultsObj)
        return  jsonify(results)

@nkc.route('/duration-type/<id>', methods=['GET', 'PUT', 'DELETE'])
def durationTypeUpdate(id):
    durationTypeById = durationtype.query.get_or_404(id)

    if request.method == 'GET':
        response =   {
                "id" : durationTypeById.id,
                "durationtype" : durationTypeById.durationtype,
                "lowlimit" : durationTypeById.lowlimit,
                "highlimit" : durationTypeById.highlimit,
                "status" : durationTypeById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        durationTypeById.durationtype = data['durationtype']
        durationTypeById.lowlimit = data['lowlimit']
        durationTypeById.highlimit = data['highlimit']
        
        db.session.add(durationTypeById)
        db.session.commit()
        data = {"message": f"Duration updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
    
        db.session.delete(durationTypeById)
        db.session.commit()
    
        data = {"message": f"Duration deleted successfully"}
        return jsonify(data), 200

@nkc.route('/checklist-assigned', methods=['PUT'])
def checklistOk():
    if request.method == 'PUT':
        data = request.get_json()
        checklistbyid = checklist.query.get_or_404(data['id'])
        checklistbyid.checkpointstatus = data['checkpointstatus']
        checklistbyid.remark = data['remark']
        checklistbyid.submittedby = data['submittedby']
        checklistbyid.submittedon = datetime.now()
        db.session.add(checklistbyid)
        db.session.commit()
        data = {"message": f"checklist updated successfully"}
        return jsonify(data), 200

@nkc.route('/preventive-maintenance-submit', methods=['PUT'])
def preventiveMaintenanceSubmit():
    if request.method == 'PUT':
        data = request.get_json()
        preventivemaintenanceById = preventivemaintenance.query.get_or_404(data['id'])
        if preventivemaintenanceById.submittedby:
            data = {"message": f"Already Submitted."}
            return jsonify(data), 500
        else:
            preventivemaintenanceById.allchecklistcompleted = True
            preventivemaintenanceById.isautosubmit = False
            preventivemaintenanceById.submittedby = data['submittedby']
            preventivemaintenanceById.submittedon = datetime.now()
            preventivemaintenanceById.submittedbysupervisor =False

            db.session.add(preventivemaintenanceById)
            db.session.commit()
        
            data = {"message": f"Submitted successfully"}
            return jsonify(data), 200

@nkc.route('/preventive-maintenance-by-assetcategory-asset-duration', methods=['GET'])
def preventiveMaintenanceGet():
    if request.method == 'GET':
        data = request.get_json()
        assetCategoryId = assetcategory.query.filter(assetcategory.name == data['assetcategory'], assetcategory.status == True).value('id')
        assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value('id')
        durationTypeId = durationtype.query.filter(durationtype.durationtype == data['durationtype'], durationtype.status ==True).value('id')

        preventivemaintenancelist = preventivemaintenance.query.filter(preventivemaintenance.assetcategory == assetCategoryId, preventivemaintenance.asset == assetId ,preventivemaintenance.durationtype == durationTypeId, preventivemaintenance.durationvalue == data['durationvalue'])
        if preventivemaintenancelist:
            #preventivemaintenancelist.reverse()
            for preventivemaintenance_Obj in preventivemaintenancelist:
                preventivemaintenanceObj = preventivemaintenance_Obj
            checklistmapp_list = preventivemaintenance_checklist.query.filter(preventivemaintenance_checklist.preventivemaintenance == preventivemaintenanceObj.id)
            checklist_list = []
            for checklistObj in checklistmapp_list:
                checklists = checklist.query.filter(checklist.id == checklistObj.checklist).first()
                checklist_list.append(checklists)
            data = {
                "id":preventivemaintenanceObj.id,
                "assetcategory": preventivemaintenanceObj.assetcategory,
                "asset": preventivemaintenanceObj.asset,
                "durationtype": preventivemaintenanceObj.durationtype,
                "durationvalue": preventivemaintenanceObj.durationvalue,
                "allchecklistcompleted": preventivemaintenanceObj.allchecklistcompleted,
                "submittedyear": preventivemaintenanceObj.submittedyear,
                "submittedon": preventivemaintenanceObj.submittedon,
                "submittedby": preventivemaintenanceObj.submittedby,
                "isautosubmit": preventivemaintenanceObj.isautosubmit,
                "assignedon": preventivemaintenanceObj.assignedon,
                "submittedbysupervisor": preventivemaintenanceObj.submittedbysupervisor,
                "checklist": [{
                    "id": checklist.id,
                    "checkpart": checklist.checkpart,
                    "checkpoint": checklist.checkpoint,
                    "checkpointstatus": checklist.checkpointstatus,
                    "description": checklist.description,
                    "standardvalue": checklist.standardvalue,
                    "status": checklist.status,
                    "remark": checklist.remark,
                    "submittedon": checklist.submittedon,
                    "submittedby": checklist.submittedby
                }for checklist in checklist_list]
            }
            
            return jsonify(data)
        else:
            data = {"message": f"There no maintenance present."}
            return jsonify(data), 500

#@sched.scheduled_job('cron', id='preventive_maintenance', hour=0, minute=0)
def preventiveMaintenanceScheduler():
    print("*******************************Scheduler**Running*************************************************")
    now = datetime.now()
    #currentday = now.strftime("%d/%m/%Y %H:%M:%S")
    #latestAretHr = str(int(alertLatest[7].strftime("%H")) + 2)
    currentDay = now.strftime("%d")
    currentMonth = now.strftime("%m")
    currentYear = now.strftime("%Y")

    preventivemaintenancemaster_list = preventivemaintenance.query.all()
    for preventivemaintenancemaster in preventivemaintenancemaster_list:
        preventivemaintenance_list = preventivemaintenance.query.filter(preventivemaintenance.assetCategory == preventivemaintenancemaster.assetCategory, preventivemaintenance.asset == preventivemaintenancemaster.asset, preventivemaintenance.durationtype == preventivemaintenancemaster.durationtype,preventivemaintenance.durationvalue == preventivemaintenancemaster.durationvalue).value(all)
        for preventivemaintenance in preventivemaintenance_list:
            preventivemaintenanceObj = preventivemaintenance
        if preventivemaintenance_list:
            durationtypeObj = durationtype.query.filter(durationtype.id == preventivemaintenancemaster.durationtype, durationtype.status ==True).value(all)
            if durationtypeObj.durationtype == "Day":
                assignedon = preventivemaintenanceObj.assignedon.strftime("%d")
                if (currentDay - assignedon) == preventivemaintenancemaster.durationvalue:
                    if preventivemaintenanceObj.submittedby is None:
                        submitAllCheckList(preventivemaintenanceObj)
                    bindAllCheckList(preventivemaintenancemaster.id)
            if durationtypeObj.durationtype == "Week":
                currentWeek = ((now.day - 1) // 7 + 1)
                assignedWeek = ((preventivemaintenanceObj.assignedon.day - 1) // 7 + 1)
                if (currentWeek - assignedWeek) == preventivemaintenancemaster.durationvalue:
                    if preventivemaintenanceObj.submittedby is None:
                        submitAllCheckList(preventivemaintenanceObj)
                    bindAllCheckList(preventivemaintenancemaster.id)
            if durationtypeObj.durationtype == "Month":
                assignedMonth = preventivemaintenanceObj.assignedon.strftime("%m")
                if (currentMonth - assignedMonth) == preventivemaintenancemaster.durationvalue:
                    if preventivemaintenanceObj.submittedby is None:
                        submitAllCheckList(preventivemaintenanceObj)
                    bindAllCheckList(preventivemaintenancemaster.id)
            if durationtypeObj.durationtype == "Year":
                assignedYear = preventivemaintenanceObj.assignedon.strftime("%y")
                if (currentYear - assignedYear) == preventivemaintenancemaster.durationvalue:
                    if preventivemaintenanceObj.submittedby is None:
                        submitAllCheckList(preventivemaintenanceObj)
                    bindAllCheckList(preventivemaintenancemaster.id)
        else:
            bindAllCheckList(0)

def bindAllCheckList(preventivemaintenancemasterId):
    now = datetime.now()
    currentYear = now.strftime("%Y")
    preventivemaintenancemaster_list = []
    if preventivemaintenancemasterId > 0:
        preventivemaintenancemaster = preventivemaintenancemaster.query.get_or_404(preventivemaintenancemasterId)
        preventivemaintenancemaster_list.append(preventivemaintenancemaster)
    else:
        preventivemaintenancemaster_list = preventivemaintenancemaster.query.all()
    for preventivemaintenancemasterObj in preventivemaintenancemaster_list:
        checklistmaster_list = preventivemaintenancemaster_checklistmaster.query.filter(preventivemaintenancemaster_checklistmaster.preventivemaintenancemaster == preventivemaintenancemaster_list.id).value(all)
        if checklistmaster_list:
            checklistmaster_data = []
            for checklistmasterObj in checklistmaster_list:
                checklistmaster = checklistmaster.query.filter(checklistmaster.id == checklistmasterObj.checklistmaster).value(all)
                checklistmaster_data.append(checklistmaster)
            preventivemaintenance_data = preventivemaintenance(assetcategory = preventivemaintenancemasterObj.assetcategory,asset = preventivemaintenancemasterObj.asset, durationtype = preventivemaintenancemasterObj.durationtype, durationvalue = preventivemaintenancemasterObj.durationvalue, submittedyear = currentYear)
            
            db.session.add(preventivemaintenance_data)
            db.session.commit()

            #checklist_assigned = []
            for checklistmasterObj in checklistmaster_data:
                checklist_data = checklist(checkpart = checklistmasterObj.checkpart, checkpoint = checklistmasterObj.checkpoint,description = checklistmasterObj.description,standardvalue = checklistmasterObj.standardvalue, status = True)
                db.session.add(checklist_data)
                db.session.commit()

                preventivemaintenance_checklist = preventivemaintenance_checklist(preventivemaintenance = preventivemaintenance_data.id, checklist = checklist_data.id)
                db.session.add(checklist_data)
                db.session.commit()

def submitAllCheckList(preventivemaintenanceObj):
    now = datetime.now()
    checkpontsNoDone = 0
    preventivemaintenance_checklist_list = preventivemaintenance_checklist.query.filter(preventivemaintenance_checklist.preventivemaintenance == preventivemaintenanceObj.id).value(all)
    for preventivemaintenance_checklist in preventivemaintenance_checklist_list:
        checklist_status = checklist.query.filter(checklist.id == preventivemaintenance_checklist.checklist).value('checkpointstatus')
        if checklist_status is None or checklist_status == False:
            checkpontsNoDone = checkpontsNoDone + 1
    if checkpontsNoDone > 0:
        preventivemaintenanceObj.allchecklistcompleted = False
    else:
        preventivemaintenanceObj.allchecklistcompleted = True
    preventivemaintenanceObj.submittedon = now
    preventivemaintenanceObj.isautosubmit = True
    preventivemaintenanceObj.submittedby = "Auto Submitted"

    db.session.add(preventivemaintenanceObj)
    db.session.commit()
    #ALERT BINDING IS PENDING

@nkc.route('/preventive-maintenance-import', methods=['POST'])
def upload_preventiveMaintenance():
    if request.method == 'POST':
        data = request.get_json()
        flask_file = request.files['file']
        if not flask_file:
            return 'Upload a CSV file'
        
        stream = codecs.iterdecode(flask_file.stream, 'utf-8')
        csv_test = csv.reader(stream, dialect=csv.excel)
        pm_response = []
        rowNo = 0
        for row in csv_test:
            if row:
                if rowNo > 0:
                    excelRowFieldValidaton(row, rowNo)
                    response_data = {
                        'checkpart': row[0],
                        'checkpoint': row[1],
                        'description': row[2],
                        'standardvalue': row[3]
                    }
                    pm_response.append(response_data)
                rowNo = rowNo + 1
        return jsonify(pm_response), 200

def excelRowFieldValidaton(row, rowNo):
    if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '':
        data = {"message": f"Please enter all data in row number {rowNo}"}
        return jsonify(data), 500
    if type(row[0]) != str or type(row[1]) != str or type(row[2]) != int or type(row[3]) != str:
        data = {"message": f"Please check all data in row number {rowNo}"}
        return jsonify(data), 500

@nkc.route('/preventive-maintenance-save-import', methods = ['POST'])
def save_preventiveMaintenance():
    if request.method == 'POST':
        now = datetime.now()
        if request.is_json:
            data = request.get_json()
            for dataObj in data:
                assetcategoryId = assetcategory.query.filter(assetcategory.name == dataObj['assetcategory'], assetcategory.status == True).value("id")
                assetId = asset.query.filter(asset.name == dataObj['asset'], asset.assetcategory == assetcategoryId, asset.status ==True).value("id")
                durationtypeId = durationtype.query.filter(durationtype.durationtype == dataObj['durationtype'], durationtype.status == True).value("id")
                preventivemaintenancemaster_save = preventivemaintenancemaster(assetcategory = assetcategoryId, asset = assetId, durationtype = durationtypeId, durationvalue = dataObj['durationvalue'],uploadedby = dataObj['uploadedby'], createdon = now, lastupdatedon = now)
                db.session.add(preventivemaintenancemaster_save)
                db.session.commit()

                checkListMasters=[]
                checklistmaster_list = dataObj['checklistmaster']
                for checklistmasterObj in checklistmaster_list:
                    checklistmaster_save = checklistmaster(checkpart = checklistmasterObj['checkpart'], checkpoint = checklistmasterObj['checkpoint'],description = checklistmasterObj['description'],standardvalue = checklistmasterObj['standardvalue'],status = True,createdon = now,updatedon = now)
                    db.session.add(checklistmaster_save)
                    db.session.commit()

                    preventivemaintenancemaster_checklistmaster_save = preventivemaintenancemaster_checklistmaster(preventivemaintenancemaster = preventivemaintenancemaster_save.id, checklistmaster = checklistmaster_save.id)
                    db.session.add(preventivemaintenancemaster_checklistmaster_save)
                    db.session.commit()
                dataResp = {"message": f"Preventive maintenance created successfully"}
                return jsonify(dataResp), 200
        else:
            return {"error": "The request payload is not in JSON format"}

#------------------------------Influx Data--------------------------------------------------

#influxdb = influxDBConn.influxConn()

def getInfluxTableName(assetId):
    asset_data = asset.query.get_or_404(assetId)
    companylocation_data = companylocation.query.get_or_404(asset_data.companylocation)
    assetcategory_data = assetcategory.query.get_or_404(asset_data.assetcategory)
    tableName = f'{companylocation_data.location}_{assetcategory_data.name}_{asset_data.name}_{asset_data.id}_Data'
    return tableName

@nkc.route('/importData', methods=['POST'])
def importSensorData():
    assets = asset.query.filter(asset.status == True).value(all)
    #assets = mySqlDataConnection.mySqlDbGetAll(assetQuery)
    for asset in assets:
        companylocation = companylocation.query.filter(companylocation.id == asset.companylocation).value('location')
        assetcategory = assetcategory.query.filter(assetcategory.id == asset.assetcategory).value('name')
        tableName = f'{companylocation}_{assetcategory}_{asset.name}_{asset.id}_Data'
        insertData(tableName, asset.id)
    
    data = {"message": f"Data Inserted successfully"}
    return jsonify(data), 200

def insertData(tableName, assetId):
    CSVReader = pd.read_csv('AssetData.csv')
    for rows_index, row in CSVReader.iterrows():
        if assetId == row[2]:
            company_location = row[0]
            asset_category = row[1]
            asset_id = row[2]
            asset_name = row[3]
            cc_link_nw_status = row[4]
            ethernet_network_status = row[5]
            tl_comm_status = row[6]
            tl_status = row[7]
            cc_link_Card = row[8]
            io_card = row[9]
            plc = row[10]
            preventive_analysis = row[11]
            chain_elongation = row[12]
            abnormal_vibration = row[13]
            power_line1_value = row[14]
            power_line2_value = row[15]
            power_line3_value  = row[16]
            motor_vibration_x_axis = row[17]
            motor_vibration_z_axis = row[18]
            mast_vibration_x_axis = row[19]
            mast_vibration_z_axis = row[20]
            available_time = row[21]
            machine_down_time = row[22]
            tl_utilization = row[23]
            cycle_time = row[24]
            voltage_line1_value = row[25]
            voltage_line2_value = row[26]
            voltage_line3_value = row[27]
            current_line1_value = row[28]
            current_line2_value = row[29]
            current_line3_value = row[30]
            frequency_line1_value = row[31]
            frequency_line2_value = row[32]
            frequency_line3_value = row[33]
            proximity_value = row[34]
            temperature_value = row[35]
            asset_running_status = row[36]

            json_body = [{
                "measurement":tableName,
                "time":datetime.now(),
                "fields":{
                    'company_location':company_location,
                    'asset_category':asset_category,
                    'asset_id' : asset_id,
                    'asset_name' : asset_name,
                    'cc_link_nw_status' : cc_link_nw_status,
                    'ethernet_network_status' : ethernet_network_status,
                    'tl_comm_status' : tl_comm_status,
                    'tl_status' : tl_status,
                    'cc_link_Card' : cc_link_Card,
                    'io_card' : io_card,
                    'plc' : plc,
                    'preventive_analysis' : preventive_analysis,
                    'chain_elongation' : chain_elongation,
                    'abnormal_vibration' : abnormal_vibration,
                    'power_line1_value' : power_line1_value,
                    'power_line2_value' : power_line2_value,
                    'power_line3_value' : power_line3_value,
                    'motor_vibration_x_axis' : motor_vibration_x_axis,
                    'motor_vibration_z_axis' : motor_vibration_z_axis,
                    'mast_vibration_x_axis' : mast_vibration_x_axis,
                    'mast_vibration_z_axis' : mast_vibration_z_axis,
                    'available_time' : available_time,
                    'machine_down_time' : machine_down_time,
                    'tl_utilization' : tl_utilization,
                    'cycle_time' : cycle_time,
                    'voltage_line1_value' : voltage_line1_value,
                    'voltage_line2_value' : voltage_line2_value,
                    'voltage_line3_value' : voltage_line3_value,
                    'current_line1_value' : current_line1_value,
                    'current_line2_value' : current_line2_value,
                    'current_line3_value' : current_line3_value,
                    'frequency_line1_value' : frequency_line1_value,
                    'frequency_line2_value' : frequency_line2_value,
                    'frequency_line3_value' : frequency_line3_value,
                    'proximity_value' : proximity_value,
                    'temperature_value' : temperature_value,
                    'asset_running_status' : asset_running_status
                }
            }]
            influxdb.write_points(json_body)
            time.sleep(1)
    insertData(tableName, assetId)

@nkc.route('/trend-live-data/<assetId>', methods=['GET'])
def trendLiveData(assetId):
    tableName = getInfluxTableName(assetId)
    dataQuery = 'SELECT * FROM %s WHERE asset_id = %s ORDER BY time DESC LIMIT 1'
    result = influxdb.query((dataQuery) % (tableName, assetId))
    points = list(result.get_points())
    assetLiveData = points[0]
    results ={
                "time" : assetLiveData["time"],
                "asset_category": assetLiveData["asset_category"],
                "asset_id": assetLiveData["asset_id"],
                "asset_name": assetLiveData["asset_name"],
                "voltage_line1_value": assetLiveData["voltage_line1_value"],
                "voltage_line2_value": assetLiveData["voltage_line2_value"],
                "voltage_line3_value": assetLiveData["voltage_line3_value"],
                "current_line1_value": assetLiveData["current_line1_value"],
                "current_line2_value": assetLiveData["current_line2_value"],
                "current_line3_value": assetLiveData["current_line3_value"],
                "power_line1_value": assetLiveData["power_line1_value"],
                "power_line2_value": assetLiveData["power_line2_value"],
                "power_line3_value": assetLiveData["power_line3_value"],
                "frequency_line1_value": assetLiveData["frequency_line1_value"],
                "frequency_line2_value": assetLiveData["frequency_line2_value"],
                "frequency_line3_value": assetLiveData["frequency_line3_value"],
                "motor_vibration_x_axis": assetLiveData["motor_vibration_x_axis"],
                "motor_vibration_z_axis": assetLiveData["motor_vibration_z_axis"],
                "mast_vibration_x_axis": assetLiveData["mast_vibration_x_axis"],
                "mast_vibration_z_axis": assetLiveData["mast_vibration_z_axis"],
                "temperature_value": assetLiveData["temperature_value"]
            }
    return jsonify(results), 200

@nkc.route('/kpi-live-data/<assetId>', methods=['GET'])
def kpiLiveData(assetId):
    tableName = getInfluxTableName(assetId)
    dataQuery = 'SELECT * FROM %s WHERE asset_id = %s ORDER BY time DESC LIMIT 1'
    result = influxdb.query((dataQuery) % (tableName, assetId))
    points = list(result.get_points())
    assetLiveData = points[0]
    results ={
        "time":assetLiveData["time"],
        "tl_comm_status": assetLiveData["tl_comm_status"],
        "power_line1_value": assetLiveData["power_line1_value"],
        "power_line2_value": assetLiveData["power_line2_value"],
        "power_line3_value": assetLiveData["power_line3_value"],
        "motor_vibration_x_axis": assetLiveData["motor_vibration_x_axis"],
        "motor_vibration_z_axis": assetLiveData["motor_vibration_z_axis"],
        "mast_vibration_x_axis": assetLiveData["mast_vibration_x_axis"],
        "mast_vibration_z_axis": assetLiveData["mast_vibration_z_axis"],
        "temperature_value": assetLiveData["temperature_value"]
    }
    return jsonify(results), 200

influxdb.close()

# def setInterval(func,time):
#     e = threading.Event()
#     while not e.wait(time):
#         func()

# setInterval(preventiveMaintenanceScheduler,5)


#------------------------------Loss Analysis--------------------------------------------------

if __name__ == '__main__':
    #scheduler.add_job(id = 'preventive maintenance', func=preventiveMaintenanceScheduler, hour=0, minute=0)
    #scheduler.start()
    nkc.run(debug=True)