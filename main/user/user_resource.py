import codecs
import csv
from datetime import datetime
from functools import wraps

import jwt as jwt
from flask import Blueprint, jsonify, request, make_response

user_api = Blueprint('user_api', __name__)


@user_api.route('/user')
def user_get():
    from models import user
    things = user.query.all()
    
    results = []
    for shiftObj in things:
        serial = user.serialize(shiftObj)
        from models import role,companylocation
        roleName = role.query.filter(role.id == serial['roleId']).value('name')
        plantName = companylocation.query.filter(companylocation.id == serial['plantId']).value('location')
        response_data = {
            'firstName': serial['firstName'],
            'middleName': serial['middleName'],
            'lastName': serial['lastName'],
            'userName': serial['username'],
            'password': serial['password'],
            'role':serial['roleId'],
            'roleName': roleName,
            'plant': serial['plantId'],
            'plantName': plantName,
            'companyLocation': serial['companyLocationId'],
            'id': serial['id']
        }
        results.append(response_data)
    return jsonify(results), 200


@user_api.route('/user-import', methods=['POST'])
def upload_userFile():
    if request.method == 'POST':
        flask_file = request.files['file']
        if not flask_file:
            return 'Upload a CSV file'
        # filename = flask_file.filename

        stream = codecs.iterdecode(flask_file.stream, 'utf-8')
        csv_test = csv.reader(stream, dialect=csv.excel)
        pm_response = []
        rowNo = 0
        for row in csv_test:
            if row:
                if rowNo > 0:
                    excelRowFieldValidaton(row, rowNo)

                    from models import role
                    roleName = role.query.filter(role.id == row[5]).value('name')
                    response_data = {
                        'firstName': row[0],
                        'middleName': row[1],
                        'lastName': row[2],
                        'userName': row[3],
                        'password': row[4],
                        'role': row[5],
                        'roleId': row[5],
                        'roleName': roleName,
                        'plant': "",
                        'companyLocation': ""
                    }
                    pm_response.append(response_data)
                rowNo = rowNo + 1
        return jsonify(pm_response), 200


def excelRowFieldValidaton(row, rowNo):
    if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '':
        data = {"message": f"Please enter all data in row number {rowNo}"}
        return jsonify(data), 500
    if type(row[0]) != str or type(row[1]) != str or type(row[2]) != str or type(row[3]) != str:
        data = {"message": f"Please check all data in row number {rowNo}"}
        return jsonify(data), 500

@user_api.route('/user-save-import',methods=['POST'])
def save_user():
    from models import user
    from app import db
    if request.method == 'POST':
        now = datetime.now()
        if request.is_json:
            dataobj = request.get_json()
            dataResp = {"message": f" "}
            for data in dataobj:
                # userObj = user.query.filter(user.name == dataObj['userName']).value("id")
                count = user.query.filter(user.username == data['username']).count()
                if count > 0:
                    data = {"message": data['userName']+"exists already"}
                    return jsonify(data), 400

                firstName = data['firstName']
                middleName = data['middleName']
                lastName = data['lastName']
                userName = data['username']
                roleId = data['roleId']
                plantId = data['plantId']
                password = data['password']

                userObj = user(True,firstName,lastName,middleName,password,userName,plantId,plantId,roleId)
                db.session.add(userObj)
                db.session.commit()
                dataResp = {"message": f"Preventive maintenance created successfully"}
            return jsonify(dataResp), 200
        else:
            return {"error": "The request payload is not in JSON format"}


@user_api.route('/user', methods=['POST'])
def add_user():
    from app import db
    from models import user, adminlog
    now = datetime.now()
    if request.method == 'POST':
        data = request.get_json()
        count = user.query.filter(user.username == data['username']).count()
        if count > 0:
            data = {"message": data['username'] + " already exists"}
            return jsonify(data), 400
        new_user = user(status=data['status'],
                        first_name=data['firstName'],
                        last_name=data['lastName'],
                        middle_name=data['middleName'],
                        password=data['password'],
                        username=data['username'],
                        role_id= data['roleId'],
                        company_location_id=data['companyLocationId'],  
                        plant_id=data['plantId'])

        db.session.add(new_user)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'user', activitydone = 'save', activityid = new_user.id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"name created successfully"}
        return jsonify(data), 200


@user_api.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
def depts(id):
    from app import db
    from models import user, adminlog
    now = datetime.now()
    userObj = user.query.get_or_404(id)

    if request.method == 'GET':
        response = user.serialize(userObj)
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        user_old = user.query.filter(user.username == data['username'], user.status == True).first()
        if user_old:
            if int(user_old.id) != int(id):
                data = {"message": f"user name already exists"}
                return jsonify(data), 500
        userObj.status = data['status']
        userObj.first_name = data['firstName']
        userObj.last_name = data['lastName']
        userObj.middle_name = data['middleName']
        userObj.password = data['password']
        userObj.username = data['username']
        userObj.company_location_id = data['companyLocationId']
        userObj.plant_id = data['plantId']
        userObj.role_id = data['roleId']

        db.session.add(userObj)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'user', activitydone = 'update', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"user updated successfully"}
        return jsonify(data), 200

    elif request.method == 'DELETE':
        data = request.get_json()
        db.session.delete(userObj)
        db.session.commit()

        data = {"message": f"name deleted successfully"}
        return jsonify(data), 200

@user_api.route('/user-delete/<id>/<logger>', methods=['DELETE'])
def delete_user(id, logger):
    from app import db
    from models import user, adminlog
    now = datetime.now()
    userObj = user.query.get_or_404(id)
    db.session.delete(userObj)
    db.session.commit()

    adminlogObj = adminlog(loggedon = now, loggedby = logger, module = 'user', activitydone = 'delete', activityid = id)
    db.session.add(adminlogObj)
    db.session.commit()

    data = {"message": f"User deleted successfully"}
    return jsonify(data), 200

# @user_api.route('/login', methods=['POST'])
def login_user():

    from models import user,role
    username = request.get_json()['username']
    password = request.get_json()['password']

    login_user = user.query.filter(user.username == username).value('password')

    id = user.query.filter(user.username == username).value('id')
    roleid = user.query.filter(user.username == username).value('roleId')

    roless =  role.query.filter(role.id == roleid).value('name')
    
    if username:
        if login_user == password:
            token= jwt.encode({'username':username,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=11000)},user_api.config['SECRET_KEY'])
            return jsonify({'token' : token.encode().decode('UTF-8'),'username' :username,'id': id  , "role" :roless })
        else :
            return make_response('could not verify password is wrong! ',401,{'www-Authenticate':'Basic realm="Login required"'})
    else:
        return make_response('could not verify username is wrong! ',401,{'www-Authenticate':'Basic realm="Login required"'})
    return ' imei is not registered'


# user_api.config['SECRET_KEY']='iotmaxapplication'
#
# def token_required(f):
#     @wraps(f)
#     def decorated(args,*kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'message':'Token is invalid'}),403
#         try:
#             datas = jwt.decode(token,user_api.config['SECRET_KEY'])
#         except:
#             return jsonify({'message':'Token is invalid'}),403
#         return f(args,*kwargs)
#     return decorated