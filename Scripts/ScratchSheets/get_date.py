from dateutil.parser import *
from dateutil.tz import *
from datetime import *

#Test the parser function
str1 = "September 5, 1988 hahaha"
str2 = "07/27/1987"

p1 = parse(str1, fuzzy=True)
print p1
print type(p1)

p2 = parse(str2)
print p2
print type(p2)