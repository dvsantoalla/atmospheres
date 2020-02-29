import json
import logging as log
import os

import data.constants as c

"""
Load data with the specified parameters. Can use the ATMOSPHERES_DATADIR environment
variable to override the default value if the "datadir" option is not specified
"""


def get(parameter, location=None, lat=None, lon=None, date=None, time="0000", dataset="10days", datatype="hres",
        datadir=None):

    if datadir is None:
        datadir = os.environ.get("ATMOSPHERES_DATADIR", "../atmospheres-misc/data")

    data = {}
    files = os.listdir(datadir)
    log.debug("Files found in data dir %s: %s" % (datadir, files))
    files.sort()
    for i in files:
        if i.endswith(".json"):
            bits = i.split("-")
            loc = bits[0]
            par = bits[1]
            if loc == location and par == parameter:
                log.debug("Loading data from %s, place:%s, param:%s " % (i, loc, par))
                data = json.load(open(datadir + "/" + i))[parameter][datatype]
                if parameter == c.T:
                    data = list(map(lambda x: x - 273.15, data))
                elif parameter == c.C:
                    data = list(map(lambda x: x * 8, data))
                elif parameter == c.P:
                    data = list(map(lambda x: x * 1000, data))

                minimum, maximum, avg = describe(data)
                log.debug("Loaded %s values (min:%s, max:%s, avg:%s) from file '%s', parameter:%s, location:%s " % (
                        len(data), minimum, maximum, avg, i, par, loc))
                log.debug("Loaded values are %s " % str(data))
                return data

    log.warning("Cannot find any data at %s for the parameter '%s' and location '%s'. Files found: %s", datadir, parameter,
                location, files)
    return None


def describe(data):

    log.debug(type(data))
    minimum = 1000000
    maximum = -1000000
    total = 0
    for i in data:
        if i < minimum:
            minimum = i
        if i > maximum:
            maximum = i
        total += i

    return minimum, maximum, total / len(data)
