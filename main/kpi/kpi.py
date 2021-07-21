from datetime import timedelta, time, datetime
import pandas as pd
import time
from flask import jsonify, Blueprint, request
from influxdb import InfluxDBClient
import sys
import mySqlDataConnection

kpi_api = Blueprint('kpi_api', __name__)
sys.setrecursionlimit(150000)

influxdb = InfluxDBClient('localhost', 8086)
influxdb.create_database('test')
influxdb.get_list_database()
influxdb.switch_database('test')


# def getInfluxTableName(assetId):
#     assetQuery = "SELECT * FROM asset WHERE asset_status = true AND id = %s"
#     asset = mySqlDataConnection.mySqlDbGetOneByValue(assetQuery, (assetId,))
#     locationQuery = "SELECT location FROM company_location WHERE status = true AND id = %s"
#     companyLocation = mySqlDataConnection.mySqlDbGetOneByValue(locationQuery, (asset[8],))
#     assetCategoryQuery = "SELECT name FROM asset_category WHERE status = true AND id = %s"
#     assetCategory = mySqlDataConnection.mySqlDbGetOneByValue(assetCategoryQuery, (asset[7],))
#     tableName = f'{companyLocation[0]}_{assetCategory[0]}_{asset[3]}_{asset[0]}_Data'
#     return tableName


@kpi_api.route('/kpi-parameters-graph-live-data/<assetId>', methods=['GET'])
def get_kpi_parameters(assetId):
    kpi_details = calculate_kpi_details(assetId)
    return kpi_details, 200


def calculate_kpi_details(assetId):
    table_name = getInfluxTableName(assetId)
    data_query = 'SELECT * FROM %s WHERE asset_id = %s ORDER BY time'
    assetLiveDatas = influxdb.query((data_query) % (table_name, assetId))

    # assetLiveDatas = influxdb.query("SELECT asset_running_status FROM Manesar_Transfer_Lift_Transfer_Lift_1_1_Data")

    results = list(assetLiveDatas.get_points())
    cycle_time_flag = 0
    cycle_time = 0
    no_of_cycles = 0
    average_cycle_time = 0
    shift_time_in_seconds = 28800
    for asset_running_status_data in results:
        # print(asset_running_status_data['asset_running_status'])
        asset_running_status = asset_running_status_data['asset_running_status']
        assetDate = asset_running_status_data['time']
        fDate = datetime.strptime(assetDate, '%Y-%m-%dT%H:%M:%S.%fZ')
        if fDate.date()== (datetime.now()).date():
            if asset_running_status == 1:
                cycle_time_flag = asset_running_status
                cycle_time = cycle_time + 1
            elif asset_running_status == 0:
                if cycle_time_flag != 0:
                    no_of_cycles = no_of_cycles + 1
                    cycle_time_flag = asset_running_status

    if no_of_cycles != 0:
        average_cycle_time = cycle_time / no_of_cycles

    total_availablity_in_seconds = cycle_time
    down_time_in_seconds = shift_time_in_seconds - total_availablity_in_seconds
    utilization_in_percentage = (total_availablity_in_seconds / shift_time_in_seconds) * 100
    payload = {
        "totalAvailablity": (round((total_availablity_in_seconds/60), 2)) , 
        "totalNoOfCycle": no_of_cycles,
        "avgCycletime": (round(average_cycle_time)),
        "shift_time_in_seconds": shift_time_in_seconds, 
        "downTime":  (round((down_time_in_seconds/60), 2)),
        "utilization": (round(utilization_in_percentage)),
        "asset": "",
        "shift": "",
        "noOfCycleAboveAvg": "",
        "noOfCycleBelowAvg": "",
        "noOfCycleAsPerAvg": "",
        "date": str(datetime.now().time())
    }
    return jsonify(payload)


@kpi_api.route("/kpi-report-test")
def get_kpi_details_report_test():
    start_date = '2021-06-01'
    end_date = '2021-07-15'
    dates = pd.date_range(start_date, end_date)
    result = []

    for date in dates:
        details = calculate_kpi_details_report(1, date.date())
        print(details)
        result.append(details)
        print(result)

    return jsonify(result), 200


