# Ideas
# https://en.wikipedia.org/wiki/Harmonic_series_(music)
# Interval strength (David Cope) https://en.wikipedia.org/wiki/Interval_(music)#Consonant_and_dissonant

import logging as log

import numpy as np
from csound import orchestra as orc
from data import spline as sp


def generate_notes_from_harmonic_series(fundamental=110, transpose_octaves=0, num_harmonics=25):
    equal = []
    harmonics = []
    for i in range(0, num_harmonics):
        harmonics.append(fundamental * (i + 1))

    # print harmonics
    octaves = np.sqrt(num_harmonics)
    # print "Generated %s octaves of harmonics" % octaves

    # scalestep = 100 / 12.0
    base = np.longdouble(2.0)
    exponent = np.longdouble(1.0) / np.longdouble(12.0)
    # base = 2.0
    # exponent = 1.0/12.0
    scalefactor = base ** exponent

    # print type(base), base
    # print type(exponent), exponent
    # print type(scalefactor), scalefactor

    for octave in range(0, int(octaves)):
        scale = []
        for i in range(0, 12):
            scale.append(fundamental * (2 ** octave) * (scalefactor ** i))
        equal.append(scale)

    nharm = 1
    notes = []
    for h in harmonics:
        # print "Looking up (%s) %s" % (nharm, h)
        diff = np.longdouble(999999.0)
        tdiff = 0
        octave = 0
        note = 0
        for oidx in range(0, len(equal)):
            for nidx in range(0, 12):

                localdiff = abs(equal[oidx][nidx] - h)
                # print "Comparing %s.%s, h: %s, note: %s, diff %s" % (oidx,nidx,h,equal[oidx][nidx] ,localdiff)
                if localdiff < diff:
                    octave = oidx
                    note = nidx
                    diff = localdiff
                    tdiff = equal[oidx][nidx] - h

        # print "Closest value (diff %s) is %s, octave %s, note %s" % (tdiff, equal[octave][note], octave, note)
        notes.append((octave, note))
        nharm += 1

    notes = [(x[0] + transpose_octaves, x[1]) for x in notes]
    log.debug("Returning notes %s, transposed %s" % (notes, transpose_octaves))
    return notes


def reduce_harmonics(harms, starting_octave=0):
    reduced = []
    octaves_for_semitone = {key: [starting_octave] for key in range(0, 12)}
    for o, s in harms:
        octave = octaves_for_semitone[s][-1]
        octaves_for_semitone[s].append(octave + 1)
        reduced.append((octave, s))
    return reduced

def add_amplitudes_to_reduced_harmonics(harms, start_amplitude=1, repeated_octave_amplitude_factor=1):
    reduced_with_amplitudes = []
    for o, s in harms:
        count = 0.0
        for o1, s1 in harms:
            if o1 == o and s1 == s:
                break
            elif s1 == s:
                count += 1
        reduced_with_amplitudes.append((o, s, start_amplitude * pow(repeated_octave_amplitude_factor, count)))
    return reduced_with_amplitudes



def sound_harmonics_from_data(harmonics, data, step=1, instrument_number=1, value_range=[0, 40], volume=20):
    end_of_piece = len(data) * step
    rng = value_range

    notes_per_harmonic = []
    # ylines = [0]

    log.info("The number of data points is %s, number of harmonics is %s, value range is %s" %
             (len(data), len(harmonics), rng))
    harm_step = (rng[1] - rng[0]) / float(len(harmonics))
    for i in np.arange(rng[0], rng[1], harm_step):
        log.debug("Getting roots for step %s" % i)
        # ylines.append(i)
        f = sp.generate_spline([x - i for x in data], step=step)
        d = f.derivative()
        roots = f.roots()
        values = [(x, d(x)) for x in roots]
        notes_per_harmonic.append((i, values))
        log.debug("For level %s, roots %s" % (i, values))
        # p = plt.plot_test_multi([[x - i for x in data]], additional_ys=ylines)

    score = [";f1 0 16384 10 1 ; Sine wave",
             "f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth",
             "f3 0 16384 10 1 0   0.3 0    0.2 0     0.14 0     .111   ; Square",
             "f4 0 16384 20 2 1 ; Hanning window",
             "f5 0 16384 8  0 2048 1 2048 3 2048 4 2048 5 2048 4 2048 5 2048 4 2048 0 ; Spline"
             ]

    bottom = True
    harm_idx = 0
    for n in notes_per_harmonic:
        prev_cut_x = 0
        note = harmonics[harm_idx]
        log.debug("Generating notes for harmonic at 'y' value %s, note %s" % (n[0], note))
        cuts = n[1]
        amplitude = float(volume) * note[2]
        if len(cuts) == 0 and bottom:
            log.debug("** Generating full note, for all the duration of the piece, still below the values")
            log.debug("** (%s) from %s to %s, length: %s" % (note, 0, end_of_piece, end_of_piece))
            score.append("i%s %s %s %s %s.%02d ; Generating full note" % (instrument_number, 0, end_of_piece,
                                                                          amplitude, note[0], note[1]))
        else:
            bottom = False
            for cut, derivative in cuts:
                if derivative >= 0:
                    prev_cut_x = cut
                else:
                    log.debug("** (%s) from %s to %s, length: %s" % (note, prev_cut_x, cut, cut - prev_cut_x))
                    score.append(
                        "i%s %s %s %s %s.%02d" % (instrument_number, prev_cut_x, cut - prev_cut_x,
                                                  amplitude, note[0], note[1]))

            # if last derivative is positive, generate harmonic from there till the end.
            if len(cuts) > 0:
                cut, derivative = cuts[-1]
                if derivative >= 0:
                    log.debug("** (%s) from %s to %s, length: %s" % (note, cut, end_of_piece, end_of_piece - cut))
                    score.append(
                        "i%s %s %s %s %s.%02d" % (instrument_number, cut, end_of_piece - cut,
                                                  amplitude, note[0], note[1]))

        harm_idx += 1

    instr = orc.table_modulated_basic_wave(instrument_number=instrument_number, oscillator_function_number=3,
                                           modulating_function_number=5, seq_length=end_of_piece,
                                           use_function_as_envelope=True)

    return [instr], score
