import unittest
import logging as log
from data import constants as cc
from data import get
from music import notes as n
from music import transpose as t
from music import concepts as cnc
from music import generation as gen


class TestNotes(unittest.TestCase):

    def test_notes_following_spline(self):
        """ Generate a stream of notes from a extended scale
        that follow the movement of one or several parameters"""
        gen.get_notes_following_spline(get(cc.T, location='Madrid'), cc.T, cnc.SCALES["major"], n.find("D"))

    def test_transpose(self):

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
