import logging as log 
from math import pi,e, sqrt, cos
from matplotlib import pyplot as p
from scipy import sinc


def normal(x,mean,variance):
    return  pow(e,-(pow((x-mean),2.0) / 2.0*variance)) / sqrt(2.0*pi*variance)

def raised(x,beta,T):
    return (pi/4.0*T) * sinc(1/2.0*beta)

def raised2(t,beta,T):
    a = 1.0/T 
    b = sinc (t/T)
    c = cos((pi * beta * t) / T)
    d = 1 - pow(2.0 * beta * t / T, 2)

    #print "a:%s, b:%s, c:%s, d:%s" % (a,b,c,d)

    return a * b * (c / d)

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def raised_cosine(beta=0.01,T=1.0,number_of_values=15):

    log.debug("Generating raised cosine with beta=%s, T=%s" % (beta,T))
    xvals = []
    yvals = []
    step = 2.0 / number_of_values

    for t in frange(-1.0/T,1.0/T, step):

        xvals.append(t)
        #yvals.append(normal(x,0.0,0.00005))
        if t == (T / (2.0*beta)) or t == -(T / (2.0*beta)):
            yvals.append(raised(t,beta,T))
            log.debug( "value is constant %s " % yvals[-1])
        else:
            yvals.append(raised2(t,beta,T))

       # print "Value for %s: %s" % (t,yvals[-1])

    log.debug("Generated %s raised_cosine values: %s" % (len(yvals), yvals))
    return yvals


def plot_values(vals):

    p.plot(vals[0],vals[1])
    p.show()


#plot_raised_cosine(beta=0)
#plot_raised_cosine(beta=0.01)
#a = raised_cosine(beta=0.1)
#b = raised_cosine(beta=0.01)
#for i in range(0,len(a[0])):
#    print "%s:%s diff %s" % (a[0][i], b[0][i], a[1][i]-b[1][i])
#plot_values(raised_cosine(beta=0.000000000001))
#plot_values(raised_cosine(beta=0.1))
