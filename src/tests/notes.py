import unittest
import logging as log
from data import constants as cc
from data import get
from music import notes as n
from music import transpose as t
from music import concepts as cnc
from music import generation as gen
from csound import mikelson_drums as mkdrums


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

    def get_all_beats(self):
        result = []
        beat = cnc.BEAT8_LEVELS
        for i in range(0, len(beat) + 1):
            bar = gen.get_rhythm_level(beat, i)
            log.debug("Level %s, instruments %s" % (i, bar))
            result.append(bar)
        return result

    def test_drums(self):
        output = ""
        bars = self.get_all_beats()
        time_count = 0
        inner_step = 0
        step = 0.25
        for b in bars:
            log.debug("Generating bar %s" % b)
            output += "; **** Generating bar %s\n" % (b)
            for i in ["bass", "snare", "hihat"]:
                data = b.get(i, [])
                output += "; generating instrument '%s' bar %s \n" % (i, data)
                gen_instr, gen_note = mkdrums.get_drum_function(i)
                if len(data) > 0:
                    inner_step = 0
                    for note in data:
                        if note == 1:
                            output += gen_note(start=time_count + inner_step) + '\n'
                        inner_step += step
            time_count += inner_step
        log.info(output)
