from app import db
import datetime

# class shift(db.Model):
#     __tablename__ = 'shift'
#     # __bind_key__ = 'mydb'
#
#     id = db.Column(db.Integer, primary_key=True)
#     status = db.Column(db.Boolean)
#     shift_name = db.Column(db.String(255))
#     start_time = db.Column(db.Time)
#     end_time = db.Column(db.Time)
#     company_location_id= db.Column(db.Integer)
#
# # compdatetime = db.Column(db.DateTime)
#
#     def __init__(self, status, shift_name, start_time, end_time, company_location_id):
#         self.status = status
#         self.shift_name = shift_name
#         self.start_time = start_time
#         self.end_time = end_time
#         self.company_location_id = company_location_id
#
#     def __repr__(self):
#         return '<id {}>'.format(self.id)
#
#     def serialize(self):
#         return {
#             'id': self.id,
#             'status': self.status,
#             'shiftName': self.shift_name,
#             # 'start_time': self.start_time,
#             # 'end_time': self.end_time,
#             'companyLocationId': self.company_location_id,
#         }

class shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)
    status = db.Column(db.Boolean)
    plantId = db.Column(db.Integer)

    def __init__(self, name, starttime, endtime, status,plantId):
        self.name = name
        self.starttime = starttime
        self.endtime = endtime
        self.status = status
        self.plantId = plantId

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'starttime': str(self.starttime),
            'endtime': str(self.endtime),
            'status': self.status,
            'plantId': self.plantId
        }

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    username = db.Column(db.String(255))
    company_location_id = db.Column(db.Integer)
    plant_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)

    # compdatetime = db.Column(db.DateTime)

    def __init__(self, status, first_name, last_name,middle_name,password,username,company_location_id,plant_id,role_id):
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.password = password
        self.username = username
        self.company_location_id = company_location_id
        self.plant_id = plant_id
        self.role_id = role_id
        # self.compdatetime = compdatetime

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'middleName': self.middle_name,
            'password': self.password,
            'username': self.username,
            'companyLocationId': self.company_location_id,
            'plantId': self.plant_id,
            'roleId':self.role_id
            #  'compdatetime':self.compdatetime,
        }


class sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    name = db.Column(db.String(255))
    tag_name = db.Column(db.String(255))
    sensor_type = db.Column(db.String(255))
    additional_info = db.Column(db.String(255))
    battery_life = db.Column(db.Integer)
    in_use = db.Column(db.Boolean)
    fw_version = db.Column(db.String(255))
    model = db.Column(db.Integer)
    # sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    asset_sensor_allocation_id = db.Column(db.Integer, db.ForeignKey('asset_sensor_allocation.id'))

    # compdatetime = db.Column(db.DateTime)

    def __init__(self, status, name, tag_name,sensor_type,additional_info,battery_life,in_use,fw_version,model):
        self.status = status
        self.name = name
        self.tag_name = tag_name
        self.sensor_type = sensor_type
        self.additional_info = additional_info
        self.battery_life = battery_life
        self.in_use = in_use
        self.fw_version = fw_version
        self.model = model
        # self.asset_sensor_allocation_id = asset_sensor_allocation_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'status': self.status,
            'name': self.name,
            'tagName': self.tag_name,
            'sensorType': self.sensor_type,
            'additionalInfo': self.additional_info,
            'batteryLife': self.battery_life,
            'usage': self.in_use,
            'model': self.model,
            'fwVersion':self.fw_version,
            'assetSensorAllocationId' : self.asset_sensor_allocation_id
            #  'compdatetime':self.compdatetime,
        }


class asset_sensor_allocation(db.Model):
    __tablename__ = 'asset_sensor_allocation'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    # sensors = db.relationship("sensor", backref="asset_sensor_allocation",lazy='dynamic',foreign_keys = 'sensor.id')
    sensors = []
    def __init__(self, status, asset_id):
        self.status = status
        self.asset_id = asset_id
        

    def __repr__(self):
        return '<id {}>'.format(self.id,self.asset_id)

