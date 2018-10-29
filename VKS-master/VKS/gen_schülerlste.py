import json
s1 = {'name':'Paul Schneider', 'status':'anwesend', 'year':'2004'}
s2 = {'name':'Karl Twister', 'status':'anwesend', 'year':'2004'}
s3 = {'name':'Jakob Förster', 'status':'anwesend', 'year':'2004'}
s4 = {'name':'Mark Schuhmacher', 'status':'anwesend', 'year':'2004'}
s5 = {'name':'Kevin Anderson', 'status':'abwesend', 'year':'2004'}
s6 = {'name':'Anna Maurer', 'status':'abwesend', 'year':'2004'}
s7 = {'name':'Leo Müller', 'status':'abwesend', 'year':'2004'}
s8 = {'name':'Maja Musterfrau', 'status':'abwesend', 'year':'2004'}
s9 = {'name':'Maria Eulenspiegel', 'status':'anwesend', 'year':'2004'}
s10 = {'name':'Knut Elstermann', 'status':'abwesend', 'year':'2004'}
schuelerliste = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
json.dump(schuelerliste, open("schuelerliste-9b.json", "w"))
