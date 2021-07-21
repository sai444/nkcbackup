import json
from functools import wraps
import datetime
import jwt
from flask import Flask, jsonify, request,make_response
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from influxdb import InfluxDBClient
from main.alert.alertResource import alert_api
from main.asset.assetResource import asset_api
from main.companyLocation.locationResource import location_api
from main.kpi.kpi import kpi_api
from main.lossAnalysis.lossAnalysisResource import loss_api
from main.preventiveMaintenance.preventiveMaintenanceResource import (
    pm_api, preventiveMaintenanceScheduler)
from main.sensor.sensor_resource import sensor_api
from main.shift.shift_resource import shift_api
from main.user.user_resource import user_api
from main.role.role_resource import role_api
from main.alert.alertNewResource import alertnew_api

app = Flask(__name__)
prefix = '/api/v1'
app.register_blueprint(shift_api,url_prefix=prefix)
app.register_blueprint(kpi_api,url_prefix=prefix)
app.register_blueprint(user_api,url_prefix=prefix)
app.register_blueprint(sensor_api,url_prefix=prefix)
app.register_blueprint(alert_api,url_prefix=prefix)
app.register_blueprint(asset_api,url_prefix=prefix)
app.register_blueprint(location_api,url_prefix=prefix)
app.register_blueprint(pm_api,url_prefix=prefix)
app.register_blueprint(loss_api,url_prefix=prefix)
app.register_blueprint(role_api,url_prefix=prefix)
app.register_blueprint(alertnew_api,url_prefix=prefix)

# --------- localhost---------
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@123@localhost:5432/mytestdb"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5433/nkc2"

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/demo"

# -------------SERVER------------
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5433/nkc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 5000


# app.config["SQLALCHEMY_BINDS"] = databases
app.config['SECRET_KEY']='iotmaxapplication'


db = SQLAlchemy(app)
scheduler = APScheduler()
# ----------------Influx conection---------------
with open('config.json', 'r') as c:
    influxConnection = json.load(c)["influxDBDetails"]

influxdb = InfluxDBClient(influxConnection['influxHost'],influxConnection['influxPort'],influxConnection['indluxId'],influxConnection["influxPassword"],influxConnection['influxDBName'])
influxdb.create_database(influxConnection['influxDBName'])
influxdb.get_list_database()
influxdb.switch_database(influxConnection['influxDBName'])
# ----------------Influx conection---------------

from models import dept, role

cors = CORS(app, resources={
    r"/*": {
        "origins": "*",
        "Access-Control-Allow-Origin": "*"
    }
})
def token_required(f):
    @wraps(f)
    def decorated(args,*kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'Token is invalid'}),403
        try:
            datas = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Token is invalid'}),403
        return f(args,*kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login_user():
    from models import role, user
    username = request.get_json()['username']
    password = request.get_json()['password']

    login_user = user.query.filter(user.username == username).value('password')

    id = user.query.filter(user.username == username).value('id')
    roleid = user.query.filter(user.username == username).value('role_id')

    roless =  role.query.filter(role.id == roleid).value('name')
    print(roless ,'roless', username)
    print(type(login_user),login_user)
    if username:
        if login_user == password:
            token= jwt.encode({'username':username,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=11000)},app.config['SECRET_KEY'])
            return jsonify({'token' : token.decode('UTF-8'),'username' :username,'id': id  , "role" :roless })
        else :
            return make_response('could not verify password is wrong! ',401,{'www-Authenticate':'Basic realm="Login required"'})
    else:
        return make_response('could not verify username is wrong! ',401,{'www-Authenticate':'Basic realm="Login required"'})
    return ' imei is not registered'

@app.route("/")
def hello():
    return "Hello welcome to ToDo API!"



@app.route('/role/<id>', methods=['GET', 'PUT', 'DELETE'])
def role2(id):
    car = role.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id": car.id,
            "name": car.name,
            "dept": dept.query.filter(dept.id == car.dept).value('name'),
            "description": car.description

        }
        return jsonify(response)
    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.dept = dept.query.filter(dept.name == data['dept']).value('id')
        car.description = data['description']

        db.session.add(car)
        db.session.commit()
        data = {"message": f"name updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        data = {"message": f"name deleted successfully"}
        return jsonify(data), 200


@app.route('/dept', methods=['POST', 'GET'])
def dept2():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            count = dept.query.filter(dept.name == data['name']).count()
            if count > 0:
                data = {"message": f"name already exists"}
                return jsonify(data), 400
            else:
                new_car = dept(name=data['name'], des=data['des'])
                db.session.add(new_car)
                db.session.commit()
                data = {"message": f"name created successfully"}
                return jsonify(data), 200

        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = dept.query.all()
        results = [
            {
                "id": thing.id,
                "name": thing.name,
                "des": thing.des
            } for thing in things]
        print("hello")
        return jsonify(results)


@app.route('/dept/<id>', methods=['GET', 'PUT', 'DELETE'])
def depts(id):
    car = dept.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id": car.id,
            "name": car.name,
            "des": car.des

        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.des = data['des']
        db.session.add(car)
        db.session.commit()
        data = {"message": f"name updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        data = {"message": f"name deleted successfully"}
        return jsonify(data), 200


if __name__ == '_main_':
    db.create_all()
    scheduler.add_job(id = 'preventive maintenance', func=preventiveMaintenanceScheduler, trigger="interval", hours=24, start_date='00:00:00')
    scheduler.start()
    app.run(debug=True , host = '122.166.167.113',port=4200)
