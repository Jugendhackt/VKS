import json
term1 = {"name":"Day of open door", "date":"2018-10-31", "author":"Byakushiki", "content":"A day full of open doors."}
term2 = {"name":"Day of closed door", "date":"2018-10-31", "author":"Byakushiki", "content":"A day full of closed doors."}
term_list = (term1, term2)
json.dump(term_list, open("terms.json", "w"))
