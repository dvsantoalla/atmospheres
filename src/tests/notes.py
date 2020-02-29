import logging as log
import unittest

from csound import output
from data import constants as cc
from data import get
from data import plot as plt
from data import spline as sp
from music import concepts as cnc
from music import generation as gen
from music import harmonics as harm
from music import notes as n
from music import rhythms as rhy
from music import transpose as t


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

        # ****** HARMONICS ***********

        data1 = get(cc.T, location='Madrid')
        data1 = get(cc.C, location='Madrid')
        harmonics = harm.generate_notes_from_harmonic_series(transpose_octaves=5)
        log.debug("Harmonics are %s" % harmonics)
        harmonics = harm.reduce_harmonics(harmonics, starting_octave=5)
        log.debug("Reduced Harmonics are %s" % harmonics)

        f1 = sp.generate_spline(data1, step=10)
        interp_data1 = []
        for i in range(0, (len(data1)-1)*10):
            interp_data1.append(f1(i))

        # Thsi does not work...
        instr1, score1 = harm.sound_harmonics_from_data(harmonics, interp_data1, step=1, instrument_number=55,
                                                        range=(min(data1), max(data1)))

        # This works
        # instr1, score1 = harm.sound_harmonics_from_data(harmonics, data1, step=10, instrument_number=55)

        # ****** DRUMS ***********

        place = "Madrid"
        data2 = get(cc.W, location=place)
        f2 = sp.generate_spline(data2, step=10)

        interp_data2 = []
        for i in range(0, (len(data2)-1)*10):
            interp_data2.append(f2(i))

        instr2, score2, headers = rhy.generate_drums(data=interp_data2, range=(min(data2), max(data2)), amplitude=10000)


        # ***** PLOT AND RUN *************

        log.info("Plotting datasets with length %s and %s" % (len(interp_data1), len(interp_data2)))
        plt.plot_score(score1)
        plt.plot_test_multi([interp_data1, interp_data2])

        #output.write_and_play(output.get_csd(instr1, score1, headers=headers))
        #output.write_and_play(output.get_csd(instr2, score2, headers=headers))
        output.write_and_play(output.get_csd(instr1+instr2, score1+score2, headers=headers))

