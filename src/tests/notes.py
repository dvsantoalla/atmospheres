import unittest
import logging as log
from data import constants as cc
from data import get
from data import plot as plt
from music import notes as n
from music import transpose as t
from music import concepts as cnc
from music import generation as gen
from music import rhythms as rhy
from csound import mikelson_drums as mkdrums
from csound import output

class TestNotes(unittest.TestCase):

    def notest_notes_following_spline(self):
        """ Generate a stream of notes from a extended scale
        that follow the movement of one or several parameters"""
        gen.get_notes_following_spline(get(cc.T, location='Madrid'), cc.T, cnc.SCALES["major"], n.find("D"))

    def notest_transpose(self):

        for i in (n.find("D"), n.find("B")):
            c = n.find("A").clone()
            log.debug("=" * 20)
            log.debug("Original %s" % c)
            t.transpose([c], i)
            log.debug("Transposed %s sem: %s" % (i, c))

        for i in (n.find("A"), n.find("E"), n.find("C")):
            c = n.find("B").clone()
            log.debug("=" * 20)
            log.debug("Original %s" % c)
            t.transpose([c], i)
            log.debug("Transposed %s sem: %s" % (i, c))

        major = cnc.SCALES["major"]
        stream = []
        for i in range(-3, 2):
            for j in major:
                stream.append(t.extend([j.clone()], i))

        log.debug(stream)

    def notest_drums_range(self):

        instr, score, headers = rhy.generate_drums()
        output.write_and_play(output.get_csd(instr, score, headers=headers))


    def test_drums_following_data(self):

        place = "Madrid"
        mad2t = get(cc.W, location=place)
        plt.plot_test_multi([mad2t])
        instr, score, headers = rhy.generate_drums(data=mad2t, range=(0, 10))
        output.write_and_play(output.get_csd(instr, score, headers=headers))

