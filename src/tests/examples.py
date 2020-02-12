import sys
import unittest
import logging as log
import numpy as np
import data.plot as plt
import scipy.optimize as opt
from csound import output, orchestra
from csound.orchestra import gen08
from music import concepts as cnc
from music import generation as gen
from music import notes as n
from music import shepard as shep
from music import harmonics as harm
from data import constants as td
from data import get
from data import spline as sp


def notest_simple_soundwaves(osc=1, duration=30):
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
            "i3 0 %s 5000 2 3 ; " % duration,
            "i3 0 %s 5000 5 4 ; " % duration,
        ]

    score = ["f1 0 8192 10 1  ; Table containing a sine wave.",
             gen08(2, mad2t, number_of_points=points, comment="Weather parameter table 2"),
             gen08(3, madp, number_of_points=points, comment="Weather parameter table 3", ),
             gen08(4, madw, number_of_points=points, comment="Weather parameter table 4"),
             gen08(5, madc, number_of_points=points, comment="Weather parameter table 5")
             ]
    score += events

    output.write_and_play(output.get_csd([oscillator], score))


class TestHarmonics(unittest.TestCase):

    def test_harmonics(self, step=1):

        harmonics = harm.generate_notes_from_harmonic_series(transpose_octaves=5)
        log.debug("Harmonics are %s" % harmonics)
        #self.run_test_harmonics(harmonics, step=2)
        harmonics = harm.reduce_harmonics(harmonics, starting_octave=5)
        log.debug("Reduced Harmonics are %s" % harmonics)
        self.run_test_harmonics(harmonics, step=4)

    def run_test_harmonics(self, harmonics, step=1):

        data = get(td.T, location='Madrid')
        end_of_piece = len(data) * step
        rng = [0, len(data)]

        notes_per_harmonic = []
        ylines = [0]

        log.debug("The number of data points is %s, number of harmonics is %s" % (len(data), len(harmonics)))
        harm_step = (rng[1] - rng[0]) / float(len(harmonics))
        for i in np.arange(rng[0], rng[1], harm_step):
            # log.debug("Getting roots for step %s" % i)
            # ylines.append(i)
            f = sp.generate_spline([x - i for x in data], step=step)
            d = f.derivative()
            roots = f.roots()
            values = [(x, d(x)) for x in roots]
            notes_per_harmonic.append((i, values))
            # log.debug("For level %s, roots %s" % (i, values))
            #p = plt.plot_test_multi([[x - i for x in data]], additional_ys=ylines)

        score = ["f 1 0 16384 10 1 ; Sine wave",
                 "f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth",
                 "f3 0 16384 20 2 1 ; Hanning window"]

        bottom = True
        harm_idx = 0
        for n in notes_per_harmonic:
            prev_cut_x = 0
            note = harmonics[harm_idx]
            log.debug("Generating notes for harmonic at 'y' value %s, note %s" % (n[0], note))
            cuts = n[1]
            if len(cuts) == 0 and bottom:
                log.debug("** Generating full note, for all the duration of the piece, still below the values")
                score.append("i1 %s %s 20 %s.%02d ; Generating full note" % (0, end_of_piece, note[0], note[1]))
            else:
                bottom = False
                for cut, derivative in cuts:
                    if derivative >= 0:
                        prev_cut_x = cut
                    else:
                        log.debug("** (%s) from %s to %s, length: %s" % (note, prev_cut_x, cut, cut - prev_cut_x))
                        score.append(
                            "i1 %s %s 20 %s.%02d" % (prev_cut_x, cut - prev_cut_x, note[0], note[1]))

                # if last derivative is positive, generate harmonic from there till the end.
                if len(cuts) > 0:
                    cut, derivative = cuts[-1]
                    if derivative >= 0:
                        log.debug("** (%s) from %s to %s, length: %s" % (note, cut, end_of_piece, end_of_piece - cut))
                        score.append(
                            "i1 %s %s 20 %s.%02d" % (cut, end_of_piece - cut, note[0], note[1]))

            harm_idx += 1

        instr = orchestra.table_modulated_basic_wave(instrument_number=1, oscillator_function_number=2,
                                                     modulating_function_number=3, seq_length=end_of_piece,
                                                     use_function_as_envelope=True)
        plt.plot_score(score)
        output.write_and_play(output.get_csd([instr], score))


