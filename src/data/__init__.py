import os
import json
import logging as log
import constants as c

def get(parameter,location=None,lat=None,lon=None,date=None,time="0000",dataset="10days",datatype="hres", datadir="data"):
    
    data = {}
    files = os.listdir(datadir)
    files.sort()
    for i in files:
        if i.endswith(".json"):
            bits = i.split("-")
            loc = bits[0]
            par = bits[1]
            if loc==location and par==parameter:
                log.debug("Loading data from %s, place:%s, param:%s " % (i,loc,par))
                data = json.load(open(datadir+"/"+i))[parameter][datatype]
                if parameter == c.T:
                    data = map(lambda x:x-273.15,data)
                elif parameter == c.C:
                    data = map(lambda x:x*8,data)
                elif parameter == c.P:
                    data = map(lambda x:x*1000,data)

                min,max,avg = describe(data)
                log.debug("Loaded %s values (min:%s, max:%s, avg:%s) from %s, place:%s, param:%s " % (len(data),min,max,avg,i,loc,par))
                return data

    return None


def describe(data):
    min=1000000
    max=-1000000
    total=0
    for i in data:
        if i<min:
            min=i
        if i>max:
            max=i
        total += i

    return min,max,total/len(data)
