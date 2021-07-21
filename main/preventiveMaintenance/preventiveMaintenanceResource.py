import codecs
import csv
from datetime import datetime

from flask import Blueprint, request, jsonify

pm_api = Blueprint('pm_api', __name__)

@pm_api.route('/duration-type', methods=['POST', 'GET'])
def durationTypeSave():
    from models import durationtype
    from app import db
    if request.method == 'POST':
        data = request.get_json()
        durationtype_old = durationtype.query.filter(durationtype.durationtype == data['durationtype'],
                                                     durationtype.status == True).first()
        if durationtype_old:
            data = {"message": f"This duration type already exit."}
            return jsonify(data), 500
        duration_type = durationtype(durationtype=data['durationtype'], lowlimit=data['lowlimit'],
                                     highlimit=data['highlimit'], status=True)

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
                        "id": thing.id,
                        "durationtype": thing.durationtype,
                        "lowlimit": thing.lowlimit,
                        "highlimit": thing.highlimit,
                        "status": thing.status
                    }
                    results.append(resultsObj)
        return jsonify(results)


@pm_api.route('/duration-type/<id>', methods=['GET', 'PUT', 'DELETE'])
def durationTypeUpdate(id):
    from models import durationtype
    from app import db
    durationTypeById = durationtype.query.get_or_404(id)

    if request.method == 'GET':
        response = {
            "id": durationTypeById.id,
            "durationtype": durationTypeById.durationtype,
            "lowlimit": durationTypeById.lowlimit,
            "highlimit": durationTypeById.highlimit,
            "status": durationTypeById.status
        }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        durationtype_old = durationtype.query.filter(durationtype.durationtype == data['durationtype'],
                                                     durationtype.status == True).first()
        if durationtype_old:
            if int(durationtype_old.id) != int(id):
                data = {"message": f"This duration type already exit."}
                return jsonify(data), 500
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


@pm_api.route('/checklist-assigned', methods=['PUT'])
def checklistOk():
    from models import checklist
    from app import db
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


@pm_api.route('/preventive-maintenance-submit', methods=['PUT'])
def preventiveMaintenanceSubmit():
    from models import preventivemaintenance
    from app import db
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
            preventivemaintenanceById.submittedbysupervisor = False

            db.session.add(preventivemaintenanceById)
            db.session.commit()

            data = {"message": f"Submitted successfully"}
            return jsonify(data), 200


@pm_api.route('/preventive-maintenance-by-assetcategory-asset-duration', methods=['POST'])
def preventiveMaintenanceGet():
    from models import preventivemaintenance,asset,assetcategory,durationtype,preventivemaintenance_checklist,checklist
    if request.method == 'POST':
        data = request.get_json()
        assetCategoryId = assetcategory.query.filter(assetcategory.name == data['assetcategory'],
                                                     assetcategory.status == True).value('id')
        assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value('id')
        durationTypeId = durationtype.query.filter(durationtype.durationtype == data['durationtype'],
                                                   durationtype.status == True).value('id')

        preventivemaintenancelist = preventivemaintenance.query.filter(
            preventivemaintenance.assetcategory == assetCategoryId, preventivemaintenance.asset == assetId,
            preventivemaintenance.durationtype == durationTypeId,
            preventivemaintenance.durationvalue == data['durationvalue'])
        if preventivemaintenancelist:
            # preventivemaintenancelist.reverse()
            for preventivemaintenance_Obj in preventivemaintenancelist:
                preventivemaintenanceObj = preventivemaintenance_Obj
            checklistmapp_list = preventivemaintenance_checklist.query.filter(
                preventivemaintenance_checklist.preventivemaintenance == preventivemaintenanceObj.id)
            checklist_list = []
            for checklistObj in checklistmapp_list:
                checklists = checklist.query.filter(checklist.id == checklistObj.checklist).first()
                checklist_list.append(checklists)
            data = {
                "id": preventivemaintenanceObj.id,
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
                } for checklist in checklist_list]
            }

            return jsonify(data)
        else:
            data = {"message": f"There no maintenance present."}
            return jsonify(data), 500


