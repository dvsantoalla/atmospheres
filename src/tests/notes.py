import unittest
import logging as log
from pprint import pprint
from data import constants as cc
from data import get
from data import spline as s
from music import notes as n
from music import transpose as t
from music import concepts as cnc
from music import generation as gen
from music import shepard as shep
from csound import orchestra,output


class TestNotes(unittest.TestCase):

	def notest_notes_following_spline(self):
		""" Generate a stream of notes from a extended scale
		that follow the movement of one or several parameters"""
		gen.get_notes_following_spline(get('Madrid',cc.T),cc.T,cnc.SCALES["major"], n.find("D"))


	def notest_transpose(self):

		for i in (n.find("D"), n.find("B")):
			c = n.find("A").clone()
			log.debug("=" * 20)
			log.debug("Original %s" % c)
			t.transpose([c],i)
			log.debug("Transposed %s sem: %s" % (i,c))

		for i in (n.find("A"),n.find("E"),n.find("C")):
			c = n.find("B").clone()
			log.debug("=" * 20)
			log.debug("Original %s" % c)
			t.transpose([c],i)
			log.debug("Transposed %s sem: %s" % (i,c))
 
		major = cnc.SCALES["major"]
		stream = []
		for i in range(-3,2):	
			for j in major:
				stream.append(t.extend([j.clone()],i))

	        log.debug(stream)


	def test_shepard(self):

		scale = cnc.SCALES["major"]
                for n in scale:
                    n.octave += 2

		notes =  shep.generate_list(scale,length=30,levels=10)
		log.debug("Notes: %s " % (notes))

		step = 0.25
		duration = step / 2.0
		time = 1
		score = []
		for chord in notes:
			
			score.append("; Writing out %s" % chord)
			for note in chord:
				amp = note[0]
				pitch = "%s.%02d" % (note[1].octave,note[1].semitones)
				score.append("i1 %s %s %s %s   ; %s " % (time, duration, amp*5000, pitch, note))
			time += step

		#pluck = orchestra.wgpluck2(instrument_number=1,krefl=0.95)
		#pluck = orchestra.wgpluck(instrument_number=1)
		score.insert(0,"f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth")
		score.insert(0,"f 1 0 16384 10 1")
		pluck = orchestra.basic_wave(instrument_number=1)
		output.write_and_play(output.get_csd([pluck], score))


		pluck = orchestra.basic_wave(instrument_number=1, function_number=2)
		output.write_and_play(output.get_csd([pluck], score))



 	


