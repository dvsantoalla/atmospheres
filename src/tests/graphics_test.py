import unittest

from data import constants as c
from data import get
from data import plot as pl


class TestGraphics(unittest.TestCase):

    def test_plotting(self):

        place = "Madrid"
        place = "Reading"
        
        mad2t = get(c.T, location=place)
        madp = get(c.P, location=place)
        madw = get(c.W, location=place)
        madc = get(c.C, location=place)

        pl.plot_test_multi([mad2t, madp, madw, madc], file="test_plotting.png")


