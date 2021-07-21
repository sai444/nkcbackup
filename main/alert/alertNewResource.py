import codecs
import datetime
# from datetime import datetime, date, time, timedelta
from flask import Blueprint, request, jsonify
from sqlalchemy import Column, Integer, DateTime, desc, Date, cast
from _datetime import date
from datetime import datetime

alertnew_api = Blueprint('alertnew_api', __name__)

@alertnew_api.route('/sensordetails', methods=['POST', 'GET'])
def sensordetailss():
    from models import sensor,sensorval,sensoralerts,sensordetails
    from app import db
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            # sensorids = sensor.query.filter(sensor.name == data['sensorId']).value('id')
            new_car = sensordetails(sampleinterval = data['sampleinterval'],asset = data['asset'], assetcategory = data['assetcategory'],sensorid = data['sensorid'], medop = data['medop'], highop = data['highop'], alertstatus = '', alerttype = data['alerttype'], highrange = data['highrange'], lowop = data['lowop'], propertytype = '', midrange = data['midrange'],lowrange = data['lowrange'], units = '', description = data['description'], type = '', propertyid = '', thresholdvalue= '', msg = data['msg'], property = '', alarm = '', operator = data['operator'], realtimeval = data['realtimeval'])
            db.session.add(new_car)
            db.session.commit()
            data = {"message": f"car {new_car.id} has been created successfully."}
            return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = sensordetails.query.all()
        results = [
            {
                "id" : thing.id,
                "alarm" : thing.alarm,
                "asset" : thing.asset,
                "assetcategory" : thing.assetcategory,
                "operator" : thing.operator,
                "realtimeval" : thing.realtimeval,
                "thresholdvalue" : thing.thresholdvalue,
                "sensor" : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                "sensorid" : thing.sensorid,
                "msg" : thing.msg,
                "property" : thing.property,
                "units"  : thing.units,
                "description" : thing.description,
                # "type" : thing.type,
                "propertyid" : thing.propertyid,
                "propertytype" : thing.propertytype,
                "midrange" : thing.midrange,
                "lowrange" : thing.lowrange,
                "highrange" : thing.highrange,
                "lowop" : thing.lowop,
                "medop" : thing.medop,
                "highop" : thing.highop,
                "alertstatus" : thing.alertstatus,
                "alerttype" : thing.alerttype,
                "sampleinterval" : thing.sampleinterval
            } for thing in things]
        print("hello")
        return  jsonify(results)

@alertnew_api.route('/sensordetails/<id>', methods=['GET', 'PUT', 'DELETE'])
def sensordetailsss(id):
    from models import sensor,sensorval,sensoralerts,sensordetails
    from app import db
    thing = sensordetails.query.get_or_404(id)

    if request.method == 'GET':
        # thingz = sensordetails.query.filter(sensordetails.asset == id).value('id')
        things = sensordetails.query.filter(sensordetails.asset == id).all()
        response = [{
                "id" : thing.id,
                "alarm" : thing.alarm,
                "asset" : thing.asset,
                "assetcategory" : thing.assetcategory,
                "operator" : thing.operator,
                "realtimeval" : thing.realtimeval,
                "thresholdvalue" : thing.thresholdvalue,
                "sensorid" : thing.sensorid,
                "sensor" : sensor.query.filter(sensor.id == thing.sensorid).value('name'),				
                "msg" : thing.msg,
                "property" : thing.property,
                "units"  : thing.units,
                "description" : thing.description,
                "type" : thing.type,
                "propertyid" : thing.propertyid,
                "propertytype" : thing.propertytype,
                "midrange" : thing.midrange,
                "lowrange" : thing.lowrange,
                "highrange" : thing.highrange,
                "lowop" : thing.lowop,
                "medop" : thing.medop,
                "highop" : thing.highop,
                "alertstatus" : thing.alertstatus,
                "alerttype" : thing.alerttype,
                "sampleinterval" : thing.sampleinterval
            } for thing in things]
        return jsonify(response)
    elif request.method == 'PUT':
        data = request.get_json()
        thing.sensorid = data['sensorid']

        thing.operator = data['operator']
        thing.realtimeval = data['realtimeval']
        thing.thresholdvalue = ''
        thing.msg = data['msg']

        thing.description = data['description']
        thing.sampleinterval = data['sampleinterval']
        thing.midrange = data['midrange']
        thing.highrange = data['highrange']
        thing.lowrange = data['lowrange']
        thing.highop = data['highop']
        thing.medop = data['medop']
        thing.lowop = data['lowop']

        thing.asset = data['asset']
        thing.assetcatergory = data['assetcategory']
        thing.sampleinterval = data['sampleinterval']
        thing.alerttype = data['alerttype']
        db.session.add(thing)
        db.session.commit()
        data = {"message": f"car  has been updated successfully."}
        return jsonify(data), 200
        # return {"message": f"car {thing.id} successfully updated"}

    elif request.method == 'DELETE':
        thing = sensordetails.query.get_or_404(id)
        db.session.delete(thing)
        db.session.commit()
        data = {"message": f"car  has been deleted successfully."}
        return jsonify(data), 200
        # return {"message": f"Car {thing.id} successfully deleted."}


