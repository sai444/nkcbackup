from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086)
client.switch_database('test')

json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "name": "server01",
            "region": "us-west"
        },

        "fields": {
            "value": 0.64,
            "main": 0.15
        }
    }
]

client.write_points(json_body)

result = client.query('select * from cpu_load_short;')

print("Result: {0}".format(result))
