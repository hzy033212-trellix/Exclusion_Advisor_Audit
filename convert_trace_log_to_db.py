import json
import sqlite3
from datetime import datetime

file_path = 'trace.log'
output_json_path = 'trace_log.json'
db_file_path = 'trace_log_database.db'

# Parse trace log from raw text to dictionary in python
data = []
search = "TResult(1)"
print("Start read log time: " + str(datetime.now()))
with open(file_path, 'r', encoding='utf-8') as log_file:
    row_id = 0
    for line in log_file:
        row_id += 1
        if search in line:
            line = line.strip()
            timestamp = line[0:19]
            path = line.split("->")[-1]
            curDict = {}
            curDict['row_id'] = row_id
            curDict['timestamp'] = timestamp
            curDict['path'] = path
            data.append(curDict)
print("End read log time: " + str(datetime.now()))

print("Start write json time: " + str(datetime.now()))
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)
print("End write json time: " + str(datetime.now()))

# 2. Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# 3. Create a table in the database
# Note: You should tailor this SQL statement to match the structure of your JSON data
cursor.execute('''
CREATE TABLE IF NOT EXISTS tracelogEvents (
    row_id INTEGER,
    timestamp TEXT,
    path TEXT
)
''')

# 4. Insert the data into the table
print("Start insert data into table time: " + str(datetime.now()))
for record in data:
    if record['path'] is not None:
        cursor.execute('''INSERT INTO tracelogEvents (row_id, timestamp, path) VALUES (?, ?, ?)''', (record['row_id'], record['timestamp'], record['path']))
print("End insert data into table time: " + str(datetime.now()))

# 5. Commit the changes and close the connection
conn.commit() # Saves the changes to the .db file
conn.close()
    
print("Program Completed!")