@alertnew_api.route('/sensoralerts', methods=['POST', 'GET'])
def sensoralertss():
    from models import sensor,sensorval,sensoralerts, asset
    from app import db
    from datetime import datetime
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            sensorids = sensor.query.filter(sensor.name == data['sensor']).value('id')
            now = datetime.now()
            new_car = sensoralerts(resolvedon = None, resolvedby = None,remarks = None, recommendation = None,created_on = now, sensorid = sensorids,property = data['property'],status = data['status'], severity = data['severity'], description = data['description'], alertname = data['alertname'], alertmsg = data['alertmsg'], alertval = data['alertval'])
            db.session.add(new_car)
            db.session.commit()
            data = {"message": f"car {new_car.id} has been created successfully."}
            return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        things = sensoralerts.query.all()
        results = [
            {
                'id' : thing.id,
                'sensor' : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                'alertname' : thing.alertname,
                'alertmsg' : thing.alertmsg,
                'alertval' : thing.alertval,
                'status' : thing.status,
                'severity' : thing.severity,
                'created_on' : thing.created_on,
                'description' : thing.description,
                'property' : thing.property,
                'resolvedon' : thing.resolvedon,
                'resolvedby' : thing.resolvedby,
                'remarks' : thing.remarks,
                'recommendation' : thing.recommendation,
                'asset' : asset.query.filter(asset.id == sensor.query.filter(sensor.id == thing.sensorid).value('asset_sensor_allocation_id')).value('name')
            } for thing in things]
        print("hello")
        return  jsonify(results)

@alertnew_api.route('/machinealertstoday', methods=['GET', 'PUT', 'DELETE'])
def sensoralerttodayssss():
    from models import sensor,sensorval,sensoralerts,asset
    from app import db
    things = sensoralerts.query.filter(cast(sensoralerts.created_on,Date) == date.today()).all()
    results = [
        {
                'id' : thing.id,
                'sensor' : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                'alertname' : thing.alertname,
                'alertmsg' : thing.alertmsg,
                'alertval' : thing.alertval,
                'status' : thing.status,
                'severity' : thing.severity,
                'created_on' : thing.created_on,
                'description' : thing.description,
                'property' : thing.property,
                'resolvedon' : thing.resolvedon,
                'resolvedby' : thing.resolvedby,
                'remarks' : thing.remarks,
                'recommendation' : thing.recommendation,
                'asset' : asset.query.filter(asset.id == sensor.query.filter(sensor.id == thing.sensorid).value('asset_sensor_allocation_id')).value('name')
            } for thing in things]
    print("hello")
    return  jsonify(results)

