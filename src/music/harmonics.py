# Ideas
# https://en.wikipedia.org/wiki/Harmonic_series_(music)
# Interval strength (David Cope) https://en.wikipedia.org/wiki/Interval_(music)#Consonant_and_dissonant

import numpy as np

def generate_notes_from_harmonic_series(fundamental=110):

    equal = []
    harmonics = []
    num_harmonics = 25
    for i in range(0, num_harmonics):
        harmonics.append(fundamental * (i + 1))

    #print harmonics
    octaves = np.sqrt(num_harmonics)
    #print "Generated %s octaves of harmonics" % octaves

    # scalestep = 100 / 12.0
    base = np.longdouble(2.0)
    exponent = np.longdouble(1.0) / np.longdouble(12.0)
    # base = 2.0
    # exponent = 1.0/12.0
    scalefactor = base ** exponent

    #print type(base), base
    #print type(exponent), exponent
    #print type(scalefactor), scalefactor

    for octave in range(0, int(octaves)):
        scale = []
        for i in range(0, 12):
            scale.append(fundamental * (2 ** octave) * (scalefactor ** i))
        equal.append(scale)

    nharm = 1
    notes = []
    for h in harmonics:
        #print "Looking up (%s) %s" % (nharm, h)
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

        #print "Closest value (diff %s) is %s, octave %s, note %s" % (tdiff, equal[octave][note], octave, note)
        notes.append((octave, note))
        nharm += 1

    return notes
