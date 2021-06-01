import logging as log

from csound import output
from data import get
from studios import Studio
from music import harmonics as harm
from music import rhythms as rhy
from data import constants as cc
from data import spline as sp
from data import plot as plt



class Studio02(Studio):
    """
    This studio takes climate data, single variable,
    """

    def play(self):

        self.wave_following_data(plot=True)

    @staticmethod
    def wave_following_data(plot=False):

        # ****** HARMONICS ***********

        # data1 = get(cc.T, location='Madrid')
        temp = get(cc.T, collection='Pieces/Piece01')
        log.debug("Read %s data elements" % len(temp))
        # Every data element has two components
        data1, data2 = list(map(lambda x: x[0], temp)), list(map(lambda x: x[1], temp))
        min1, min2 = min(data1), min(data2)
        max1, max2 = max(data1), max(data2)
        globalmin = min1 if min1 < min2 else min2
        globalmax = max1 if max1 > max2 else max2
        log.debug("Minimum value from all data is %s" % globalmin)
        # Move the data so that it is based on zero as the min value
        data1, data2 = [x - globalmin for x in data1], [x - globalmin for x in data2]
        # Interpolation functions
        f1 = sp.generate_spline(data1, step=10)
        f2 = sp.generate_spline(data2, step=10)

        harmonics = harm.reduce_harmonics(
            harm.generate_notes_from_harmonic_series(transpose_octaves=3, num_harmonics=50), starting_octave=5)
        log.debug("Notes from harmonics %s" % harmonics)
        harmonics = harm.add_amplitudes_to_reduced_harmonics(harmonics, repeated_octave_amplitude_factor=.85)
        log.debug("Notes and amplitudes from harmonics %s" % harmonics)

        instr, score = harm.sound_harmonics_from_data(harmonics, data1, volume=40,
                                                      value_range=[0, globalmax - globalmin])
        csd = output.get_csd(instr, score)
        if plot:
            plt.plot_score(score)

        output.write_and_play(csd)

        interp_data1 = []
        interp_data2 = []
        for i in range(0, (len(data1) - 1) * 10):
            interp_data1.append(f1(i))
            interp_data2.append(f2(i))

        if plot:
            plt.plot_test_multi([interp_data1, interp_data2])

        log.info(data1)
        log.info(data2)