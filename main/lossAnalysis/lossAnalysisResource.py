from datetime import datetime, date

from flask import Blueprint, request, jsonify

loss_api = Blueprint('loss_api', __name__)

@loss_api.route('/loss-category', methods=['POST', 'GET'])
def losscategorysave():
    from models import losscategory,adminlog
    from app import db
    now = datetime.now()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            losscategory_old = losscategory.query.filter(losscategory.losscategory == data['losscategory'], losscategory.status == True).first()
            if losscategory_old:
                data = {"message": f"Loss category already exist."}
                return jsonify(data), 500

            losscategory_data = losscategory(losscategory=data['losscategory'], description=data['description'],
                                             status=True)

            db.session.add(losscategory_data)
            db.session.commit()

            adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'loss category', activitydone = 'save', activityid = losscategory_data.id)
            db.session.add(adminlogObj)
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
                        "id": thing.id,
                        "losscategory": thing.losscategory,
                        "description": thing.description,
                        "status": thing.status
                    }
                    results.append(resultsObj)
        return jsonify(results)


@loss_api.route('/loss-category/<id>', methods=['GET', 'PUT'])
def losscategoryUpdate(id):
    from models import losscategory,adminlog
    from app import db
    now = datetime.now()
    losscategoryById = losscategory.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id": losscategoryById.id,
            "losscategory": losscategoryById.losscategory,
            "description": losscategoryById.description,
            "status": losscategoryById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        losscategory_old = losscategory.query.filter(losscategory.losscategory == data['losscategory'], losscategory.status == True).first()
        if losscategory_old:
            if int(losscategory_old.id) != int(id):
                data = {"message": f"Loss category name already exist."}
                return jsonify(data), 500
        losscategoryById.losscategory = data['losscategory']
        losscategoryById.description = data['description']

        db.session.add(losscategoryById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'loss category', activitydone = 'update', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Loss category updated successfully"}
        return jsonify(data), 200

@loss_api.route('/loss-category/<id>/<logger>', methods=['DELETE'])
def losscategoryDelete(id, logger):
    from models import losscategory,adminlog
    from app import db
    now = datetime.now()
    losscategoryById = losscategory.query.get_or_404(id)

    if request.method == 'DELETE':

        db.session.delete(losscategoryById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger, module = 'loss category', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Loss category deleted successfully"}
        return jsonify(data), 200


@loss_api.route('/loss-sub-category', methods=['POST', 'GET'])
def losssubcategorysave():
    from models import losscategory,losssubcategory,adminlog
    from app import db
    now = datetime.now()
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            count = losssubcategory.query.filter(losssubcategory.losssubcategory == data['losssubcategory'],
                                                 losssubcategory.status == True).count()
            if count > 0:
                data = {"message": f"This loss subcategory name already exists"}
                return jsonify(data), 400
            else:
                losscategory_id = losscategory.query.filter(losscategory.losscategory == data['losscategory'],
                                                            losscategory.status == True).value('id')
                losssubcategory_data = losssubcategory(losssubcategory=data['losssubcategory'],
                                                       description=data['description'], status=True,
                                                       losscategory=losscategory_id)

                db.session.add(losssubcategory_data)
                db.session.commit()

                adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'loss subcategory', activitydone = 'save', activityid = losssubcategory_data.id)
                db.session.add(adminlogObj)
                db.session.commit()

                data = {"message": f"Loss subcategory created successfully"}
                return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = losssubcategory.query.all()
        # losscategoryById = losscategory.query.get_or_404(id)
        results = []
        if things:
            for thing in things:
                if thing.status == True:
                    resultsObj = {
                        "id": thing.id,
                        "losssubcategory": thing.losssubcategory,
                        "description": thing.description,
                        "status": True,
                        "losscategory": losscategory.query.filter(losscategory.id == thing.losscategory,
                                                                  losscategory.status == True).value('losscategory')
                    }
                    results.append(resultsObj)
        return jsonify(results)


@loss_api.route('/loss-sub-category/<id>', methods=['GET', 'PUT'])
def losssubcategoryUpdate(id):
    from models import  losscategory,losssubcategory,adminlog
    from app import db
    now = datetime.now()
    losssubcategoryById = losssubcategory.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id": losssubcategoryById.id,
            "losssubcategory": losssubcategoryById.losssubcategory,
            "description": losssubcategoryById.description,
            "status": losssubcategoryById.status,
            "losscategory": losscategory.query.filter(losscategory.id == losssubcategoryById.losscategory,
                                                      losscategory.status == True).value('losscategory')
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        losssubcategory_old = losssubcategory.query.filter(losssubcategory.losssubcategory == data['losssubcategory'], losssubcategory.status == True).first()
        if losssubcategory_old:
            if int(losssubcategory_old.id) != int(id):
                data = {"message": f"This loss subcategory name already exists"}
                return jsonify(data), 500
        losssubcategoryById.losssubcategory = data['losssubcategory']
        losssubcategoryById.description = data['description']
        losssubcategoryById.losscategory = losscategory.query.filter(losscategory.losscategory == data['losscategory'],
                                                                     losscategory.status == True).value('id')

        db.session.add(losssubcategoryById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = data['logger'] , module = 'loss subcategory', activitydone = 'update', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Loss subcategory updated successfully"}
        return jsonify(data), 200

@loss_api.route('/loss-sub-category/<id>/<logger>', methods=['DELETE'])
def losssubcategoryDelete(id, logger):
    from models import  losscategory,losssubcategory,adminlog
    from app import db
    now = datetime.now()
    losssubcategoryById = losssubcategory.query.get_or_404(id)

    if request.method == 'DELETE':

        db.session.delete(losssubcategoryById)
        db.session.commit()

        adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'loss subcategory', activitydone = 'delete', activityid = id)
        db.session.add(adminlogObj)
        db.session.commit()

        data = {"message": f"Loss subcategory deleted successfully"}
        return jsonify(data), 200


@loss_api.route('/loss-sub-category-by-losscategory/<losscategoryid>', methods=['GET'])
def losssubcategoryBylosssCategory(losscategoryid):
    from models import losscategory, losssubcategory
    from app import db
    if request.method == 'GET':
        losscategoryById = losscategory.query.get_or_404(losscategoryid)
        losssubcategory_list = losssubcategory.query.filter(losssubcategory.losscategory == losscategoryid,
                                                            losssubcategory.status == True)
        response = []
        for losssubcategoryObj in losssubcategory_list:
            data = {
                "id": losssubcategoryObj.id,
                "losssubcategory": losssubcategoryObj.losssubcategory,
                "description": losssubcategoryObj.description,
                "status": losssubcategoryObj.status,
                "losscategory": losscategory.query.filter(losscategory.id == losscategoryid,
                                                          losscategory.status == True).value('losscategory')
            }
            response.append(data)
        return jsonify(response), 200


@loss_api.route('/loss-analysis-current-day', methods=['GET'])
def getLossAnalysisCurrentDay():
    from models import losscategory, losssubcategory,lossanalysis,asset,assetcategory,shift
    if request.method == 'GET':
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")
        curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        lossanalysis_data = lossanalysis.query.filter(lossanalysis.status == True).all()
        if len(lossanalysis_data) > 0:
            lossanalysis_data.reverse()
            response_list = []
            for lossanalysisObj in lossanalysis_data:
                lossanalysisDate_str = (lossanalysisObj.createdon).strftime("%Y-%m-%d")
                lossanalysisDate = datetime.strptime(lossanalysisDate_str, '%Y-%m-%d')
                if lossanalysisDate == curerntDate:
                    response_data = {
                        'id': lossanalysisObj.id,
                        'assetcategory': assetcategory.query.filter(assetcategory.id == lossanalysisObj.assetcategory,
                                                                    assetcategory.status == True).value('name'),
                        'asset': asset.query.filter(asset.id == lossanalysisObj.asset,
                                                    asset.assetcategory == lossanalysisObj.assetcategory,
                                                    asset.status == True).value('name'),
                        'losscategory': losscategory.query.filter(losscategory.id == lossanalysisObj.losscategory,
                                                                losscategory.status == True).value('losscategory'),
                        'losssubcategory': losssubcategory.query.filter(
                            losssubcategory.id == lossanalysisObj.losssubcategory,
                            losssubcategory.losscategory == lossanalysisObj.losscategory,
                            losssubcategory.status == True).value('losssubcategory'),
                        'shift': shift.query.filter(shift.id == lossanalysisObj.shift, shift.status == True).value('name'),
                        'fromtime': lossanalysisObj.fromtime.strftime("%H:%M:%S"),
                        'totime': lossanalysisObj.totime.strftime("%H:%M:%S"),
                        'losstime': lossanalysisObj.losstime,
                        'createdon': lossanalysisObj.createdon.strftime("%d-%m-%Y %H:%M:%S"),
                        'status': lossanalysisObj.status
                    }
                    response_list.append(response_data)
            
        if len(response_list) > 0:
            return jsonify(response_list)
        else:
            data = {"message": f"There is no loss for current day."}
            return jsonify(data), 500


@loss_api.route('/loss-analysis-by-shift-date-for-total-time', methods=['POST'])
def getLossAnalysisShiftDateTotalTime():
    from models import shift,lossanalysis
    from app import db
    if request.method == 'POST':
        data = request.get_json()
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")        
        if data['filterdate'] is None:
            curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        else:
            curerntDate = datetime.strptime(str(data['filterdate']), '%Y-%m-%d')
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        totalRunTime = 0
        totalLossTime = 0
        totalTimeStr = str(datetime.combine(date.min, shiftObj.endtime) - datetime.combine(date.min, shiftObj.starttime))
        t = totalTimeStr.split(':')
        totalTime = int(t[0]) * 60 + int(t[1]) * 1 + int(t[2]) / 60
        lossanalysis_data = lossanalysis.query.filter(lossanalysis.shift == shiftObj.id, lossanalysis.status == True ).all()
        for lossanalysisObj in lossanalysis_data:
            lossanalysisDate_str = (lossanalysisObj.createdon).strftime("%Y-%m-%d")
            lossanalysisDate = datetime.strptime(lossanalysisDate_str, '%Y-%m-%d')
            if lossanalysisDate == curerntDate:            
                totalLossTime = totalLossTime + lossanalysisObj.losstime
        totalRunTime = totalTime - totalLossTime
        response = {
            "totaltime": totalTime,
            "totalruntime": totalRunTime,
            "totallosstime": totalLossTime
        }
        return jsonify(response), 200


@loss_api.route('/loss-analysis-by-shift-date-for-category-loss-time', methods=['POST'])
def getLossAnalysisCurrentMonthForCategoryLossTime():
    from models import shift,lossanalysis,losscategory
    from app import db
    if request.method == 'POST':        
        data = request.get_json()
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")        
        if data['filterdate'] is None:
            curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        else:
            curerntDate = datetime.strptime(str(data['filterdate']), '%Y-%m-%d')
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        losscategory_list = losscategory.query.all()
        lossanalysis_list = lossanalysis.query.filter(lossanalysis.shift == shiftObj.id,
                                                      lossanalysis.status == True).all()
        response_data = []
        for losscategory_Obj in losscategory_list:
            totalCategoryLossTime = 0
            losscategoryObj = None
            for lossanalysisObj in lossanalysis_list:
                lossanalysisDate_str = (lossanalysisObj.createdon).strftime("%Y-%m-%d")
                lossanalysisDate = datetime.strptime(lossanalysisDate_str, '%Y-%m-%d')                
                if lossanalysisDate == curerntDate:
                    if lossanalysisObj.losscategory == losscategory_Obj.id:
                        totalCategoryLossTime = totalCategoryLossTime + lossanalysisObj.losstime
                        losscategoryObj = losscategory_Obj
            if losscategoryObj:
                dataObj = {
                    "losscategory": losscategoryObj.losscategory,
                    "totalCategoryLossTime": totalCategoryLossTime
                }
                response_data.append(dataObj)
        return jsonify(response_data), 200


@loss_api.route('/loss-analysis-by-shift-date-for-subcategory-loss-time', methods=['POST'])
def getLossAnalysisByShiftByDateBySubcategory():
    from models import losscategory, losssubcategory,shift,lossanalysis
    if request.method == 'POST':
        data = request.get_json()
        now = datetime.now()
        curerntDate_str = now.strftime("%Y-%m-%d")
        if data['filterdate'] is None:
            curerntDate = datetime.strptime(curerntDate_str, '%Y-%m-%d')
        else :
            curerntDate = datetime.strptime(str(data['filterdate']), '%Y-%m-%d')
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        losscategoryObj = losscategory.query.filter(losscategory.losscategory == data['losscategory'],
                                                    losscategory.status == True).first()
        losssubcategory_list = losssubcategory.query.filter(losssubcategory.losscategory == losscategoryObj.id,
                                                            losssubcategory.status == True).all()
        lossanalysis_list = lossanalysis.query.filter(lossanalysis.shift == shiftObj.id,
                                                      lossanalysis.status == True).all()
        response = []
        for losssubcategory_Obj in losssubcategory_list:
            totalSubCategoryTime = 0
            losssubcategoryObj = None
            for lossanalysisObj in lossanalysis_list:
                lossanalysisDate_str = (lossanalysisObj.createdon).strftime("%Y-%m-%d")
                lossanalysisDate = datetime.strptime(lossanalysisDate_str, '%Y-%m-%d')
                if lossanalysisDate == curerntDate:
                    if lossanalysisObj.losssubcategory == losssubcategory_Obj.id:
                        totalSubCategoryTime = totalSubCategoryTime + lossanalysisObj.losstime
                        losssubcategoryObj = losssubcategory_Obj
            if losssubcategoryObj:
                data = {
                    "losssubcategory": losssubcategoryObj.losssubcategory,
                    "totalsubcategorylosstime": totalSubCategoryTime
                }
                response.append(data)
        return jsonify(response), 200


@loss_api.route('/loss-analysis', methods=['POST'])
def saveLossAnalysis():
    from models import losscategory, losssubcategory,shift,lossanalysis,assetcategory,asset
    from app import db
    if request.method == 'POST':
        now = datetime.now()
        curerntDate = now.strftime("%d/%m/%Y")
        data = request.get_json()
        shiftObj = shift.query.filter(shift.name == data['shift'], shift.status == True).first()
        assetcategoryObj = assetcategory.query.filter(assetcategory.name == data['assetcategory'],
                                                      assetcategory.status == True).first()
        assetObj = asset.query.filter(asset.name == data['asset'], asset.status == True).first()
        losscategoryObj = losscategory.query.filter(losscategory.losscategory == data['losscategory'],
                                                    losscategory.status == True).first()
        losssubcategoryObj = losssubcategory.query.filter(losssubcategory.losssubcategory == data['losssubcategory'],
                                                          losssubcategory.status == True).first()
        lossanalysis_list = lossanalysis.query.filter(lossanalysis.assetcategory == assetcategoryObj.id,
                                                      lossanalysis.asset == assetObj.id,
                                                      lossanalysis.shift == shiftObj.id,
                                                      lossanalysis.status == True).all()
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
        elif (data['fromtime'] >= shiftObj.starttime.strftime("%H:%M:%S")) == True and (
                data['totime'] <= shiftObj.endtime.strftime("%H:%M:%S")) == True:
            if startTime != 0 and endTime != 0:
                if (data['fromtime'] < endTime.strftime("%H:%M:%S")) == True:
                    data = {"message": f"Loss already present for this time range."}
                    return jsonify(data), 500
                else:
                    losstimeStr = str(
                        datetime.strptime(data['totime'], '%H:%M:%S') - datetime.strptime(data['fromtime'], '%H:%M:%S'))
                    t = losstimeStr.split(':')
                    losstime = int(t[0]) * 60 + int(t[1]) * 1 + int(t[2]) / 60
                    lossanalysisObj = lossanalysis(assetcategory=assetcategoryObj.id, asset=assetObj.id,
                                                   losscategory=losscategoryObj.id,
                                                   losssubcategory=losssubcategoryObj.id, shift=shiftObj.id,
                                                   fromtime=data['fromtime'], totime=data['totime'], losstime=losstime,
                                                   createdon=now, status=True)
                    db.session.add(lossanalysisObj)
                    db.session.commit()
            else:
                losstimeStr = str(
                    datetime.strptime(data['totime'], '%H:%M:%S') - datetime.strptime(data['fromtime'], '%H:%M:%S'))
                t = losstimeStr.split(':')
                losstime = int(t[0]) * 60 + int(t[1]) * 1 + int(t[2]) / 60
                lossanalysisObj = lossanalysis(assetcategory=assetcategoryObj.id, asset=assetObj.id,
                                               losscategory=losscategoryObj.id, losssubcategory=losssubcategoryObj.id,
                                               shift=shiftObj.id, fromtime=data['fromtime'], totime=data['totime'],
                                               losstime=losstime, createdon=now, status=True)
                db.session.add(lossanalysisObj)
                db.session.commit()
        else:
            data = {"message": f"Please enter time between current shift time range."}
            return jsonify(data), 500
        data = {"message": f"Loss saved successfully."}
        return jsonify(data), 200