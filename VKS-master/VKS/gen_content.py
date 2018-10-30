import json
entry1 = {"name":"The Thruth", "author":"Sage with eyes of blue", "date":"1.1.2000", "time":"00:00", "content":"Justice is only a tool to judge over Sins. But Justice don't block Sins."}
entry2 = {"name": "Alternative Thruth", "author":"Sage with eyyes of red", "date":"2.1.2000", "time":"00:00", "content":"I am a bread."}
entrys = [entry1, entry2] # + other entrys
json.dump(entrys, open("content.json", "w"))
