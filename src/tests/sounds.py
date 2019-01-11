import unittest
from csound import output,orchestra
from csound.orchestra import gen08
from data import constants as c
from data import get

class TestSounds(unittest.TestCase):

    def test_simple_soundwaves(self):

	# Get all data

	place = "Madrid"
	mad2t = get(c.T, location=place)
	madp = get(c.P, location=place)
	madw = get(c.W, location=place)
	madc = get(c.C, location=place)

	# write orchestra + score

	duration = 30
	points = 16777216
	oscillator = orchestra.oscillator1(points)

	score = [	"f1 0 8192 10 1  ; Table containing a sine wave.", 
			gen08(2,mad2t,number_of_points=points,comment="Weather parameter table 2"),
			gen08(3,madp,number_of_points=points,comment="Weather parameter table 3",),
			gen08(4,madw,number_of_points=points,comment="Weather parameter table 4"),
			gen08(5,madc,number_of_points=points,comment="Weather parameter table 5"),
			"i1 0 %s 10000 2 ; " % duration,
			"i1 0 %s 5000 3 ; " % duration,
			"i1 0 %s 5000 4 ; " % duration,
			"i1 0 %s 5000 5 ; " % duration
		]

	output.write_and_play(output.get_csd([oscillator],score))



