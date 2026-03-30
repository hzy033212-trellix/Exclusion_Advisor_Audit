import json
import sqlite3
from datetime import datetime

file_path = 'events_output.json'
db_file_path = 'file_write_events_database.db'
output_json_file = 'file_write_output_json_file.json'
output_json_file_2 = 'file_write_output_json_file_2.json'

# 1. Read the JSON data from the file
print("Start read json time: " + str(datetime.now()))
try:
    with open(file_path, 'r') as file:
        data = json.load(file) # Converts JSON to a Python list/dict
except FileNotFoundError:
    print(f"Error: {json_file_path} not found.")
    exit()
print("End read json time: " + str(datetime.now()))

# 2. Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# 3. Create a table in the database
# Note: You should tailor this SQL statement to match the structure of your JSON data
cursor.execute('''
CREATE TABLE IF NOT EXISTS fileWriteEvents (
    filePath TEXT,
    processPath TEXT,
    process TEXT,
    timestamp TEXT
)
''')

# 4. Insert the data into the table
print("Start insert data into table time: " + str(datetime.now()))
data = data['itemList']['eventItem']
for record in data:
    if record['eventType1'] != 'fileWriteEvent':
        continue;
    cursor.execute('''INSERT INTO fileWriteEvents (filePath, processPath, process, timestamp) VALUES (?, ?, ?, ?)''', (record['fullPath'], record['processPath'], record['process'], record['timestamp1']))
print("End insert data into table time: " + str(datetime.now()))

# 5. Commit the changes
conn.commit() # Saves the changes to the .db file

# 6. Execute the query
def python_concat(*args):
    # Filter out None values to match CONCAT's behavior of ignoring NULLs
    return "".join(str(arg) for arg in args if arg is not None)
conn.create_function("CONCAT", -1, python_concat)    
query = '''
SELECT 
    CONCAT(processPath, "\\", process) AS fullProcessPath,
    filePath,
    COUNT(*) OVER(PARTITION BY CONCAT(processPath, "\\", process)) AS processPathCount,
    COUNT(*) OVER(PARTITION BY CONCAT(processPath, "\\", process), filePath) AS filePathUnderProcessCount
FROM 
    fileWriteEvents
WHERE
    timestamp > '2026-02-26T00:00:00.000Z'
'''
cursor.execute(query)
rows = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
data_list = []
for row in rows:
    data_list.append(dict(zip(column_names, row)))
with open(output_json_file, 'w') as json_file:
    json.dump(data_list, json_file, indent=4)
print(f"Data successfully exported to {output_json_file}")

query_2 = '''
SELECT
	CONCAT(processPath, "\\", process) AS fullProcessPath,
	MIN(timestamp) AS firstEvent,
	MAX(timestamp) AS lastEvent
FROM
	filewriteEvents
WHERE
    timestamp > '2026-02-26T00:00:00.000Z'
GROUP BY
	fullProcessPath
'''
cursor.execute(query_2)
rows_2 = cursor.fetchall()
column_names_2 = [description[0] for description in cursor.description]
data_list_2 = []
for row in rows_2:
    data_list_2.append(dict(zip(column_names_2, row)))
with open(output_json_file_2, 'w') as json_file:
    json.dump(data_list_2, json_file, indent=4)
print(f"Data successfully exported to {output_json_file_2}")

# 7. Close the connection
conn.close()

print("Program Completed!")
