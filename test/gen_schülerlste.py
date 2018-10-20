import json
s1 = {'name':'Paul', 'status':'anwesend'}
s2 = {'name':'Karl', 'status':'anwesend'} 
s3 = {'name':'Jakob', 'status':'anwesend'} 
s4 = {'name':'Mark', 'status':'anwesend'} 
s5 = {'name':'Kevin', 'status':'abwesend'} 
s6 = {'name':'Anna', 'status':'abwesend'}
s7 = {'name':'Leo', 'status':'abwesend'}
s8 = {'name':'Maja', 'status':'abwesend'}
s9 = {'name':'Maria', 'status':'anwesend'}
s10 = {'name':'Knut', 'status':'abwesend'}
schuelerliste = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
json.dump(schuelerliste, open("schuelerliste2.json", "w"))
