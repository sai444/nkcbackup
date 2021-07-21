from flask import Blueprint, request, jsonify
from datetime import datetime
import csv
import codecs

asset_api = Blueprint('asset_api', __name__)

@asset_api.route('/asset', methods=['POST', 'GET'])
def assetsave():
    from models import asset,assetcategory,companylocation,adminlog
    from app import db
    if request.method == 'POST':
        if request.is_json:
            now = datetime.now()
            data = request.get_json()
            count = asset.query.filter(asset.name == data['name'], asset.status == True).count()
            if count > 0:
                data = {"message": f"Asset name already exists"}
                return jsonify(data), 400
            else:
                assetcategory_id = assetcategory.query.filter(assetcategory.name == data['assetcategory']).value('id')
                companylocation_id = companylocation.query.filter(
                    companylocation.location == data['companylocation']).value('id')
                asset_data = asset(name=data['name'], description=data['description'], assetcategory=assetcategory_id,
                                   companylocation=companylocation_id, status=True)

                db.session.add(asset_data)
                db.session.commit()

                adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'asset', activitydone = 'save', activityid = asset_data.id)
                db.session.add(adminlogObj)
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
                        "id": thing.id,
                        "name": thing.name,
                        "description": thing.description,
                        "assetcategory": assetcategory.query.filter(assetcategory.id == thing.assetcategory).value(
                            'name'),
                        "companylocation": companylocation.query.filter(
                            companylocation.id == thing.companylocation).value('location'),
                        "status": thing.status
                    }
                    results.append(resultsObj)
        return jsonify(results)


