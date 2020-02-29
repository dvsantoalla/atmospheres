import json
import logging as log
import os


def load_data(directory):

    data = {}
    for i in os.listdir(directory):
        if i.endswith(".json"):
            bits = i.split("-")
            place = bits[0]
            param = bits[1]
            if not data.has_key(place):
                    data[place] = {}
            log.info("Loading data from %s, place:%s, param:%s " % (i,place,param))
            data[place][param] = json.load(open(directory+"/"+i))
    

    log.debug(data)

if __name__ == '__main__':
    load_data("../../data")
