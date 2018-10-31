import json
term1 = {"name":"Tag der offenen Tür", "date":"2018-10-31", "author":"Byakushiki", "content":"Tag der offenen Tür mit der Maus."}
term2 = {"name":"Tag der geschlossenen Tür", "date":"2018-10-31", "author":"Byakushiki", "content":"Tag der geschlossenen Tür mit der Maus."}
term_list = (term1, term2)
json.dump(term_list, open("terms.json", "w"))