@alertnew_api.route('/machinealertsopen', methods=['GET', 'PUT', 'DELETE'])
def sensoralertopenssss():
    from models import sensor,sensorval,sensoralerts,asset
    from app import db
    things = sensoralerts.query.filter(sensoralerts.status == True).all()
    results = [
        {
                'id' : thing.id,
                'sensor' : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                'alertname' : thing.alertname,
                'alertmsg' : thing.alertmsg,
                'alertval' : thing.alertval,
                'status' : thing.status,
                'severity' : thing.severity,
                'created_on' : thing.created_on,
                'description' : thing.description,
                'property' : thing.property,
                'resolvedon' : thing.resolvedon,
                'resolvedby' : thing.resolvedby,
                'remarks' : thing.remarks,
                'recommendation' : thing.recommendation,
                'asset' : asset.query.filter(asset.id == sensor.query.filter(sensor.id == thing.sensorid).value('asset_sensor_allocation_id')).value('name')
            } for thing in things]
    print("hello")
    return  jsonify(results)

@alertnew_api.route('/machinealertsclose', methods=['GET', 'PUT', 'DELETE'])
def sensoralertclosessss():
    from models import sensor,sensorval,sensoralerts,asset
    from app import db
    things = sensoralerts.query.filter(sensoralerts.status == False).all()
    results = [
        {
                'id' : thing.id,
                'sensor' : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                'alertname' : thing.alertname,
                'alertmsg' : thing.alertmsg,
                'alertval' : thing.alertval,
                'status' : thing.status,
                'severity' : thing.severity,
                'created_on' : thing.created_on,
                'description' : thing.description,
                'property' : thing.property,
                'resolvedon' : thing.resolvedon,
                'resolvedby' : thing.resolvedby,
                'remarks' : thing.remarks,
                'recommendation' : thing.recommendation,
                'asset' : asset.query.filter(asset.id == sensor.query.filter(sensor.id == thing.sensorid).value('asset_sensor_allocation_id')).value('name')
            } for thing in things]
    print("hello")
    return  jsonify(results)

@alertnew_api.route('/alertcount', methods=['POST', 'GET'])
def alertcounts():
    from models import sensor,sensorval,sensoralerts,asset
    from app import db
    if request.method == 'GET':
        proactivecount = sensor.query.count()
        activecount = sensoralerts.query.filter(sensoralerts.status == True).count()
        deactivecount = sensoralerts.query.filter(sensoralerts.status == False).count()
        high = sensoralerts.query.filter(sensoralerts.status == True, sensoralerts.severity == 'High').count()
        today = sensoralerts.query.filter(cast(sensoralerts.created_on,Date) == date.today()).count()
        results = [
            {
                "active" : activecount,
                "deactive" : deactivecount,
                "high" : high,
                "today" : today,
                "proactivecount":proactivecount
            } ]
    return jsonify(results)

@alertnew_api.route('/sensoralerts/<id>', methods=['GET', 'PUT', 'DELETE'])
def sensoralertssss(id):
    from models import sensor,sensorval,sensoralerts,asset
    from app import db
    thing = sensoralerts.query.get_or_404(id)

    if request.method == 'GET':
        response = {
                'id' : thing.id,
                'sensor' : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                'alertname' : thing.alertname,
                'alertmsg' : thing.alertmsg,
                'alertval' : thing.alertval,
                'status' : thing.status,
                'severity' : thing.severity,
                'created_on' : thing.created_on,
                'description' : thing.description,
                'property' : thing.property,
                'resolvedon' : thing.resolvedon,
                'resolvedby' : thing.resolvedby,
                'remarks' : thing.remarks,
                'recommendation' : thing.recommendation,
                'asset' : asset.query.filter(asset.id == sensor.query.filter(sensor.id == thing.sensorid).value('asset_sensor_allocation_id')).value('name')
            }
        return jsonify(response)

    elif request.method == 'PUT':
        data = request.get_json()
        thing.sensor = sensor.query.filter(sensor.name == data['sensor']).value('id'),
        thing.alertname = data['alertname']
        thing.alertval = data['alertval']
        # thing.thresholdvalue = data['thresholdvalue']
        thing.status = data['status']
        thing.severity = data['severity']
        thing.resolvedon = datetime.now()
        thing.resolvedby = data['resolvedby']
        thing.property = data['property']
        thing.description = data['description']
        thing.remarks = data['remarks']
        thing.recommendation = data['recommendation']
        thing.alertmsg = data['alertmsg']
        db.session.add(thing)
        db.session.commit()
        data = {"message": f"car test  has been updated successfully."}
        return jsonify(data), 200
        # return {"message": f"car {thing.id} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(thing)
        db.session.commit()
        data = {"message": f"car  has been deleted successfully."}
        return jsonify(data), 200
        # return {"message": f"Car {thing.id} successfully deleted."}