# asset_sensor_allocation.sensors = db.relationship("sensor", order_by = sensor.id, back_populates = "asset_sensor_allocation")


# class asset(db.Model):
#     __tablename__ = 'asset'
#
#     id = db.Column(db.Integer, primary_key=True)
#     asset_status = db.Column(db.Boolean)
#     name = db.Column(db.String(255))
#
#     def __init__(self, asset_status, name):
#         self.asset_status = asset_status
#         self.name = name
#
#     def __repr__(self):
#         return '<id {}>'.format(self.id)
#
#     def serialize(self):
#         return {
#             'id': self.id,
#             'assetStatus': self.asset_status,
#             'name':self.name
#             #  'compdatetime':self.compdatetime,
#         }

# Mapping test

class role(db.Model):
    __tablerole__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Car {self.id}>"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class dept(db.Model):
    __tablerole__ = 'dept'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    des = db.Column(db.String(255))

    def __init__(self, name, des):
        self.name = name
        self.des = des

    def __repr__(self):
        return f"<Car {self.id}>"

# ----------------Dhwanit code---------------

class companylocation(db.Model):
    __tablename__ = 'companylocation'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255))
    productioncapacity = db.Column(db.Integer)
    longitude = db.Column(db.String(255))
    latitude = db.Column(db.String(255))
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


#------------------------------Asset Category-----------------------------------------
class assetcategory(db.Model):
    __tablename__ = 'assetcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
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

class asset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
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


# ------------------------------Alertrule - -------------------------------------------------

class alarmconfiguration(db.Model):
    __tablename__ = 'alarmconfiguration'

    id = db.Column(db.Integer, primary_key=True)
    companylocation = db.Column(db.Integer, db.ForeignKey('companylocation.id'), nullable=False)
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable=False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    alertsubcategory = db.Column(db.String(255))
    alertlimittype = db.Column(db.String(255))
    configvalue = db.Column(db.Integer)
    alarm = db.Column(db.String(255))
    severity = db.Column(db.String(255))
    createdon = db.Column(db.DateTime)
    status = db.Column(db.Boolean)

    def __init__(self, companylocation, assetcategory, asset, alertsubcategory, alertlimittype, configvalue, alarm,
                 severity, createdon, status):
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
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable=False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    alertsubcategory = db.Column(db.String(255))
    alertlimittype = db.Column(db.String(255))
    trackvalue = db.Column(db.Float)
    alarm = db.Column(db.String(255))
    alertstatus = db.Column(db.Boolean)
    triggeredon = db.Column(db.DateTime)

    def __init__(self, assetcategory, asset, alertsubcategory, alertlimittype, trackvalue, alarm, alertstatus,
                 triggeredon):
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


#------------------------------Loss Analysis--------------------------------------------------

class losscategory(db.Model):
    __tablename__ = 'losscategory'

    id = db.Column(db.Integer, primary_key=True)
    losscategory = db.Column(db.String(255))
    description = db.Column(db.String(255))
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
    losssubcategory = db.Column(db.String(255))
    description = db.Column(db.String(255))
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


# ------------------------------Preventive Maintenance--------------------------------------------------