#   plantId;
#    assetId;
#    duration;
#     fromDate;
#     toDate;
#     reportDuration;
#     reportOption;
#     shiftName;
#  shiftId;


@kpi_api.route("/report-cycle-time", methods=['POST'])
def get_kpi_details_report():
    data = request.get_json()
    start_date = data['fromDate']
    end_date = data['toDate']

    if data['reportDuration'] == "Daily":
        end_date = data['fromDate']

    dates = pd.date_range(start_date, end_date)
    result = []

    for date in dates:
        details = calculate_kpi_details_report(data['assetId'], date.date())
        print(details)
        result.append(details)
        print(result)
    return jsonify(result), 200


def calculate_kpi_details_report(assetId, choosed_date):
    table_name = getInfluxTableName(assetId)
    next_day = choosed_date+timedelta(2)
    # data_query = 'SELECT * FROM %s WHERE asset_id = %s AND  time >= %s AND time < %s ORDER BY time'
    data_query = 'SELECT * FROM %s WHERE asset_id = %s AND  time >= %s ORDER BY time'
    # data_query = 'SELECT * FROM %s WHERE asset_id = %s AND  time BETWEEN %s AND  %s ORDER BY time'
    assetLiveDatas = influxdb.query((data_query) % (table_name, assetId, choosed_date))

    # assetLiveDatas = influxdb.query("SELECT asset_running_status FROM Manesar_Transfer_Lift_Transfer_Lift_1_1_Data")

    results = list(assetLiveDatas.get_points())
    cycle_time_flag = 0
    cycle_time = 0
    no_of_cycles = 0
    average_cycle_time = 0
    shift_time_in_seconds = 28800
    time = ""
    for asset_running_status_data in results:
        assetDate = asset_running_status_data['time']
        fDate = datetime.strptime(assetDate, '%Y-%m-%dT%H:%M:%S.%fZ')
        if fDate.date()==choosed_date:
                   # print(asset_running_status_data['asset_running_status'])
            asset_running_status = asset_running_status_data['asset_running_status']
            time = asset_running_status_data['time']
            # print(time)
            if asset_running_status == 1:
                cycle_time_flag = asset_running_status
                cycle_time = cycle_time + 1
            elif asset_running_status == 0:
                if cycle_time_flag != 0:
                    no_of_cycles = no_of_cycles + 1
                    cycle_time_flag = asset_running_status

    if no_of_cycles != 0:
        average_cycle_time = cycle_time / no_of_cycles

    total_availablity_in_seconds = cycle_time
    down_time_in_seconds = shift_time_in_seconds - total_availablity_in_seconds
    utilization_in_percentage = (total_availablity_in_seconds / shift_time_in_seconds) * 100
    from models import asset
    assetName = asset.query.filter(asset.id == assetId).value('name')
    payload = {
        "totalAvailablity": (round((total_availablity_in_seconds/60), 2)) , 
        "totalNoOfCycle": no_of_cycles,
        "avgCycletime": (round(average_cycle_time)),
        "shift_time_in_seconds": shift_time_in_seconds, 
        "downTime":  (round((down_time_in_seconds/60), 2)),
        "utilization": (round(utilization_in_percentage)),
        "asset": assetName,
        "shift": "",
        "noOfCycleAboveAvg": "",
        "noOfCycleBelowAvg": "",
        "noOfCycleAsPerAvg": "",
        "date":choosed_date,
        "time":time
    }
    return (payload)


def getInfluxTableName(assetId):
    from models import asset,companylocation,assetcategory
    asset_data = asset.query.get_or_404(assetId)
    companylocation_data = companylocation.query.get_or_404(asset_data.companylocation)
    assetcategory_data = assetcategory.query.get_or_404(asset_data.assetcategory)
    tableName = f'{companylocation_data.location}_{assetcategory_data.name}_{asset_data.name}_{asset_data.id}_Data'
    return tableName