@asset_api.route('/asset/<id>', methods=['GET', 'PUT'])
def assetUpdate(id):
    from models import asset,assetcategory,companylocation,adminlog
    from app import db
    assetById = asset.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'GET':
        response = {
            "id": assetById.id,
            "name": assetById.name,
            "description": assetById.description,
            "assetcategory": assetcategory.query.filter(assetcategory.id == assetById.assetcategory).value('name'),
            "companylocation": companylocation.query.filter(companylocation.id == assetById.companylocation).value(
                'location'),
            "status": assetById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        asset_old = asset.query.filter(asset.name == data['name'], asset.status == True).first()
        if asset_old:
            if int(asset_old.id) != int(id):
                data = {"message": f"Asset name already exists"}
                return jsonify(data), 500
        assetById.name = data['name']
        assetById.description = data['description']
        assetById.assetcategory = assetcategory.query.filter(assetcategory.name == data['assetcategory']).value('id')
        assetById.companylocation = companylocation.query.filter(
            companylocation.location == data['companylocation']).value('id')

        db.session.add(assetById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'asset', activitydone = 'update', activityid = assetById.id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Asset updated successfully"}
        return jsonify(data), 200

@asset_api.route('/asset/<id>/<logger>', methods=['DELETE'])
def assetDelete(id, logger):
    from models import asset,assetcategory,companylocation,adminlog
    from app import db
    assetById = asset.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'DELETE':

        db.session.delete(assetById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'asset', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Asset deleted successfully"}
        return jsonify(data), 200


@asset_api.route('/asset-by-assetcategory-location', methods=['POST'])
def assetDetails():
    from models import asset,assetcategory,companylocation
    if request.method == 'POST':
        data = request.get_json()
        assetcategory_id = assetcategory.query.filter(assetcategory.name == data['assetcategory'],
                                                      assetcategory.status == True).value('id')
        companylocation_id = companylocation.query.filter(companylocation.location == data['companylocation'],
                                                          companylocation.status == True).value('id')
        asset_data = asset.query.filter(asset.companylocation == companylocation_id,
                                        asset.assetcategory == assetcategory_id)
        if asset_data:
            response_list = []
            for assetObj in asset_data:
                response = {
                    "id": assetObj.id,
                    "name": assetObj.name,
                    "description": assetObj.description,
                    "assetcategory": data['assetcategory'],
                    "companylocation": data['companylocation'],
                    "status": assetObj.status
                }
                response_list.append(response)
            return jsonify(response_list)
        else:
            data = {"message": f"There is no data"}
            return jsonify(data), 500

@asset_api.route('/asset-category', methods=['POST', 'GET'])
def assetcategorysave():
    from models import assetcategory,adminlog
    from app import db
    if request.method == 'POST':
        now = datetime.now()
        data = request.get_json()
        assetcategory_old = assetcategory.query.filter(assetcategory.name == data['name'], assetcategory.status == True).first()
        if assetcategory_old:
            data = {"message": f"This category already present."}
            return jsonify(data), 500

        asset_category = assetcategory(name = data['name'], keyvalue = data['keyvalue'], status = True)

        db.session.add(asset_category)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'asset category', activitydone = 'save', activityid = asset_category.id)
        db.session.add(adminlogObj)
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

@asset_api.route('/asset-category/<id>', methods=['GET', 'PUT'])
def assetcategoryUpdate(id):
    from models import asset,assetcategory,companylocation,adminlog
    from app import db
    assetcategoryById = assetcategory.query.get_or_404(id)
    now = datetime.now()

    if request.method == 'GET':
        response = {
            "id" : assetcategoryById.id,
            "name" : assetcategoryById.name,
            "keyvalue" : assetcategoryById.keyvalue,
            "status" : assetcategoryById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        assetcategory_old = assetcategory.query.filter(assetcategory.name == data['name'], assetcategory.status == True).first()
        if assetcategory_old:
            if int(assetcategory_old.id) != int(id):
                data = {"message": f"This category already present."}
                return jsonify(data), 500

        assetcategoryById.name = data['name']
        assetcategoryById.keyvalue = data['keyvalue']

        db.session.add(assetcategoryById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'asset category', activitydone = 'update', activityid = assetcategoryById.id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Asset category updated successfully"}
        return jsonify(data), 200

@asset_api.route('/asset-category/<id>/<logger>', methods=['DELETE'])
def assetcategoryDelete(id,logger):
    from models import asset,assetcategory,companylocation,adminlog
    from app import db
    assetcategoryById = assetcategory.query.get_or_404(id)
    now = datetime.now()
    if request.method == 'DELETE':

        db.session.delete(assetcategoryById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger, module = 'asset category', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Asset category deleted successfully"}
        return jsonify(data), 200


@asset_api.route('/asset-configuration-import', methods=['POST'])
def upload_asset():
    from models import asset
    # data = request.get_json()
    flask_file = request.files['file']
    if not flask_file:
        return 'Upload a CSV file'
    # filename = flask_file.filename

    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    csv_test = csv.reader(stream, dialect=csv.excel)
    asset_response = []
    rowNo = 0
    for row in csv_test:
        if row:
            if rowNo > 0:
                assetid_old = 0
                assetExcelRowFieldValidaton(row, rowNo)
                assetid_old = asset.query.filter(asset.name == row[0], asset.status == True).count()
                if assetid_old > 0:
                    data = {"message": f"Asset name for row number {rowNo} already present!"}
                    return jsonify(data), 500
                response_data = {
                    'asset_name': row[0],
                    'description': row[1]
                }
                asset_response.append(response_data)
            rowNo = rowNo + 1
    return jsonify(asset_response), 200

def assetExcelRowFieldValidaton(row, rowNo):
    if row[0] == '' or row[1] == '':
        data = {"message": f"Please enter all data in row number {rowNo}"}
        return jsonify(data), 500
    if type(row[0]) != str or type(row[1]) != str:
        data = {"message": f"Please check all data in row number {rowNo}"}
        return jsonify(data), 500

@asset_api.route('/asset-configuration-save-import/<logger>', methods=['POST'])
def save_asset(logger):
    from models import asset,assetcategory,companylocation,adminlog
    from app import db
    now = datetime.now()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            for dataObj in data:
                companylocationId = companylocation.query.filter(companylocation.location == dataObj['companylocation'],
                                                                 companylocation.status == True).value("id")
                assetcategoryId = assetcategory.query.filter(assetcategory.name == dataObj['assetcategory'],
                                                             assetcategory.status == True).value("id")
                asset_save = asset(name=dataObj['name'], description=dataObj['description'],
                                   companylocation=companylocationId, assetcategory=assetcategoryId, status=True)

                db.session.add(asset_save)
                db.session.commit()

                adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'asset', activitydone = 'save', activityid = asset_save.id)
                db.session.add(adminlogObj)
                db.session.commit()

            data = {"message": f"Asset created successfully"}
            return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

@asset_api.route('/asset-first-sheet-cloumn-export', methods=['GET'])
def assetFirstSheetColumnNames():
    if request.method == 'GET':
        response_data = {
            'row0': 'Asset Name',
            'row1': 'Description'
        }
        return jsonify(response_data), 200