class durationtype(db.Model):
    __tablename__ = 'durationtype'

    id = db.Column(db.Integer, primary_key=True)
    durationtype = db.Column(db.String(255))
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
    checkpart = db.Column(db.String(255))
    checkpoint = db.Column(db.String(255))
    description = db.Column(db.String(255))
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
    checkpart = db.Column(db.String(255))
    checkpoint = db.Column(db.String(255))
    checkpointstatus = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    standardvalue = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    remark = db.Column(db.String(255))
    submittedon = db.Column(db.DateTime)
    submittedby = db.Column(db.String(255))

    def __init__(self, checkpart, checkpoint, checkpointstatus, description, standardvalue, status, remark, submittedon,
                 submittedby):
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
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable=False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    durationtype = db.Column(db.Integer, db.ForeignKey('durationtype.id'), nullable=False)
    durationvalue = db.Column(db.Integer)
    uploadedby = db.Column(db.String(255))
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
    assetcategory = db.Column(db.Integer, db.ForeignKey('assetcategory.id'), nullable=False)
    asset = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    durationtype = db.Column(db.Integer, db.ForeignKey('durationtype.id'), nullable=False)
    durationvalue = db.Column(db.Integer)
    allchecklistcompleted = db.Column(db.Boolean)
    submittedyear = db.Column(db.Integer)
    submittedon = db.Column(db.DateTime)
    submittedby = db.Column(db.String(255))
    isautosubmit = db.Column(db.Boolean)
    assignedon = db.Column(db.DateTime)
    submittedbysupervisor = db.Column(db.String(255))

    def __init__(self, assetcategory, asset, allchecklistcompleted, durationtype, durationvalue, submittedyear,
                 submittedon, submittedby, isautosubmit, assignedon, submittedbysupervisor):
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
    preventivemaintenancemaster = db.Column(db.Integer, db.ForeignKey('preventivemaintenancemaster.id'), nullable=False)
    checklistmaster = db.Column(db.Integer, db.ForeignKey('checklistmaster.id'), nullable=False)

    def __init__(self, preventivemaintenancemaster, checklistmaster):
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
    preventivemaintenance = db.Column(db.Integer, db.ForeignKey('preventivemaintenance.id'), nullable=False)
    checklist = db.Column(db.Integer, db.ForeignKey('checklist.id'), nullable=False)

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

class adminlog(db.Model):
    __tablename__ = 'adminlog'

    id = db.Column(db.Integer, primary_key=True)
    loggedon = db.Column(db.DateTime)
    loggedby = db.Column(db.String())
    module = db.Column(db.String())
    activitydone = db.Column(db.String())
    activityid = db.Column(db.Integer)

    def __init__(self, loggedon, loggedby, module, activitydone, activityid):
        self.loggedon = loggedon
        self.loggedby = loggedby
        self.module = module
        self.activitydone = activitydone
        self.activityid = activityid

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'loggedon': self.loggedon,
            'loggedby': self.loggedby,
            'module': self.module,
            'activitydone': self.activitydone,
            'activityid': self.activityid
        }

#----------------Sensor Details -----------------------------------------#

class sensordetails(db.Model):
    __tablename__ = 'sensordetails'

    id = db.Column(db.Integer, primary_key=True)
    alarm = db.Column(db.String())
    operator = db.Column(db.String())
    msg = db.Column(db.String())
    realtimeval = db.Column(db.String())
    thresholdvalue = db.Column(db.String())
    sensorid = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable = False)
    property = db.Column(db.String())
    type = db.Column(db.String())
    description = db.Column(db.String())
    units = db.Column(db.String())
    propertyid = db.Column(db.String())
    propertytype = db.Column(db.String())
    midrange =  db.Column(db.String())
    lowrange =  db.Column(db.String())
    highrange =  db.Column(db.String())
    lowop =  db.Column(db.String())
    medop =  db.Column(db.String())
    highop =  db.Column(db.String())
    alertstatus =  db.Column(db.String())
    alerttype =  db.Column(db.String())
    asset = db.Column(db.Integer)
    assetcategory = db.Column(db.Integer)
    sampleinterval = db.Column(db.String())

    def __init__(self,sampleinterval,asset,assetcategory,midrange, lowrange, highrange, lowop, medop, highop, alertstatus, alerttype, propertytype, propertyid, property, type, description, units, sensorid,alarm,operator,msg,realtimeval, thresholdvalue):
        self.sensorid = sensorid
        self.asset = asset
        self.sampleinterval = sampleinterval
        self.assetcategory = assetcategory
        self.midrange = midrange
        self.lowrange= lowrange
        self.highrange = highrange
        self.lowop = lowop
        self.medop = medop
        self.highop = highop
        self.alertstatus = alertstatus
        self.alerttype = alerttype
        self.propertyid = propertyid
        self.alarm = alarm
        self.operator = operator
        self.msg = msg
        self.realtimeval = realtimeval
        self.thresholdvalue = thresholdvalue
        self.units = units
        self.description = description
        self.type =type
        self.property = property
        self.propertytype = propertytype

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id' : self.id,
            'sensorid' : self.sensorid,
            'midrange' : self.midrange,
            'lowrange' : self.lowrange,
            'highrange' : self.highrange,
            'lowop' : self.lowop,
            'medop' : self.medop,
            'highop' : self.highop,
            'alertstatus' : self.alertstatus,
            'alerttype' : self.alerttype,
           
            'alarm' : self.alarm,
            'operator' : self.operator,
            'msg' : self.msg,
            'realtimeval' : self.realtimeval,
            'thresholdvalue' : self.thresholdvalue,
            'units' : self.units,
            'description' : self.description,
            'type' : self.type,
            'property' : self.property,
            'propertytype' : self.propertytype,
            'asset' : self.asset,
            'assetcategory'  :self.assetcategory
        }


