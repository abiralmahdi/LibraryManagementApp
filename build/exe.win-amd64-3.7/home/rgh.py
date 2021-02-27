import datetime

a = abs(datetime.datetime.now()-datetime.datetime.strptime('12/12/12', '%d/%m/%y')).days
print(a)