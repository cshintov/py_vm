#checks whether a year is leap year; 1 for yes , 0 for no

year = 248
print year
if not year % 4 and year % 100:
    print 1
else:
    print 0
