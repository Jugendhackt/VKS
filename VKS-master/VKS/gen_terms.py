import json
term1 = {"name":"Tag der offenen Tür", "date":"31. 10. 2018", "author":"Byakushiki", "content":"Tag der offenen Tür mit der Maus."}
term2 = {"name":"Tag der geschlossenen Tür", "date":"30. 10. 2018", "author":"Byakushiki", "content":"Tag der geschlossenen Tür mit der Maus."}
term_list = (term1, term2)
json.dump(term_list, open("terms.json", "w"))