@alertnew_api.route('/sensorval', methods=['POST', 'GET'])
def sensorvals():
    from models import sensor,sensorval,sensordetails
    from app import db
    if request.method == 'POST':
        if request.is_json:
            now = datetime.now()
            data = request.get_json()
            sensorids = sensor.query.filter(sensor.name == data['sensor']).value('id')
            new_car = sensorval(propertyid = None, created_on = now, sensorid = sensorids, property = '', units = data['units'], liveval = data['liveval'])
            db.session.add(new_car)
            db.session.commit()

            #update live val in sensor details table

            detailsid = sensordetails.query.filter(sensordetails.sensorid == sensorids).value('id')
            thing = sensordetails.query.get_or_404(detailsid)
            thing.liveval = data['liveval']
            db.session.add(thing)
            db.session.commit()

            #update alerts tables
            updatesensoralerts(sensorids,data['liveval'])

            data = {"message": f"car {new_car.id} has been created successfully."}
            return jsonify(data), 200
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        things = sensorval.query.all()
        results = [
            {
                "id" : thing.id,
                "sensor" : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                "units" : thing.units,
                "liveval" : thing.liveval,
                "created_on"  : thing.created_on,
                "propertyid" : thing.propertyid,
                "property"  : thing.property
            } for thing in things]
        print("hello")
        return  jsonify(results)

@alertnew_api.route('/sensorval/<id>', methods=['GET', 'PUT', 'DELETE'])
def sensorvalsss(id):
    from models import sensor,sensorval, sensordetails
    from app import db
    thing = sensorval.query.get_or_404(id)

    if request.method == 'GET':
        response = {
                "id" : thing.id,
                "sensor" : sensor.query.filter(sensor.id == thing.sensorid).value('name'),
                "units" : thing.units,
                "liveval" : thing.liveval,
                "created_on"  : thing.created_on,
                "propertyid" : thing.propertyid,
                "property"  : thing.property
            }
        return jsonify(response)
		
    elif request.method == 'PUT':
        data = request.get_json()
        thing.sensorid = sensor.query.filter(sensor.name == data['sensor']).value('id'),
        thing.units = data['units']
        thing.liveval = data['liveval']
        thing.created_on = datetime.datetime.now()
        thing.property = ''
        thing.propertyid = ''
        db.session.add(thing)
        db.session.commit()

        detailsid = sensordetails.query.filter(sensordetails.sensorid == sensor.query.filter(sensor.name == data['sensor']).value('id')).value('id')
        thing = sensordetails.query.get_or_404(detailsid)
        thing.liveval = data['liveval']
        db.session.add(thing)
        db.session.commit()

        data = {"message": f"car  has been updated successfully."}
        return jsonify(data), 200
        # return {"message": f"car {thing.id} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(thing)
        db.session.commit()
        data = {"message": f"car  has been deleted successfully."}
        return jsonify(data), 200
        # return {"message": f"Car {thing.id} successfully deleted."}


