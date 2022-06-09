import logging as log

from csound import output
from data import constants as cc
from data import get
from data import spline as sp
from music import harmonics as harm
from music import rhythms as rhy
from studios import Studio


class Studio01(Studio):
    """
    This studio takes cloud cover and wind data from Madrid,
    """

    def play(self):

        self.drums_following_data(plot=True)

    @staticmethod
    def drums_following_data(plot=False):

        # ****** HARMONICS ***********

        # data1 = get(cc.T, location='Madrid')
        data1 = get(cc.C, location='Madrid')
        harmonics = harm.generate_notes_from_harmonic_series(transpose_octaves=5)
        log.debug("Harmonics are %s" % harmonics)
        harmonics = harm.reduce_harmonics(harmonics, starting_octave=5)
        log.debug("Reduced Harmonics are %s" % harmonics)

        f1 = sp.generate_spline(data1, step=10)
        interp_data1 = []
        for i in range(0, (len(data1) - 1) * 10):
            interp_data1.append(f1(i))

        harmonics_amp = harm.add_amplitudes_to_reduced_harmonics(harmonics, repeated_octave_amplitude_factor=0.85)
        instr1, score1 = harm.sound_harmonics_from_data(harmonics_amp, interp_data1, step=1, instrument_number=55,
                                                        value_range=(min(data1), max(data1)))

        # This works
        # instr1, score1 = harm.sound_harmonics_from_data(harmonics, data1, step=10, instrument_number=55)

        # ****** DRUMS ***********

        place = "Madrid"
        data2 = get(cc.W, location=place)
        f2 = sp.generate_spline(data2, step=10)

        interp_data2 = []
        for i in range(0, (len(data2) - 1) * 10):
            interp_data2.append(f2(i))

        rng = (min(data2), max(data2))
        rng = (0, 10)
        instr2, score2, headers = rhy.generate_drums(data=interp_data2, rng=rng, amplitude=10000)

        # ***** PLOT AND RUN *************

        log.info("Plotting datasets with length %s and %s" % (len(interp_data1), len(interp_data2)))

        if plot:
            from data import plot as plt
            plt.plot_score(score1)
            plt.plot_test_multi([interp_data1, interp_data2])

        # output.write_and_play(output.get_csd(instr1, score1, headers=headers))
        # output.write_and_play(output.get_csd(instr2, score2, headers=headers))

        output.write_and_play(output.get_csd(instr1 + instr2, score1 + score2, headers=headers))
