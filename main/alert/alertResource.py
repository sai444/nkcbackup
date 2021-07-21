import codecs
import csv
from datetime import datetime, timedelta, date

from flask import Blueprint, request, jsonify

alert_api = Blueprint('alert_api', __name__)

def createAlert():
    from app import influxdb
    from models import alarmconfiguration
    getTabes = "show measurements"
    result = influxdb.query(getTabes)
    points = list(result.get_points())
    for table in points:
        dataQuery = 'SELECT * FROM %s ORDER BY time DESC LIMIT 1'
        result = influxdb.query((dataQuery) % (table['name'],))
        points = list(result.get_points())
        assetLiveData = points[0]
        assetId = assetLiveData["asset_id"]
        alarmRules = alarmconfiguration.query.filter(alarmconfiguration.asset == assetId,
                                                     alarmconfiguration.status == True).value('all')

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
            currentValue = float(assetLiveData["power_line1_value"]) / 1000
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "POWER_LINE_2":
            currentValue = float(assetLiveData["power_line2_value"]) / 1000
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "POWER_LINE_3":
            currentValue = float(assetLiveData["power_line3_value"]) / 1000
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "MOTOR_VIBRATION_X_AXIS":
            currentValue = float(assetLiveData["motor_vibration_x_axis"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "MOTOR_VIBRATION_Z_AXIS":
            currentValue = float(assetLiveData["motor_vibration_z_axis"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "MAST_VIBRATION_X_AXIS":
            currentValue = float(assetLiveData["mast_vibration_x_axis"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "MAST_VIBRATION_Z_AXIS":
            currentValue = float(assetLiveData["mast_vibration_z_axis"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "VOLTAGE_LINE_1":
            currentValue = float(assetLiveData["voltage_line1_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "VOLTAGE_LINE_2":
            currentValue = float(assetLiveData["voltage_line2_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "VOLTAGE_LINE_3":
            currentValue = float(assetLiveData["voltage_line3_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "CURRENT_LINE_1":
            currentValue = float(assetLiveData["current_line1_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "CURRENT_LINE_2":
            currentValue = float(assetLiveData["current_line2_value"])
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "CURRENT_LINE_3":
            currentValue = float(assetLiveData["current_line3_value"])
            oldAlertVerification(assetLiveData, alarm, currentValue)

        if alarm.alertsubcategory == "FREQUENCY_LINE_1":
            currentValue = float(assetLiveData["frequency_line1_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "FREQUENCY_LINE_2":
            currentValue = float(assetLiveData["frequency_line2_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "FREQUENCY_LINE_3":
            currentValue = float(assetLiveData["frequency_line3_value"]) / 10
            oldAlertVerification(assetLiveData, alarm, currentValue)
        if alarm.alertsubcategory == "TEMPERATURE":
            currentValue = float(assetLiveData["temperature_value"]) / 100
            oldAlertVerification(assetLiveData, alarm, currentValue)


def oldAlertVerification(assetLiveData, alarm, currentValue):
    from models import alert
    now = datetime.now()
    assetId = assetLiveData["asset_id"]
    alert_sub_category = alarm.alertsubcategory
    # currentHr = now.strftime("%d/%m/%Y %H:%M:%S")
    # latestAretHr = str(int(alertLatest[7].strftime("%H")) + 2)
    alertlist = alert.query.filter(alert.asset == assetId, alert.alertsubcategory == alert_sub_category)
    for alertObj in alertlist:
        alertLatest = alertObj
    if alertLatest:
        latestAretHr = alertLatest.triggeredon + timedelta(hours=2)
        if now > latestAretHr:
            calculateAlert(assetLiveData, alarm, currentValue)
        else:
            print("***************Alerm already exit***************")


def calculateAlert(assetLiveData, alarm, currentValue):
    from models import alert
    from app import  db
    now = datetime.now()
    if alarm.alertlimittype == "Greater_Than":
        if currentValue > alarm.trackvalue:
            alert = alert(assetcategory=alarm[10], asset=alarm[9], alertsubcategory=alarm[4], alertlimittype=alarm[3],
                          trackvalue=currentValue, alarm=alarm[1], alertstatus=True, triggeredon=now)
            db.session.add(alert)
            db.session.commit()
    elif alarm.alertlimittype == "Less_Than":
        if currentValue < alarm.trackvalue:
            alert = alert(assetcategory=alarm[10], asset=alarm[9], alertsubcategory=alarm[4], alertlimittype=alarm[3],
                          trackvalue=currentValue, alarm=alarm[1], alertstatus=True, triggeredon=now)
            db.session.add(alert)
            db.session.commit()
    elif alarm.alertlimittype == "Equal_To":
        if currentValue == alarm.trackvalue:
            alert = alert(assetcategory=alarm[10], asset=alarm[9], alertsubcategory=alarm[4], alertlimittype=alarm[3],
                          trackValue=currentValue, alarm=alarm[1], alertstatus=True, triggeredon=now)
            db.session.add(alert)
            db.session.commit()


@alert_api.route('/alert-current-day', methods=['GET'])
def alertForCurrentDay():
    from models import alert,assetcategory,asset
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
                    "id": alertObj.id,
                    "assetcategory": assetcategory.query.filter(assetcategory.id == alertObj.assetcategory).value(
                        "name"),
                    "asset": asset.query.filter(asset.id == alertObj.asset).value("name"),
                    "alertsubcategory": alertObj.alertsubcategory,
                    "alertlimittype": alertObj.alertlimittype,
                    "trackvalue": alertObj.trackvalue,
                    "alarm": alertObj.alarm,
                    "alertstatus": alertObj.alertstatus,
                    "triggeredon": alertObj.triggeredon
                }
                alert_response.append(data)
        if len(alert_response) < 1:
            data = {"message": f"There is no Alert."}
            return jsonify(data), 500
        alert_response.reverse()
        return jsonify(alert_response), 200


@alert_api.route('/alert-assetcategory-asset', methods=['POST'])
def alertbycategoryAndAssetForCurrentMonth():
    from models import assetcategory,alert,asset
    if request.method == 'POST':
        data = request.get_json()
        now = datetime.now()
        currentMonth = now.strftime("%m")
        currentYear = now.strftime("%Y")
        alert_response = []
        assetCategoryId = assetcategory.query.filter(assetcategory.name == data['assetcategory'],
                                                     assetcategory.status == True).value("id")
        assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value("id")
        alerts = alert.query.filter(alert.assetcategory == assetCategoryId, alert.asset == assetId,
                                    alert.alertstatus == True)
        for alertObj in alerts:
            alertMonth = (alertObj.triggeredon).strftime("%m")
            alertYear = (alertObj.triggeredon).strftime("%Y")
            if alertMonth == currentMonth and alertYear == currentYear:
                response = {
                    "id": alertObj.id,
                    "assetcategory": assetcategory.query.filter(assetcategory.id == alertObj.assetcategory).value(
                        "name"),
                    "asset": asset.query.filter(asset.id == alertObj.asset).value("name"),
                    "alertsubcategory": alertObj.alertsubcategory,
                    "alertlimittype": alertObj.alertlimittype,
                    "trackvalue": alertObj.trackvalue,
                    "alarm": alertObj.alarm,
                    "alertstatus": alertObj.alertstatus,
                    "triggeredon": alertObj.triggeredon
                }
                alert_response.append(response)
        if len(alert_response) < 1:
            data_error = {"message": f"There is no Alert."}
            return jsonify(data_error), 500
        alert_response.reverse()
        return jsonify(alert_response), 200


@alert_api.route('/alarm-configuration-import', methods=['POST'])
def upload_alertrule():
    # data = request.get_json()
    flask_file = request.files['file']
    if not flask_file:
        return 'Upload a CSV file'
    # filename = flask_file.filename

    stream = codecs.iterdecode(flask_file.stream, 'utf-8')
    csv_test = csv.reader(stream, dialect=csv.excel)
    alarm_response = []
    rowNo = 0
    for row in csv_test:
        if row:
            if rowNo > 0:
                excelRowFieldValidaton(row, rowNo)
                response_data = {
                    # 'assetcategory': assetcategory.query.filter(assetcategory.name == data['assetcategory'], assetcategory.status == True).value("id"),
                    # 'asset': asset.query.filter(asset.name == data['asset'], asset.status == True).value("id"),
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


@alert_api.route('/alarm-configuration-save-import', methods=['POST', 'GET'])
def save_alertrule():
    from models import companylocation,asset,assetcategory,alarmconfiguration
    from app import db
    if request.method == 'POST':
        if request.is_json:
            now = datetime.now()
            data = request.get_json()
            for dataObj in data:
                companylocationId = companylocation.query.filter(companylocation.location == dataObj['companylocation'],
                                                                 companylocation.status == True).value("id")
                assetcategoryId = assetcategory.query.filter(assetcategory.name == dataObj['assetcategory'],
                                                             assetcategory.status == True).value("id")
                assetId = asset.query.filter(asset.name == dataObj['asset'], asset.assetcategory == assetcategoryId,
                                             asset.status == True).value("id")

                alarmconfiguration_save = alarmconfiguration(companylocation=companylocationId,
                                                             assetcategory=assetcategoryId, asset=assetId,
                                                             alertsubcategory=dataObj['alertsubcategory'],
                                                             alertlimittype=dataObj['alertlimittype'],
                                                             configvalue=dataObj['configvalue'], alarm=dataObj['alarm'],
                                                             severity=dataObj['severity'], createdon=now, status=True)
                db.session.add(alarmconfiguration_save)
                db.session.commit()
                data = {"message": f"Alert rule created successfully"}
                return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}