@kpi_api.route('/importData', methods=['GET'])
def importSensorData():
    from models import asset,companylocation,assetcategory
    assets = asset.query.filter(asset.status == True).all()
    # assets = mySqlDataConnection.mySqlDbGetAll(assetQuery)
    for assetObj in assets:
        companylocationObj = companylocation.query.filter(companylocation.id == assetObj.companylocation).value(
            'location')
        assetcategoryObj = assetcategory.query.filter(assetcategory.id == assetObj.assetcategory).value('name')
        #tableName = f'{companylocationObj}_{assetcategoryObj}_{assetObj.name}_{assetObj.id}_Data'
        #insertData(tableName, assetObj.id)
        insertData('Manesar_Transfer_Lift_Transfer_Lift_1_1_Data', 1)
        
        

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
            power_line3_value = row[16]
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
                "measurement": tableName,
                "time": datetime.now(),
                "fields": {
                    'company_location': company_location,
                    'asset_category': asset_category,
                    'asset_id': asset_id,
                    'asset_name': asset_name,
                    'cc_link_nw_status': cc_link_nw_status,
                    'ethernet_network_status': ethernet_network_status,
                    'tl_comm_status': tl_comm_status,
                    'tl_status': tl_status,
                    'cc_link_Card': cc_link_Card,
                    'io_card': io_card,
                    'plc': plc,
                    'preventive_analysis': preventive_analysis,
                    'chain_elongation': chain_elongation,
                    'abnormal_vibration': abnormal_vibration,
                    'power_line1_value': power_line1_value,
                    'power_line2_value': power_line2_value,
                    'power_line3_value': power_line3_value,
                    'motor_vibration_x_axis': motor_vibration_x_axis,
                    'motor_vibration_z_axis': motor_vibration_z_axis,
                    'mast_vibration_x_axis': mast_vibration_x_axis,
                    'mast_vibration_z_axis': mast_vibration_z_axis,
                    'available_time': available_time,
                    'machine_down_time': machine_down_time,
                    'tl_utilization': tl_utilization,
                    'cycle_time': cycle_time,
                    'voltage_line1_value': voltage_line1_value,
                    'voltage_line2_value': voltage_line2_value,
                    'voltage_line3_value': voltage_line3_value,
                    'current_line1_value': current_line1_value,
                    'current_line2_value': current_line2_value,
                    'current_line3_value': current_line3_value,
                    'frequency_line1_value': frequency_line1_value,
                    'frequency_line2_value': frequency_line2_value,
                    'frequency_line3_value': frequency_line3_value,
                    'proximity_value': proximity_value,
                    'temperature_value': temperature_value,
                    'asset_running_status': asset_running_status
                }
            }]
            influxdb.write_points(json_body)
            print("******************************************************")
            time.sleep(1)
    insertData(tableName, assetId)