class TestSineWavesPerParameter(unittest.TestCase):

    def notest_simple_soundwaves(self):
        test_simple_soundwaves(osc=1)


class TestSineWaveModulatedInPitchAmplitude(unittest.TestCase):
    """ Play two sine waves, modulated in pitch and amplitude. The first
    two parameters modulating pitch and amplitude of the first oscillator 
    and the second two parameters the second oscillator """

    def notest_both(self):
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

    def notest_scale_wgpluck_with_rhythm(self):
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

    def notest_short_one(self):
        test_simple_soundwaves(osc=2, duration=10)

    def notest_medium_one(self):
        test_simple_soundwaves(osc=2, duration=60)

    def notest_long_one(self):
        test_simple_soundwaves(osc=2, duration=120)


class TestShepardTones(unittest.TestCase):

    def basic_test(self, step_factor=1, step_function=None, initial_step=0.25, reverse=False,
                   step_list=None, use_step_derivative=False):

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

        score += self.generate_note_sequence(notes, initial_step=initial_step,
                                             fixed_step_factor=step_factor, step_function=step_function,
                                             step_list=step_list, use_step_derivative=use_step_derivative)

        instr = orchestra.table_modulated_basic_wave(instrument_number=1, oscillator_function_number=2,
                                                     modulating_function_number=3, seq_length=seq_length,
                                                     use_function_as_envelope=True)
        output.write_and_play(output.get_csd([instr], score))

    def generate_note_sequence(self, notes, initial_step=0.25, fixed_step_factor=1, step_function=None,
                               step_list=None, use_step_derivative=False):

        step = initial_step
        time = 1
        score = []
        N = len(notes)

        log.debug("Length of NOTES %s " % N)
        if step_list is not None:
            log.debug("Length of step_list %s" % len(step_list))

        count = 0
        i = 0

        while count < N:

            # Calculate step (ie "gap" between the notes or "speed" of the progression)
            # Mode is chosen from variables fixed_step_factor, step_list, use_step_derivative
            # Three working modes
            # a) Use a constant step factor, that multiplies to the previous step
            # b) Use a step list, that substracts from the initial step
            # c) Use a step derivative, that uses the increment between previous and current point values
            #       This increment is used to calculate speed

            i = count
            if fixed_step_factor is not None and not use_step_derivative and step_list is None:
                # a)
                step = step * fixed_step_factor

            elif step_list is not None:
                # b)
                step = initial_step * (1.0 - step_list[i]) + 0.1

            elif use_step_derivative:
                # c)
                increment = step_function(i) - step_function(i - 1) if i > 0 else 0.001
                step = initial_step * (1 / increment) * .01
                i += 1 if increment > 0 else -1
                log.info("value %s, increment %s, step %s, i %s" % (step_function(i), increment, step, i))

            else:
                raise ValueError("At least one of 'fixed_step_factor','step_list','step_factor_function' or \
                                    'use_step_derivative' must be used")

            # Do we use a step function, that calculates what is the next note in the sequence? In this mode
            # we can forwards or backwards in the sequence
            # Otherwise we just move to the next note in the sequence

            if step_function is not None:
                # How many notes are we generating? Length of the progression N
                # what are the highest and lowest expected values of the function? ??? 0-30
                # How long is the data, n=40
                n = 40
                # Find the index of the data based on the position of "i" in the list of notes
                # Correspond the escale 0-30 for values into a true position in the notes
                index = (N - i) / n
                chord = notes[i]
            else:
                chord = notes[i]

            duration = step / 0.5

            score.append("; Writing out %s" % chord)
            for note in chord:
                pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
                score.append("i1 %s %s %s %s   ; %s " % (time, duration, note[0], pitch, note))
            time += step

            count += 1

        return score

    def generate_accelerating_note_sequence_by_segments(self, notes, number_of_steps=120,
                                                        data_values_available=40, value_function=None,
                                                        value_range=(-10, 50)):
        time = 0
        score = []
        number_of_chords_available = len(notes)
        number_of_notes_to_generate = number_of_steps

        log.debug("Length of chord list %s " % number_of_chords_available)
        log.debug("Length of values %s " % number_of_notes_to_generate)
        log.debug("Value range %s " % str(value_range))
        log.debug("Data values available %s" % str(data_values_available))
        outer_step = data_values_available / float(number_of_notes_to_generate)
        log.debug("Outer step is %s" % outer_step)

        def get_value_and_chord_index(idx):
            val = value_function(idx)  # Value at this point
            chordidx = get_chordidx_from_value(val)
            return val, chordidx

        def get_chordidx_from_value(val):
            return int((val - value_range[0]) / (value_range[1] - value_range[0]) * number_of_chords_available)

        for ni in np.arange(0, data_values_available - outer_step, outer_step):

            value0, chordindex0 = get_value_and_chord_index(ni)

            log.debug("ni0: %s, value: %s, chordindex0: %s" % (ni, value0, chordindex0))

            value1, chordindex1 = get_value_and_chord_index(ni + outer_step)
            log.debug("n(i+1): %s, value: %s, chordindex1: %s" % (ni + outer_step, value1, chordindex1))
            # log.debug("!!!!! Calculating inner step from outer: %s, chordindex0: %s to chordindex1: %s" % (
            #     outer_step, chordindex0, chordindex1))

            ## TODO: Now this bit, instead of being linear, should also use
            ## TODO:  - Gap length based on the interpolating function increases, no "inner_step"
            ## TODO:  - The number of gaps should be based in the different value of origin vs dest value

            valuegap = abs(value1 - value0)
            indexgap = outer_step

            ngapvals = int(valuegap * 10)
            ngapvals = 1 if ngapvals == 0 else ngapvals
            gapsize = indexgap / ngapvals
            log.debug("Found a gap between f(%s)-f(%s) of %s, divided into %s segments of size %s" %
                      (ni + outer_step, ni, valuegap, ngapvals, gapsize))
            nii = ni
            segmentdiff = 0
            absaccumdiff = 0
            notes_vals = []

            for ngap in np.arange(0, ngapvals):  # Every gap
                # Have to map the increment in value to gap length
                intval0 = value_function(nii)
                intval1 = value_function(nii + gapsize)
                nii += gapsize  # Move the index for this gap
                diff = intval1 - intval0
                absaccumdiff += abs(diff)
                segmentdiff += diff
                chordidx = get_chordidx_from_value(intval1)
                log.debug("gap %s: Inner diff (f(%s)-f(%s)) is %s" % (ngap, nii, nii - gapsize, diff))
                notes_vals.append((nii, diff, chordidx))

            log.debug("The segment accum diff is %s, absolute accum diff %s,  value gap is %s, error %s "
                      % (segmentdiff, absaccumdiff, valuegap, segmentdiff - valuegap))
            t = time
            for chordval in notes_vals:
                chordidx = chordval[2]
                diff = chordval[1]
                log.debug("Diff is %s, absaccumdim is %s" % (diff, absaccumdiff))
                # The duration should be the proportion of this diff from the total accumulated diff
                duration = abs(diff * outer_step) / absaccumdiff if diff != 0 and absaccumdiff != 0 else outer_step
                assert not np.isnan(duration)

                chord = notes[chordidx]
                mesg = "; ==== Intermediate time %s, duration %s, chord %s" % (t, duration, chord)
                log.debug(mesg)
                score.append(mesg)
                for note in chord:
                    amp = note[0]
                    pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
                    score.append("i1 %s %s %s %s \t; %s " % (t, duration, amp, pitch, note))
                t += duration

            # inner_step = outer_step / abs(chordindex1 - chordindex0) if chordindex0 != chordindex1 else outer_step
            # log.debug("ni %s: ** Previous Noteindex %s of %s, value %s, local step %s" %
            #          (ni, chordindex0, number_of_chords_available, value0, inner_step))

            # path = range(chordindex0 + 1, chordindex1) if chordindex0 < chordindex1 \
            #    else range(chordindex0 - 1, chordindex1, -1)

            # for iterm in path:
            #     time += inner_step
            #     log.debug("ni %s: ==== Generating intermediate note %s at time %s" % (ni, iterm, time))
            #
            #     chord = notes[iterm]
            #     score.append("; ==== Intermediate time %s chord %s" % (time, chord))
            #     for note in chord:
            #         pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
            #         score.append("i1 %s %s %s %s   ; %s " % (time, inner_step, note[0], pitch, note))

            # Generate the note at this point
            time += outer_step

            # log.debug("%s: ---- Noteindex %s of %s, value %s, time %s" %
            #           (ni, chordindex1, number_of_chords_available, value1, time))
            #
            # chord = notes[chordindex1]
            # score.append("; ---- Step %s chord %s" % (ni, chord))
            # for note in chord:
            #     pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
            #     score.append("i1 %s %s %s %s   ; %s " % (time, inner_step, note[0], pitch, note))

        return score

    def generate_accelerating_note_sequence_from_derivative(self, notes, initial_step=1,
                                                            data_values_available=40, value_function=None,
                                                            value_range=(-10, 50)):

        def get_value_and_chord_index(idx):
            val = value_function(idx)  # Value at this point
            chordidx = int((val - value_range[0]) / (value_range[1] - value_range[0]) * number_of_chords_available)
            return val, chordidx

        time = 0
        score = []
        number_of_chords_available = len(notes)

        log.debug("Length of chord list %s " % number_of_chords_available)
        log.debug("Value range %s " % str(value_range))
        log.debug("Data values available %s" % str(data_values_available))

        val_minus_one = get_value_and_chord_index(-initial_step)[0]
        val_zero = get_value_and_chord_index(0)[0]
        initial_step = 1.0 / 10.0 * abs(val_zero - val_minus_one)
        step = initial_step
        log.debug("Initial step is %s" % step)

        while True:

            log.debug("+" * 40)
            value0, chordindex0 = get_value_and_chord_index(time)
            # log.debug("-- time: %s, value0: %s, chordindex0: %s, step: %s" % (time, value0, chordindex0, step))
            time += step
            if time > data_values_available:
                break

            value1, chordindex1 = get_value_and_chord_index(time)
            step = (1.0 / (10.0 * abs(value1 - value0)) if value1 != value0 else initial_step)
            step = .5 if step > .5 else step
            step = .025 if step < .025 else step

            log.debug("@@@@ step at %s is %s" % (time, step))

            # log.debug("++ time: %s, value1: %s, chordindex1: %s, step: %s" % (time, value1, chordindex1, step))
            chord = notes[chordindex1]

            score.append("; ---- Time %s, incr: %s, chord %s" % (time, value1 - value0, chord))
            for note in chord:
                pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
                score.append("i1 %s %s %s %s   ; %s " % (time, step, note[0], pitch, note))

        return score

    def notest_simple_ascending(self):
        self.basic_test(step_factor=1)

    def notest_simple_descending(self):
        self.basic_test(reverse=True)

    def notest_simple_speeding_up(self):
        self.basic_test(step_factor=.995)

    def notest_simple_slowing_down(self):
        self.basic_test(step_factor=1.005, initial_step=0.1)

    def notest_ascending_descending_hanning(self):
        h = np.hanning(210)
        log.debug(h)
        self.basic_test(step_list=h, use_step_derivative=True)

    def notest_speeding_slowing(self):
        pass

    def notest_ascending_descending_following_data(self):
        data = get(td.T, location='Madrid')
        log.debug("The number of data points is %s" % len(data))
        f = sp.generate_spline(data)
        self.basic_test(step_function=f)

    def notest_speeding_slowing_following_data(self):
        data = get(td.W, location='Reading')
        self.run_speeding_slowing_following_data(data)
        data = map(lambda x: x * 40, np.hanning(40))
        self.run_speeding_slowing_following_data(data)

    def run_speeding_slowing_following_data(self, data, use_segments=True):

        log.debug("The number of data points is %s" % len(data))
        f = sp.generate_spline(data)

        scale = cnc.SCALES["major"]
        levels = 10
        seq_length = len(scale) * (levels + 1)
        log.debug("Testing Hanning Shepard with a cycle (following Hanning function) length of %s" % (seq_length))

        for n in scale:
            n.octave += 1

        notes = shep.generate_list(scale, length=30, levels=levels, give_index_instead_of_amplitudes=True)
        # log.debug("Using list of notes: %s" % str(notes))
        score = ["f 1 0 16384 10 1 ; Sine wave",
                 "f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth",
                 "f3 0 16384 20 2 1 ; Hanning window"]

        if not use_segments:
            score += self.generate_accelerating_note_sequence_from_derivative(notes,
                                                                              value_function=f,
                                                                              data_values_available=len(data))
        else:
            score += self.generate_accelerating_note_sequence_by_segments(notes,
                                                                          value_function=f,
                                                                          data_values_available=len(data))

        instr = orchestra.table_modulated_basic_wave(instrument_number=1, oscillator_function_number=2,
                                                     modulating_function_number=3, seq_length=seq_length,
                                                     use_function_as_envelope=True)
        plt.plot_score(score)
        output.write_and_play(output.get_csd([instr], score))
