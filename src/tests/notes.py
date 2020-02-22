import unittest
import logging as log
from data import constants as cc
from data import get
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

    def get_all_beats(self):
        result = []
        beat = cnc.BEAT8_LEVELS
        for i in range(0, len(beat) + 1):
            bar = rhy.get_rhythm_level(beat, i)
            log.debug("Level %s, instruments %s" % (i, bar))
            result.append(bar)
        return result

    def test_drums(self):

        bars = self.get_all_beats()

        score = ["f1 0 65536 10 1", "f5 0 1024 -8 1 256 1 256 .7 256 .1 256 .01"]
        # The pink noise should last all piece, to be able to mix it from the zak output channel
        len_ticks = (len(bars)-1)*2
        score += ['i1     0       %s      .5      1 ; Pink noise, all piece long' % len_ticks]
        score += ['i1     0       %s      .5      2 ; Pink noise, all piece long' % len_ticks]
        instr = [mkdrums.get_pinkish_noise()]

        time_count = 0
        inner_step = 0
        step = 0.125
        log.debug("The piece has %s bars, %s beats" % (len(bars), len_ticks))
        for b in bars:
            log.debug("Generating bar %s" % b)
            score += ["; **** Generating bar %s\n" % (b)]
            for i in ["bass", "snare", "hihat"]:
                data = b.get(i, [])
                score += ["; generating instrument '%s' bar %s \n" % (i, data)]
                gen_instr, gen_note = mkdrums.get_drum_function(i)
                if len(data) > 0:
                    inner_step = 0
                    for beat in data:
                        for accent in beat:
                            if accent > 0:
                                score += [gen_note(start=time_count + inner_step, amplitude=30000*accent) + '\n']
                            inner_step += step
            time_count += inner_step

        for i in ["bass", "snare", "hihat"]:
            gen_instr, gen_note = mkdrums.get_drum_function(i)
            instr.append(gen_instr())

        log.info(score)
        output.write_and_play(output.get_csd(instr, score, headers=["zakinit	50,50	; Initialize the zak system"]))