@kpi_api.route('/trend-live-data/<assetId>', methods=['GET'])
def trendLiveData(assetId):
    now = datetime.now()
    tableName = getInfluxTableName(assetId)
    dataQuery = 'SELECT * FROM %s WHERE asset_id = %s ORDER BY time DESC LIMIT 1'
    result = influxdb.query((dataQuery) % (tableName, assetId))
    points = list(result.get_points())
    assetLiveData = points[0]
    results = {
        "time": assetLiveData["time"],
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


@kpi_api.route('/kpi-live-data/<assetId>', methods=['GET'])
def kpiLiveData(assetId):
    tableName = getInfluxTableName(assetId)
    dataQuery = 'SELECT * FROM %s WHERE asset_id = %s ORDER BY time DESC LIMIT 1'
    result = influxdb.query((dataQuery) % (tableName, assetId))
    points = list(result.get_points())
    assetLiveData = points[0]
    results = {
        "time": assetLiveData["time"],
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

@kpi_api.route('/trend-history-data', methods=['POST'])
def trendHistoryData():
    from models import asset,companylocation,assetcategory
    data = request.get_json()
    assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value('id')
    tableName = getInfluxTableName(assetId)
    fromTime = data['fromtime']
    toTime = data['totime']
    parameters = data['parameter']
    dataQuery = "SELECT %s FROM %s WHERE asset_id = %s AND time >= '%s' AND time <= '%s' ORDER BY time DESC"
    result = influxdb.query((dataQuery) % (parameters,tableName, assetId, fromTime, toTime))
    points = list(result.get_points())
    response_list = []
    for point in points:
        response_data = {
            "time":point['time'],
            "perameter" : data['parameter'],
            "value":point[data['parameter']]
        }
        response_list.append(response_data)
    return jsonify(response_list), 200

@kpi_api.route('/trend-parameter-list', methods=['POST'])
def trendParameterList():
    from models import asset,companylocation,assetcategory
    # data = request.get_json()
    # assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value('id')
    # tableName = getInfluxTableName(assetId)
    # dataQuery = "SHOW FIELD KEYS FROM %s"
    # result = influxdb.query((dataQuery) % (tableName))
    # points = list(result.get_points())
    # results = []
    # for pointObj in points:
    #     results.append(pointObj)
    results = [
        {"fieldKey":"voltage_line1_value"},
        {"fieldKey":"voltage_line2_value"},
        {"fieldKey":"voltage_line3_value"},
        {"fieldKey":"current_line1_value"},
        {"fieldKey":"current_line2_value"},
        {"fieldKey":"current_line3_value"},
        {"fieldKey":"power_line1_value"},
        {"fieldKey":"power_line2_value"},
        {"fieldKey":"power_line3_value"},
        {"fieldKey":"frequency_line1_value"},
        {"fieldKey":"frequency_line2_value"},
        {"fieldKey":"frequency_line3_value"},
        {"fieldKey":"motor_vibration_x_axis"},
        {"fieldKey":"motor_vibration_z_axis"},
        {"fieldKey":"mast_vibration_x_axis"},
        {"fieldKey":"mast_vibration_z_axis"},
        {"fieldKey":"temperature_value"}
    ]
    return jsonify(results), 200

@kpi_api.route('/kpi-breakdown-analysis', methods=['POST'])
def kpiBreakdownAnalysis():
    from models import asset,companylocation,assetcategory,lossanalysis
    data = request.get_json()
    now = datetime.now()
    curerntDate = now.strftime("%d/%m/%Y")
    assetId = asset.query.filter(asset.name == data['asset'], asset.status == True).value("id")
    lossanalysis_List = lossanalysis.query.filter(lossanalysis.asset == assetId).all()
    totalLosses = 0
    for lossanalysis_data in lossanalysis_List:
        losscreatedon = (lossanalysis_data.createdon).strftime("%d/%m/%Y")
        if (losscreatedon == curerntDate) == True:
            totalLosses = totalLosses + 1
    response={
        "totalAlerts":0,
        "totalLossAnalysis":totalLosses
    }
    return jsonify(response), 200






    

@kpi_api.route("/report-cycle-time-view", methods=['POST'])
def get_kpi_details_report_view_test():
    data = request.get_json()
    start_date = data['fromDate']
    end_date = data['toDate']

    if data['reportDuration'] == "Daily":
        end_date = data['fromDate']

    result = calculate_kpi_details_report_overAll_New(data['assetId'], start_date,end_date)

    return jsonify(result), 200

def calculate_kpi_details_report_overAll_New(assetId, startDate,endDate):
    
    table_name = getInfluxTableName(assetId)
    dates = pd.date_range(startDate, endDate)
    

    totalAvailablity = int(0)
    totalNoOfCycle = 0
    avgCycletime = 0
    shiftTimeInSeconds = 0
    downTime = 0
    utilization = 0
    asset = ""
    shift = ""
    noOfCycleAboveAvg = 0
    noOfCycleBelowAvg = 0
    noOfCycleAsPerAvg = 0
    date = ""
    avg = calculate_average_cycle_time(dates,table_name,assetId)
    print(avg)
    
    for date in dates:
        cycle_time_flag = 0
        cycle_time = 0
        no_of_cycles = 0
        average_cycle_time = 0
        shift_time_in_seconds = 28800
        choosed_date = date.date()
        data_query = 'SELECT * FROM %s WHERE asset_id = %s AND  time >= %s  ORDER BY time'
        assetLiveDatas = influxdb.query((data_query) % (table_name, assetId, choosed_date))

        # assetLiveDatas = influxdb.query("SELECT asset_running_status FROM Manesar_Transfer_Lift_Transfer_Lift_1_1_Data")

        results = list(assetLiveDatas.get_points())
        for asset_running_status_data in results:
            # print(asset_running_status_data['asset_running_status'])
            asset_running_status = asset_running_status_data['asset_running_status']
            assetDate = asset_running_status_data['time']
            fDate = datetime.strptime(assetDate, '%Y-%m-%dT%H:%M:%S.%fZ')
            if fDate.date() == choosed_date:
                if asset_running_status == 1:
                    cycle_time_flag = asset_running_status
                    cycle_time = cycle_time + 1
                elif asset_running_status == 0:
                    if cycle_time_flag != 0:
                        no_of_cycles = no_of_cycles + 1
                        cycle_time_flag = asset_running_status

        if no_of_cycles != 0:
            average_cycle_time = cycle_time / no_of_cycles

        total_availablity_in_seconds = cycle_time
        down_time_in_seconds = shift_time_in_seconds - total_availablity_in_seconds
        utilization_in_percentage = (total_availablity_in_seconds / shift_time_in_seconds) * 100
        # --------dto--------

        totalAvailablity = totalAvailablity + (total_availablity_in_seconds/3600)
        totalNoOfCycle = totalNoOfCycle + no_of_cycles
        avgCycletime = avgCycletime + average_cycle_time
        shiftTimeInSeconds = shiftTimeInSeconds + shift_time_in_seconds
        downTime = downTime + (down_time_in_seconds / 3600)
        utilization = utilization + utilization_in_percentage
        asset = ""
        shift = ""
        if average_cycle_time > avg:
           noOfCycleAboveAvg = noOfCycleAboveAvg+(no_of_cycles)
        elif average_cycle_time<avg:
           noOfCycleBelowAvg = noOfCycleBelowAvg+(no_of_cycles)
        else :
            noOfCycleAsPerAvg = noOfCycleAsPerAvg+(no_of_cycles)
        noOfCycleBelowAvg = noOfCycleBelowAvg
        noOfCycleAsPerAvg = noOfCycleAsPerAvg 
        date = choosed_date
        
        # ---------------------
    
    avgCycletime = avgCycletime / len(dates)


    payload = {
        "totalAvailablity": (round(totalAvailablity,2)),
        "totalNoOfCycle": (round(totalNoOfCycle,2)),
        "avgCycletime": (round(avgCycletime,2)),
        "shift_time_in_seconds": shiftTimeInSeconds,
        "downTime": round(downTime,2),
        "utilization": round(utilization,2),
        "asset": "",
        "shift": "",
        "noOfCycleAboveAvg": noOfCycleAboveAvg,
        "noOfCycleBelowAvg": noOfCycleBelowAvg,
        "noOfCycleAsPerAvg": noOfCycleAsPerAvg,
        "date": choosed_date
    }
    return (payload)

def calculate_average_cycle_time(dates,table_name,assetId):
   
    avg = 0.0
    avgCycletime =0
    for date in dates:
        cycle_time_flag = 0
        cycle_time = 0
        no_of_cycles = 0
        average_cycle_time = 0 
        choosed_date = date.date()
        data_query = 'SELECT * FROM %s WHERE asset_id = %s AND  time >= %s  ORDER BY time'
        assetLiveDatas = influxdb.query((data_query) % (table_name, assetId, choosed_date))

        # assetLiveDatas = influxdb.query("SELECT asset_running_status FROM Manesar_Transfer_Lift_Transfer_Lift_1_1_Data")

        results = list(assetLiveDatas.get_points())
        for asset_running_status_data in results:
            # print(asset_running_status_data['asset_running_status'])
            asset_running_status = asset_running_status_data['asset_running_status']
            assetDate = asset_running_status_data['time']
            fDate = datetime.strptime(assetDate, '%Y-%m-%dT%H:%M:%S.%fZ')
            if fDate.date() == choosed_date:
                if asset_running_status == 1:
                    cycle_time_flag = asset_running_status
                    cycle_time = cycle_time + 1
                elif asset_running_status == 0:
                    if cycle_time_flag != 0:
                        no_of_cycles = no_of_cycles + 1
                        cycle_time_flag = asset_running_status

        if no_of_cycles != 0:
            average_cycle_time = cycle_time / no_of_cycles

        avgCycletime = avgCycletime + average_cycle_time
          
    avg = avgCycletime / len(dates)
    print(avg)
    return avg