import matplotlib.pyplot as plt
from spline import generate_spline
import random
import logging as log


def plot_test_multi(datasets, step=1, file=None, additional_ys=[], show=True):

    for yvals in datasets:
        #log.debug("yvals %s" % yvals)
        s = generate_spline(yvals, step=step)
        x = []
        for i in range(0, (len(yvals) - 1) * step):
            for j in range(0, 5):
                x.append(i + j * .2)

        y = s(x)
        plt.plot(x, y)
        for yy in additional_ys:
            plt.plot(x, [yy]*len(x))

    if file:
        plt.savefig(file)
    elif show:
        plt.show()
    else:
        return plt


def plot_score(score):

    data = []
    for line in score:
        if line.strip().startswith("i"):
            bits = line.split()
            log.debug(bits)
            start = float(bits[1])
            duration = float(bits[2])
            amplitude = float(bits[3])
            note = bits[4].split(".")
            noteval = int(note[0])*12 + int(note[1])

            data.append((start,start+duration))
            data.append((noteval,noteval))
            #data.append("r") # follow amplitude?


    plt.plot(*data, linewidth=1)
    plt.show()




def test():
    x = [x * 6 for x in range(0, 10 * 4)]
    s1 = generate_spline([random.random() * 10 for i in x], step=6)
    s2 = generate_spline([random.random() * 20 for i in x], step=6)
    s3 = generate_spline([random.random() * 30 for i in x], step=6)

    a = []
    for i in range(0, 230):
        for j in range(0, 5):
            a.append(i + j * .2)

    b1 = s1(a)
    b2 = s2(a)
    b3 = s3(a)

    # plt.step(x,y1)
    plt.plot(a, b1)
    plt.plot(a, b2)
    plt.plot(a, b3)
    # plt.plot(x,y1,':')
    # plt.plot(x,y2,':')
    # plt.plot(x,y3,':')

    # plt.savefig("pepe.png")

    plt.show()
