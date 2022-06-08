import logging as log

from csound import output
from data import constants as cc
from data import get
from data import plot as plt
from data import spline as sp
from data import moving_average
from music import harmonics as harm
from studios import Studio


class Studio02(Studio):
    """
    This studio takes climate data, single variable,
    """

    def play(self):

        self.wave_following_data(plot=True)

    @staticmethod
    def wave_following_data(plot=False):

        # ****** HARMONICS ***********

        temp = get(cc.T, collection='Pieces/Piece01')
        log.debug("Read %s data elements" % len(temp))
        # Every data element has two components
        data1, data2 = list(map(lambda x: x[0], temp)), list(map(lambda x: x[1], temp))
        wdata1 = moving_average(data1, window=31)
        wdata2 = moving_average(data2, window=31)
        min1, min2 = min(wdata1), min(wdata2)
        max1, max2 = max(wdata1), max(wdata2)
        globalmin = min1 if min1 < min2 else min2
        globalmax = max1 if max1 > max2 else max2
        log.debug("Minimum value from all data is %s" % globalmin)

        # Interpolation functions
        f1 = sp.generate_spline(wdata1, step=10)
        f2 = sp.generate_spline(wdata2, step=10)
        plt.plot_test_multi([data1, wdata1])
        plt.plot_test_multi([data2, wdata2])

        # Move the data so that it is based on zero as the min value
        wdata1, wdata2 = [x - min1 for x in wdata1], [x - min2 for x in wdata2]
        harmonics = harm.reduce_harmonics(
            harm.generate_notes_from_harmonic_series(transpose_octaves=3, num_harmonics=50), starting_octave=5)
        #log.debug("Notes from harmonics %s" % harmonics)
        # repeated_octave_amplitude_factor=1.85 generates quite a bit of distortion/overdrive but sounds cool
        # repeated_octave_amplitude_factor=0.85 is safe (but boring ;) )
        harmonics = harm.add_amplitudes_to_reduced_harmonics(harmonics, repeated_octave_amplitude_factor=0.85)
        #log.debug("Notes and amplitudes from harmonics %s" % harmonics)

        instr, score = harm.sound_harmonics_from_data(harmonics, wdata1, volume=30,
                                                      value_range=[0, max1 - min1], reverb_length=1.5, reverb_mix=0.15)
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