#------------------sensor alerts--------------------------------------------#

class sensoralerts(db.Model):
    __tablename__ = 'sensoralerts'

    id = db.Column(db.Integer, primary_key=True)
    sensorid = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable = False)
    alertname = db.Column(db.String())
    alertmsg = db.Column(db.String())
    alertval = db.Column(db.String())
    status = db.Column(db.Boolean)
    severity  = db.Column(db.String())
    property  = db.Column(db.String())
    description = db.Column(db.String())
    created_on = db.Column(db.DateTime)
    resolvedon = db.Column(db.DateTime)
    remarks = db.Column(db.String())
    resolvedby = db.Column(db.String())
    recommendation = db.Column(db.String())

    def __init__(self, remarks, recommendation, resolvedon, resolvedby, sensorid,alertname,alertmsg, alertval,status,severity, created_on, description, property):
        self.sensorid = sensorid
        self.resolvedby = resolvedby
        self.resolvedon = resolvedon
        self.alertname = alertname
        self.alertmsg = alertmsg
        self.alertval = alertval
        self.status = status
        self.severity = severity
        self.created_on = created_on
        self.description = description
        self.property = property
        self.remarks = remarks
        self.recommendation = recommendation

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id' : self.id,
            'sensorid' : self.sensorid,
            'alertname' : self.alertname,
            'alertmsg' : self.alertmsg,
            'alertval' : self.alertval,
            'status' : self.status,
            'severity' : self.severity,
            'created_on' : self.created_on,
            'description' : self.description,
            'property' : self.property,
            'resolvedon' : self.resolvedon,
            'resolvedby' : self.resolvedby,
            'remarks' : self.remarks,
            'recommendation' : self.recommendation
        }

#------------------sensor value--------------------------------------------#

class sensorval(db.Model):
    __tablename__ = 'sensorval'

    id = db.Column(db.Integer, primary_key=True)
    sensorid = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable = False)
    property = db.Column(db.String())
    propertyid = db.Column(db.Integer)
    units = db.Column(db.String())
    liveval = db.Column(db.String())
    created_on = db.Column(db.DateTime)

    def __init__(self, propertyid, sensorid,property,units, liveval, created_on):
        self.sensorid = sensorid
        self.property = property
        self.units = units
        self.liveval = liveval
        self.created_on = created_on
        self.propertyid = propertyid
		
    def __repr__(self):
        return f"<Car {self.id}>"

    def serialize(self):
        return {
            'id' : self.id,
            'sensorid' : self.sensorid,
            'property' : self.property,
            'units' : self.units,
            'liveval' : self.liveval,
            'created_on' : self.created_on,
            'propertyid' : self.propertyid

        }