import unittest
import logging as log
from csound import output, orchestra
from csound.orchestra import gen08
from music import concepts as cnc
from music import generation as gen
from music import notes as n
from music import shepard as shep
from data import constants as td
from data import get


def test_simple_soundwaves(osc=1, duration=30):
    """ Play a sine wave for each of the parameters of Madrid in 2014. Depending on the osc parameter
    1: Play four sine waves following each of 2t, p, w, c
    2: Play two sine waves, modulated in frequency and amplitude, the first by 2t and w, the second by p and c
    3: Play two sine waves, each consisting in two oscillators with a base frequency controlled py t or c, where the 
         second oscillator of the instruments is p or w cycles off the main oscillator
    """

    # Get all data

    loc = "Madrid"
    mad2t = get(td.T, location=loc)
    madp = get(td.P, location=loc)
    madw = get(td.W, location=loc)
    madc = get(td.C, location=loc)

    # write orchestra + score

    points = 16777216
    if osc == 1:
        oscillator = orchestra.oscillator1(points, instrument_number=1)
        events = [
            "i1 0 %s 10000 2 ; " % duration,
            "i1 0 %s 5000 3 ; " % duration,
            "i1 0 %s 5000 4 ; " % duration,
            "i1 0 %s 5000 5 ; " % duration
        ]
    elif osc == 2:
        oscillator = orchestra.oscillator2(points, instrument_number=2)
        events = [
            "i2 0 %s 10000 2 4; " % duration,
            "i2 0 %s 10000 3 5; " % duration,
        ]

    elif osc == 3:
        oscillator = orchestra.oscillator_dual(points, instrument_number=3)
        events = [
            "i3 0 %s 10000 2 3 ; " % duration,
            "i3 0 %s 10000 5 4 ; " % duration,
        ]

    score = ["f1 0 8192 10 1  ; Table containing a sine wave.",
             gen08(2, mad2t, number_of_points=points, comment="Weather parameter table 2"),
             gen08(3, madp, number_of_points=points, comment="Weather parameter table 3", ),
             gen08(4, madw, number_of_points=points, comment="Weather parameter table 4"),
             gen08(5, madc, number_of_points=points, comment="Weather parameter table 5")
             ]
    score += events

    output.write_and_play(output.get_csd([oscillator], score))


class TestSineWavesPerParameter(unittest.TestCase):

    def test_simple_soundwaves(self):
        test_simple_soundwaves(osc=1)


class TestSineWaveModulatedInPitchAmplitude(unittest.TestCase):
    """ Play two sine waves, modulated in pitch and amplitude. The first
    two parameters modulating pitch and amplitude of the first oscillator 
    and the second two parameters the second oscillator """

    def test_both(self):
        test_simple_soundwaves(osc=2)


class TestSineWaveWithModulatedDetune(unittest.TestCase):
    """ In this case there will be two sine waves with a pitch following a parameter. A second parameter
    will control how much is the second sine wave detuned in relation to the first, creating a "beat" between both.
    We have to see how a parameter should translate into "beat" as closer waves can sound more "unstable" that two further away"""

    def test_modulated_dissonance(self):
        test_simple_soundwaves(osc=3)


