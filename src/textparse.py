#!/usr/bin/python

from io import StringIO

c = open("cities.txt").read()
d = open("states.txt").read()

end = open("geographywords.txt", "w")

end.truncate()

cities = c.split("\n")

x = 0
last = cities[x]
while ( x<len(cities) ):
    i = cities[x].split("'")
    s = i[1]
    if ( s != last ):
        end.write(s + "\n")
        last = s
    x+=1

states = d.split("\n")

x = 0
last = states[x]
while ( x<len(states) ):
    i = states[x].split("'")
    s = i[1]
    if ( s != last ):
        end.write(s + "\n")
        last = s
    x+=1

end.close()
f = open("geographywords.txt").read()
print f

