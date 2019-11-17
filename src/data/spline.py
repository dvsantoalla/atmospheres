import scipy.interpolate as intp
import logging as log


def generate_spline_xy(xvals, yvals):
    return intp.InterpolatedUnivariateSpline(xvals, yvals)


def generate_spline(yvals, start=0, end=None, step=1):
    """
    Create a function that interpolates all yvalues
    step is the number of xvalues per yvalue, default is one
    """
    #log.debug(yvals)
    if end is None:
        end = len(yvals)
    xvals = [x * step for x in range(0, end)]
    #log.debug("xvals %s, yvals %s" % (len(xvals), len(yvals[0:end])))
    return generate_spline_xy(xvals, yvals[0:end])
