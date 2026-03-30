import json
import sqlite3
from datetime import datetime

file_path = 'dns_output_json_file.json'
file_path_2 = 'dns_output_json_file_2.json'
output_path_1 = 'dns_dedup_json_file.json'
output_path_2 = 'dns_re_format_file.json'

# 1. Read the JSON data from the file
print("Start read json time: " + str(datetime.now()))
try:
    with open(file_path, 'r') as file:
        data = json.load(file) # Converts JSON to a Python list/dict
except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    exit()
try:
    with open(file_path_2, 'r') as file_2:
        data_2 = json.load(file_2) # Converts JSON to a Python list/dict
except FileNotFoundError:
    print(f"Error: {file_path_2} not found.")
    exit()
print("End read json time: " + str(datetime.now()))

time_dict = {}
for elem in data_2:
    time_dict[elem['fullProcessPath']] = {}
    time_dict[elem['fullProcessPath']]['firstEvent'] = elem['firstEvent']
    time_dict[elem['fullProcessPath']]['lastEvent'] = elem['lastEvent']

def deduplicate_list_of_dicts(list_of_dicts):
    seen = set()
    unique_list = []
    for d in list_of_dicts:
        # Create a hashable representation of the dictionary (e.g., a frozenset of items)
        # to check for uniqueness in the set.
        # This assumes all dictionary values are hashable.
        hashable_d = frozenset(d.items())
        if hashable_d not in seen:
            seen.add(hashable_d)
            unique_list.append(d)
    return unique_list
unique_data = deduplicate_list_of_dicts(data)
with open(output_path_1, "w") as json_file:
    json.dump(unique_data, json_file, indent=4)
    
result_dict = {}    
for elem in unique_data:
    if elem['fullProcessPath'] not in result_dict:
        result_dict[elem['fullProcessPath']] = {}
        result_dict[elem['fullProcessPath']]['processPathCount'] = elem['processPathCount']
        result_dict[elem['fullProcessPath']]['firstEvent'] = time_dict[elem['fullProcessPath']]['firstEvent']
        result_dict[elem['fullProcessPath']]['lastEvent'] = time_dict[elem['fullProcessPath']]['lastEvent']
    result_dict[elem['fullProcessPath']][elem['fullPath']] = elem['filePathUnderProcessCount']
result_list = []
for key in result_dict:
    tmp = {}
    tmp['process'] = key
    tmp['processPathCount'] = result_dict[key]['processPathCount']
    tmp['firstEvent'] = result_dict[key]['firstEvent']
    tmp['lastEvent'] = result_dict[key]['lastEvent']
    first_event_timestamp = datetime.strptime(tmp['firstEvent'], '%Y-%m-%dT%H:%M:%S.%fZ')
    last_event_timestamp = datetime.strptime(tmp['lastEvent'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if tmp['firstEvent'] != tmp['lastEvent']:
        tmp['frequencyPerHour'] = tmp['processPathCount'] * 3600 / (last_event_timestamp - first_event_timestamp).total_seconds()
    tmp['written_files'] = []
    curDict = result_dict[key]
    for file in curDict:
        if file != 'processPathCount' and file != 'firstEvent' and file != 'lastEvent':
            tmpDict = {}
            tmpDict['path'] = file
            tmpDict['writeCount'] = curDict[file]
            tmp['written_files'].append(tmpDict)
    tmp['written_files'] = sorted(tmp['written_files'], key=lambda item: item['writeCount'], reverse=True)
    tmp['largest_25_total_count'] = sum(d['writeCount'] for d in tmp['written_files'][:25])
    tmp['written_files'] = tmp['written_files'][:25]
    result_list.append(tmp)
    sorted_result_list = sorted(result_list, key=lambda item: item['processPathCount'], reverse=True)
with open(output_path_2, "w") as json_file:
    json.dump(sorted_result_list, json_file, indent=4)

print("Program Completed!")
