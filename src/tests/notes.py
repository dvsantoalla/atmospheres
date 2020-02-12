import unittest
import logging as log
from data import constants as cc
from data import get
from music import notes as n
from music import transpose as t
from music import concepts as cnc
from music import generation as gen


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

    def test_beats(self):
        beat = cnc.BEAT8_LEVELS
        for i in range(0, len(beat)+1):
            log.debug("Level %s, instruments %s" % (i, gen.get_rhythm_level(beat, i)))
