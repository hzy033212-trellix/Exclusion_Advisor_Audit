# Exclusion_Advisor_Audit
The python scripts I wrote and used for verification of events.db related EAA testing

# How to use this repo
Trigger a Triage from HX UI and retrieve stateAgentInspector payload, i.e XML events file. Change name of this file to events.xml and put it into the same folder as this repo. Sequency run convert_xml_to_json.py and format_convert_json.py without any parameters. Then run convert_json_to_db_{type of event}.py, and it will generate db files to analyze. For four events, i.e dns, file write, image load and registry key events, dedup_rows_with_format_{type of event}.py also need to be run after convert_json_to_db_{type of event}.py. The SQLite quries can be referenced from screenshots from EAA_SQLite_Queries folder. 
