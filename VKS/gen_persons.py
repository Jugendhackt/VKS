import json
s1 = {'name':'Paul Schneider', 'status':'present', 'year':'2004'}
s2 = {'name':'Karl Twister', 'status':'present', 'year':'2004'}
s3 = {'name':'Jakob Förster', 'status':'present', 'year':'2004'}
s4 = {'name':'Mark Schuhmacher', 'status':'present', 'year':'2004'}
s5 = {'name':'Kevin Anderson', 'status':'absent', 'year':'2004'}
s6 = {'name':'Anna Maurer', 'status':'absent', 'year':'2004'}
s7 = {'name':'Leo Müller', 'status':'absent', 'year':'2004'}
s8 = {'name':'Maja Musterfrau', 'status':'absent', 'year':'2004'}
s9 = {'name':'Maria Eulenspiegel', 'status':'present', 'year':'2004'}
s10 = {'name':'Knut Elstermann', 'status':'absent', 'year':'2004'}
all_entrys = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
json.dump(all_entrys, open("list-9b.json", "w"))
