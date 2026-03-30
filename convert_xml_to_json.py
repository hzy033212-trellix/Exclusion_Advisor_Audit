import xmltodict
import json
from datetime import datetime

def xml_file_to_dict(file_path):
    """
    Reads an XML file and converts its content to a Python dictionary.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as xml_file:
            xml_data = xml_file.read()
            # Use xmltodict.parse() to convert the XML string to a dictionary (OrderedDict)
            dict_data = xmltodict.parse(xml_data)
            return dict_data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

file_path = 'events.xml'
print("Start read xml time: " + str(datetime.now()))
result_dict = xml_file_to_dict(file_path)
print("End read xml time: " + str(datetime.now()))

if result_dict:
    print("Start print json time: " + str(datetime.now()))
    # Open a file in write mode ('w') and dump the dictionary
    with open("events.json", "w") as json_file:
        json.dump(result_dict, json_file, indent=4)   
    print("End print json time: " + str(datetime.now()))
    
    print("Program Completed!")
