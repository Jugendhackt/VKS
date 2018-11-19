import json
s1 = {"name":"9B", "location":"/overview-9b"}
s_all = [s1]
json.dump(s_all, open("classes_overview.json", "w"))