# @sched.scheduled_job('cron', id='preventive_maintenance', hour=0, minute=0)
def preventiveMaintenanceScheduler():
        print("*************************************PM Scheduler********************************")
        from models import preventivemaintenancemaster, preventivemaintenance, durationtype

        now = datetime.now()
        #currentday = now.strftime("%d/%m/%Y %H:%M:%S")
        #latestAretHr = str(int(alertLatest[7].strftime("%H")) + 2)
        currentDay = int(now.strftime("%d"))
        currentMonth = int(now.strftime("%m"))
        currentYear = int(now.strftime("%Y"))


        preventivemaintenancemaster_list = preventivemaintenancemaster.query.all()
        for preventivemaintenancemasterObj in preventivemaintenancemaster_list:
            preventivemaintenance_list = preventivemaintenance.query.filter(preventivemaintenance.assetcategory == preventivemaintenancemasterObj.assetcategory, preventivemaintenance.asset == preventivemaintenancemasterObj.asset, preventivemaintenance.durationtype == preventivemaintenancemasterObj.durationtype,preventivemaintenance.durationvalue == preventivemaintenancemasterObj.durationvalue).all()
            for preventivemaintenance_Obj in preventivemaintenance_list:
                preventivemaintenanceObj = preventivemaintenance_Obj
            if preventivemaintenance_list:
                durationtypeObj = durationtype.query.filter(durationtype.id == preventivemaintenancemasterObj.durationtype, durationtype.status ==True).first()
                if durationtypeObj.durationtype == "Day":
                    assignedon = int(preventivemaintenanceObj.assignedon.strftime("%d"))
                    if (currentDay - assignedon) == preventivemaintenancemasterObj.durationvalue:
                        if preventivemaintenanceObj.submittedby is None:
                            submitAllCheckList(preventivemaintenanceObj)
                        bindAllCheckList(preventivemaintenancemasterObj.id)
                if durationtypeObj.durationtype == "Week":
                    currentWeek = int((now.day - 1) // 7 + 1)
                    assignedWeek = int((preventivemaintenanceObj.assignedon.day - 1) // 7 + 1)
                    if (currentWeek - assignedWeek) == preventivemaintenancemasterObj.durationvalue:
                        if preventivemaintenanceObj.submittedby is None:
                            submitAllCheckList(preventivemaintenanceObj)
                        bindAllCheckList(preventivemaintenancemasterObj.id)
                if durationtypeObj.durationtype == "Month":
                    assignedMonth = int(preventivemaintenanceObj.assignedon.strftime("%m"))
                    if (currentMonth - assignedMonth) == preventivemaintenancemasterObj.durationvalue:
                        if preventivemaintenanceObj.submittedby is None:
                            submitAllCheckList(preventivemaintenanceObj)
                        bindAllCheckList(preventivemaintenancemasterObj.id)
                if durationtypeObj.durationtype == "Year":
                    assignedYear = int(preventivemaintenanceObj.assignedon.strftime("%y"))
                    if (currentYear - assignedYear) == preventivemaintenancemasterObj.durationvalue:
                        if preventivemaintenanceObj.submittedby is None:
                            submitAllCheckList(preventivemaintenanceObj)
                        bindAllCheckList(preventivemaintenancemasterObj.id)
            else:
                bindAllCheckList(0)
        return '', 204

def bindAllCheckList(preventivemaintenancemasterId):
    from models import preventivemaintenancemaster, preventivemaintenance,preventivemaintenancemaster_checklistmaster,checklist
    from models import preventivemaintenance_checklist,checklistmaster
    from app import db
    now = datetime.now()
    currentYear = now.strftime("%Y")
    preventivemaintenancemaster_list = []
    if preventivemaintenancemasterId > 0:
        preventivemaintenancemaster_Obj = preventivemaintenancemaster.query.get_or_404(preventivemaintenancemasterId)
        preventivemaintenancemaster_list.append(preventivemaintenancemaster_Obj)
    else:
        preventivemaintenancemaster_list = preventivemaintenancemaster.query.all()
    for preventivemaintenancemasterObj in preventivemaintenancemaster_list:
        checklistmaster_list = preventivemaintenancemaster_checklistmaster.query.filter(preventivemaintenancemaster_checklistmaster.preventivemaintenancemaster == preventivemaintenancemasterObj.id).all()
        if checklistmaster_list:
            checklistmaster_data = []
            for checklistmasterObj in checklistmaster_list:
                checklistmaster_Obj = checklistmaster.query.filter(checklistmaster.id == checklistmasterObj.checklistmaster).first()
                checklistmaster_data.append(checklistmaster_Obj)
            preventivemaintenance_data = preventivemaintenance(assetcategory = preventivemaintenancemasterObj.assetcategory,asset = preventivemaintenancemasterObj.asset, durationtype = preventivemaintenancemasterObj.durationtype, durationvalue = preventivemaintenancemasterObj.durationvalue, submittedyear = currentYear, assignedon = now, allchecklistcompleted = None, submittedon = None, submittedby = None, isautosubmit = None, submittedbysupervisor = None)
            db.session.add(preventivemaintenance_data)
            db.session.commit()

            #checklist_assigned = []
            for checklistmaster_data_Obj in checklistmaster_data:
                checklist_data = checklist(checkpart = checklistmaster_data_Obj.checkpart, checkpoint = checklistmaster_data_Obj.checkpoint,description = checklistmaster_data_Obj.description,standardvalue = checklistmaster_data_Obj.standardvalue, status = True, checkpointstatus = None, remark = None, submittedon = None, submittedby = None)
                db.session.add(checklist_data)
                db.session.commit()

                preventivemaintenance_checklistObj = preventivemaintenance_checklist(preventivemaintenance = preventivemaintenance_data.id, checklist = checklist_data.id)
                db.session.add(preventivemaintenance_checklistObj)
                db.session.commit()

def submitAllCheckList(preventivemaintenanceObj):
    from models import preventivemaintenancemaster, preventivemaintenance, preventivemaintenancemaster_checklistmaster,checklist
    from models import preventivemaintenance_checklist, checklistmaster
    from app import db
    now = datetime.now()
    checkpontsNoDone = 0
    preventivemaintenance_checklist_list = preventivemaintenance_checklist.query.filter(preventivemaintenance_checklist.preventivemaintenance == preventivemaintenanceObj.id).all()
    for preventivemaintenance_checklist_Obj in preventivemaintenance_checklist_list:
        checklist_status = checklist.query.filter(checklist.id == preventivemaintenance_checklist_Obj.checklist).value('checkpointstatus')
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


@pm_api.route('/preventive-maintenance-import', methods=['POST'])
def upload_preventiveMaintenance():
    if request.method == 'POST':
        data = request.get_json()
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

@pm_api.route('/preventive-maintenance-save-import/<logger>', methods=['POST'])
def save_preventiveMaintenance(logger):
    from models import preventivemaintenancemaster, asset,assetcategory,durationtype,checklistmaster,preventivemaintenancemaster_checklistmaster,adminlog
    from app import db
    if request.method == 'POST':
        now = datetime.now()
        if request.is_json:
            data = request.get_json()
            dataResp = {"message": f" "}
            for dataObj in data:
                assetcategoryId = assetcategory.query.filter(assetcategory.name == dataObj['assetcategory'],
                                                             assetcategory.status == True).value("id")
                assetId = asset.query.filter(asset.name == dataObj['asset'], asset.assetcategory == assetcategoryId,
                                             asset.status == True).value("id")
                durationtypeId = durationtype.query.filter(durationtype.durationtype == dataObj['durationtype'],
                                                           durationtype.status == True).value("id")
                preventivemaintenancemaster_save = preventivemaintenancemaster(assetcategory=assetcategoryId,
                                                                               asset=assetId,
                                                                               durationtype=durationtypeId,
                                                                               durationvalue=dataObj['durationvalue'],
                                                                               uploadedby=dataObj['uploadedby'],
                                                                               createdon=now, lastupdatedon=now)
                db.session.add(preventivemaintenancemaster_save)
                db.session.commit()

                checkListMasters = []
                checklistmaster_list = dataObj['checklistmaster']
                for checklistmasterObj in checklistmaster_list:
                    checklistmaster_save = checklistmaster(checkpart=checklistmasterObj['checkpart'],
                                                           checkpoint=checklistmasterObj['checkpoint'],
                                                           description=checklistmasterObj['description'],
                                                           standardvalue=checklistmasterObj['standardvalue'],
                                                           status=True, createdon=now, updatedon=now)
                    db.session.add(checklistmaster_save)
                    db.session.commit()

                    preventivemaintenancemaster_checklistmaster_save = preventivemaintenancemaster_checklistmaster(
                        preventivemaintenancemaster=preventivemaintenancemaster_save.id,
                        checklistmaster=checklistmaster_save.id)
                    db.session.add(preventivemaintenancemaster_checklistmaster_save)
                    db.session.commit()

                adminlogObj = adminlog(loggedon = now, loggedby = logger , module = 'Preventive Maintenance', activitydone = 'save', activityid = preventivemaintenancemaster_save.id)
                db.session.add(adminlogObj)
                db.session.commit()
                dataResp = {"message": f"Preventive maintenance created successfully"}
            return jsonify(dataResp), 200
        else:
            return {"error": "The request payload is not in JSON format"}

@pm_api.route('/preventive-maintenance-first-sheet-cloumn-export', methods = ['GET'])
def pmFirstSheetColumnNames():
    if request.method == 'GET':
        response_data = {
            'row0':'Check part',
            'row1':'Check point',
            'row2':'Description',
            'row3':'Standard value'
        }
        return jsonify(response_data), 200

@pm_api.route('/preventive-maintenance-master-by-assetcategory-asset', methods=['POST'])
def preventiveMaintenanceMastrerGetAll():
    from models import preventivemaintenancemaster,asset,assetcategory,durationtype,preventivemaintenancemaster_checklistmaster,checklistmaster
    if request.method == 'POST':
        data = request.get_json()

        assetCategoryId = assetcategory.query.filter(assetcategory.name == data['assetcategory'],
                                                     assetcategory.status == True).value('id')
        assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value('id')

        preventivemaintenancemaster_list = preventivemaintenancemaster.query.filter(preventivemaintenancemaster.assetcategory == assetCategoryId, preventivemaintenancemaster.asset == assetId).all()

        #preventivemaintenancemaster_list = preventivemaintenancemaster.query.all()
        if preventivemaintenancemaster_list:
            datalist = []
            preventivemaintenancemaster_list.reverse()
            for preventivemaintenanceObj in preventivemaintenancemaster_list:
                checklistmastermapp_list = preventivemaintenancemaster_checklistmaster.query.filter(
                    preventivemaintenancemaster_checklistmaster.preventivemaintenancemaster == preventivemaintenanceObj.id)
                checklist_list = []
                for checklistObj in checklistmastermapp_list:
                    checklistmasters = checklistmaster.query.filter(checklistmaster.id == checklistObj.checklistmaster).first()
                    checklist_list.append(checklistmasters)
                dataObj = {
                    "id": preventivemaintenanceObj.id,
                    "assetcategoryId": preventivemaintenanceObj.assetcategory,
                    "assetcategory": assetcategory.query.filter(assetcategory.id == preventivemaintenanceObj.assetcategory).value("name"),
                    "assetId": preventivemaintenanceObj.asset,
                    "asset": asset.query.filter(asset.id == preventivemaintenanceObj.asset).value("name"),
                    "durationtypeId": preventivemaintenanceObj.durationtype,
                    "durationtype": durationtype.query.filter(durationtype.id == preventivemaintenanceObj.durationtype).value("durationtype"),
                    "durationvalue": preventivemaintenanceObj.durationvalue,
                    "uploadedOn":preventivemaintenanceObj.createdon,
                    "checklist": [{
                        "id": checklist.id,
                        "checkpart": checklist.checkpart,
                        "checkpoint": checklist.checkpoint,
                        "description": checklist.description,
                        "standardvalue": checklist.standardvalue,
                        "status": checklist.status
                    } for checklist in checklist_list]
                    }
                datalist.append(dataObj)
            return jsonify(datalist)
        else:
            data = {"message": f"There no maintenance present."}
            return jsonify(data), 500
