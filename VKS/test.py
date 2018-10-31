import time
datum = "Sun, 19 May 2002 15:21:36 GMT"
print time.strptime(datum, "%a, %d %b %Y %H:%M:%S %Z")
