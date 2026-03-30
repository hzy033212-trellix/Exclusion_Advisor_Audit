import json
from datetime import datetime

read_file_path = 'events.json'
write_file_path = 'events_output.json'

# 1. Read the JSON data from the file
print("Start read json time: " + str(datetime.now()))
try:
    with open(read_file_path, 'r') as file:
        data = json.load(file) # Converts JSON to a Python list/dict
except FileNotFoundError:
    print(f"Error: {json_file_path} not found.")
    exit()
print("End read json time: " + str(datetime.now()))

final_result = {}
final_result['itemList'] = {}
final_result['itemList']['eventItem'] = []

data = data['itemList']['eventItem']
for record in data:
    curDict = {}
    curDict['eventType1'] = record['eventType']
    curDict['timestamp1'] = record['timestamp']
    curList = record['details']['detail']
    for cur in curList:
        try:
            curDict[cur['name']] = cur['value']
        except Exception as e:
            print(str(record))
            print("==========")
    record['details']['detail'] = curDict
    final_result['itemList']['eventItem'].append(curDict)

print("Start print json time: " + str(datetime.now()))
with open(write_file_path, "w") as json_file:
    json.dump(final_result, json_file, indent=4)
print("End print json time: " + str(datetime.now()))
    
print("Program Completed!")