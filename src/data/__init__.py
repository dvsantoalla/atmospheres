import json
import logging as log
import os

import data.constants as c


def get(parameter, location=None, lat=None, lon=None, date=None, time="0000", dataset="10days", datatype="hres",
        datadir=None, collection="Test"):
    """
    Load data with the specified parameters. Can use the ATMOSPHERES_DATADIR environment
    variable to override the default value if the "datadir" option is not specified
    """

    log.debug("Retrieving data for %s in %s (%s,%s), date:%s%s, set:%s, type:%s, collection=%s" % (parameter, location,
                                                                                    lat, lon, date, time, dataset,
                                                                                    datatype, collection))

    if datadir is None:
        datadir = os.environ.get("ATMOSPHERES_DATADIR", "../atmospheres-misc/data")

    datadir += "/"+collection

    data = {}
    files = os.listdir(datadir)
    log.debug("Files found in data dir %s: %s" % (datadir, files))
    files.sort()
    for i in files:
        if i.endswith(".json"):
            return get_meteogram_json_data(i, location, parameter, datadir, datatype)
        elif i.endswith(".csv"):
            return get_csv_data()


    log.warning("Cannot find any data at %s for the parameter '%s' and location '%s'. Files found: %s", datadir,
                parameter,
                location, files)
    return None


def get_meteogram_json_data(f, location, parameter, datadir, datatype):

    """
    :param f:
    :param location:
    :param parameter:
    :param datadir:
    :param datatype:
    :return:
    """

    bits = f.split("-")
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
            len(data), minimum, maximum, avg, f, par, loc))
        log.debug("Loaded values are %s " % str(data))
        return data


def get_csv_data():
    pass

def get_raw(file):
    f = open(file)
    data = []
    for line in f.readlines():
        items = line.split()
        if len(items) == 3:
            data.append(items[2])
        else:
            log.warning("Ignoring line, too few elements: %s" % str(items))
    return data


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
