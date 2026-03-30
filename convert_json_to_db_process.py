import json
import sqlite3
from datetime import datetime

file_path = 'events_output.json'
db_file_path = 'process_events_database.db'

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
CREATE TABLE IF NOT EXISTS processStartEvents (
    processPath TEXT,
    timestamp TEXT
)
''')

# 4. Insert the data into the table
print("Start insert data into table time: " + str(datetime.now()))
data = data['itemList']['eventItem']
for record in data:
    if record['eventType1'] != 'processEvent':
        continue;
    if record['eventType'] == 'start':
        cursor.execute('''INSERT INTO processStartEvents (processPath, timestamp) VALUES (?, ?)''', (record['processPath'], record['timestamp1']))
print("End insert data into table time: " + str(datetime.now()))

# 5. Commit the changes and close the connection
conn.commit() # Saves the changes to the .db file
conn.close()

print("Program Completed!")