def updatesensoralerts(sensorid,liveval):
    from models import sensor,sensorval, sensordetails, sensoralerts
    from app import db
    data = sensordetails.query.filter(sensordetails.id == sensorid).all()
    for i in data:
        counnt = 0
        
        alerttype = 'Green'
        color = 'Green'
        isalert = 0
        lowrangeop = i.lowop
        lowrangeval = i.lowrange
        medrangeop = i.medop
        medrangeval = i.midrange
        highrangeop = i.highop
        highrangeval = i.highrange
        lastalertval = sensorval.query.filter(sensorval.sensorid == sensorid).order_by(sensorval.created_on.desc()).limit(30)

        if highrangeop == '>':
          highrangeval = highrangeval.replace(">", "")
          for val in lastalertval:

              print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  greaterthen jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',val.liveval)
              if float(val.liveval) > float(highrangeval):
                  counnt = counnt + 1
        elif highrangeop == '<':
          highrangeval = highrangeval.replace("<", "")
          for val in lastalertval:
              print('<<<<<<<<<<<<<<<<<<<<<<<   jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj',val.liveval)
              if float(val.liveval) < float(highrangeval):
                  counnt = counnt + 1
        else:
            print("nothing")

        

        if medrangeop == 'RANGE':
            x = medrangeval.split('-')


            print("values",float(liveval),float(x[0]),float(x[1]))


            if(float(liveval) >= float(x[0]) and float(liveval) < float(x[1])):
                isalert = 0
                alerttype = 'Mid'
                color = 'Yellow'
                desc = ''
                
                sid = sensordetails.query.filter(sensordetails.sensorid == i.id).value('id')
                thing = sensordetails.query.get_or_404(sid)
                # thing.alertstatus = 'False'
                thing.alerttype = 'Yellow'
                db.session.add(thing)
                db.session.commit()

            elif lowrangeop == 'RANGE':
                x = lowrangeval.split('-')
                print("values",float(liveval),float(x[0]),float(x[1]))
                if(float(liveval) >= float(x[0]) and float(liveval) < float(x[1])):
                    isalert = 0
                    alerttype = 'Low'
                    color = 'Green'
                    sid = sensordetails.query.filter(sensordetails.sensorid == i.id).value('id')
                    thing = sensordetails.query.get_or_404(sid)
                    # thing.alertstatus = 'False'
                    thing.alerttype = 'Green'
                    db.session.add(thing)
                    db.session.commit()
					
                else:
                    print("hi")
            else:
                print("else")
            print("alert type", isalert, alerttype, color)
        
        if highrangeop == '>':
            highrangeval = highrangeval.replace(">", "")
            
            if(float(liveval) >= float(highrangeval) ):
                isalert = 1
                alerttype = 'High'
                color = 'Red'
                
            else:
                isalert = 0

        elif highrangeop == '<':
            highrangeval = highrangeval.replace("<", "")
            

            if(float(liveval) <= float(highrangeval) ):
                isalert = 1
                alerttype = 'High'
                color = 'Red'
                
            else:
                isalert = 0

        print('count==============================',counnt)
        if counnt >= 20:
            tagvalue1 = 0
            truestatus = sensoralerts.query.filter(sensoralerts.sensorid == sensorid, sensoralerts.status == False).order_by(sensoralerts.created_on.desc()).value('resolvedon')
            interval = sensordetails.query.filter( sensordetails.sensorid == sensorid).value('sampleinterval')
            print(isalert,'*************************************************',truestatus)
            if truestatus == None:
              tagvalue1 = 1

            if tagvalue1 != 1 :

              diff = (datetime.datetime.now() - truestatus).seconds
              calc = int(interval) * 8
            else :
              diff = 0
              calc = 1
            print(diff,'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$',calc)
            if (int(diff) > int(calc)) or tagvalue1 == 1:

              if isalert == 1:
                  desc = ''
                  cnt = sensoralerts.query.filter(sensoralerts.sensorid == sensorid, sensoralerts.status == True).count()
                  if cnt == 0:
                    #updatesai
                      new_car = sensoralerts(description = desc,resolvedby = None ,resolvedon = None,recommendation = None,remarks = None,status = True,severity = alerttype,alertval = liveval,alertmsg = msg,alertname = alarm,sensorid = sensorid,created_on = datetime.datetime.now())
                      db.session.add(new_car)
                      db.session.commit()

                      sid = sensordetails.query.filter(sensordetails.sensorid == sensorid).value('id')
                      thing = sensordetails.query.get_or_404(sid)
                      thing.alertstatus = 'True'
                      thing.alerttype = 'Red'
                      db.session.add(thing)
                      db.session.commit()
    return True