class TestPlucksInScale(unittest.TestCase):

    def no_test_scale_wgpluck2(self):
        """ wgpluck seems to sound a bit better, so let's mothball this for a while"""

        notes = gen.get_notes_following_spline(get(td.T, location='Madrid'), td.T, cnc.SCALES["major"], n.find("D"))
        plucker = orchestra.wgpluck2(instrument_number=1)
        score = []
        for i in range(0, len(notes)):
            score.append("i1 %s 1.25 30000 %s.%02d" % (i, notes[i].octave, notes[i].semitones))
        output.write_and_play(output.get_csd([plucker], score))

    def no_test_scale_wgpluck(self):
        notes = gen.get_notes_following_spline(get(td.T, location='Madrid'), td.T, cnc.SCALES["major"], n.find("D"))
        plucker = orchestra.wgpluck(instrument_number=1, function_number=1)
        score = [
            "f 1 0 16384 10 1"]  # wgpluck requires an excite function https://csound.github.io/docs/manual/wgpluck.html
        for i in range(0, len(notes)):
            score.append("i1 %s 1 30000 %s.%02d" % (i, notes[i].octave, notes[i].semitones))
        output.write_and_play(output.get_csd([plucker], score))

    def test_scale_wgpluck_with_rhythm(self):
        notes = gen.get_notes_following_spline(get(td.T, location='Madrid'), td.T, cnc.SCALES["major"], n.find("D"))
        rhythms = gen.get_events_following_spline(get(td.W, location='Madrid'), td.W, cnc.RHYTHM_STABILITY)

        log.debug(notes)
        log.debug(rhythms)

        plucker = orchestra.wgpluck(instrument_number=1, function_number=1)
        score = [
            "f 1 0 16384 10 1"]  # wgpluck requires an excite function https://csound.github.io/docs/manual/wgpluck.html
        for i in range(0, len(notes)):
            score.append("i1 %s 1 30000 %s.%02d" % (i, notes[i].octave, notes[i].semitones))
        output.write_and_play(output.get_csd([plucker], score))


class TestPlucksUsingIncreasinglyComplexScales(unittest.TestCase):
    """Using a plucked instrument, follow the data by going from the simplest
    harmony (eg octaves) to the most complex (eg chromatic?) as the data values increase
    Use music.concepts.STABILITY_GRADIENT to map the progress
    """

    pass


class TestRhythms(unittest.TestCase):
    """Follow the data by creating more unstable rhythms as the data values increase
    For example one could use a single beat on the 1 of a 4/4 as the simplest and most stable
    and some kind of polyrhythm for the most unstable and complex.
    Use music.concepts.RHYTHM_STABILITY to the map the progresss
    """
    pass


class TestSawToothWithFilters(unittest.TestCase):
    pass


class TestGranularSynthesis(unittest.TestCase):
    pass


class TestDifferentPieceLengths(unittest.TestCase):

    def test_short_one(self):
        test_simple_soundwaves(osc=2, duration=10)

    def test_medium_one(self):
        test_simple_soundwaves(osc=2, duration=60)

    def test_long_one(self):
        test_simple_soundwaves(osc=2, duration=120)


class TestShepardTones(unittest.TestCase):

    def basic_test(self, step_factor=1, initial_step=0.25, reverse=False):

        scale = cnc.SCALES["major"]
        levels = 10
        seq_length = len(scale) * (levels + 1)
        log.debug("Testing Hanning Shepard with a cycle (following Hanning function) length of %s" % (seq_length))

        for n in scale:
            n.octave += 1

        notes = shep.generate_list(scale, length=30, levels=levels, give_index_instead_of_amplitudes=True)
        if reverse:
            notes.reverse()
        log.debug("Notes: %s " % (notes))

        score = ["f 1 0 16384 10 1",
                 "f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth",
                 "f3 0 16384 20 2 1 ; Hanning window"]
        step = initial_step
        time = 1
        instr = orchestra.table_modulated_basic_wave(instrument_number=1, oscillator_function_number=2,
                                                     modulating_function_number=3, seq_length=seq_length)

        for chord in notes:

            step = step * step_factor
            duration = step / 2.0

            score.append("; Writing out %s" % chord)
            for note in chord:
                pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
                score.append("i1 %s %s %s %s   ; %s " % (time, duration, note[0], pitch, note))
            time += step

        output.write_and_play(output.get_csd([instr], score))

    def test_simple_ascending(self):
        self.basic_test(step_factor=1)

    def test_simple_descending(self):
        self.basic_test(reverse=True)

    def notest_simple_speeding_up(self):
        self.basic_test(step_factor=.995)

    def notest_simple_slowing_down(self):
        self.basic_test(step_factor=1.005, initial_step=0.1)

    def test_ascending_descending(self):
        pass

    def test_speeding_slowing(self):
        pass
