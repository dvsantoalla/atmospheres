import notes
import concepts
import transpose
import logging as log 
from data import raised_and_normal
from itertools import cycle

def generate_cycles (scale, levels=1):
    """ Generate a list of cycles, each one of them generating a pair of (amp,note).
    There are as many cycles as levels (ie octaves) in the Shepard. 
    This function is interesting to get continuous Shepard tones, as long as we want. However
    the limitation is that we can not go back, get a previous value (cycle works like that)
    """

    extended_scale = transpose.extend(scale,levels)
    amplitudes = raised_and_normal.raised_cosine(number_of_values=len(extended_scale)-1)
    log.debug("%s amplitudes, len of scale %s " % (len(amplitudes),len(extended_scale)))
    amplitudes += [0]*(len(extended_scale)-len(amplitudes))
    result = []
    for i in range(0,len(amplitudes)):
        result.append((amplitudes[i],extended_scale[i]))
    #print "Amps and Notes %s" % result

    level_cycles = []
    for i in range(0,levels):
        c = cycle(result)
        move = i*len(scale)
        for j in range(0,move):
            c.next()
        level_cycles.append(c)
    
    return level_cycles

def generate_list(scale, length=1, levels=1):
    """ Generate a list of level cuts, with all the notes sounding at all levels at a point in time
    eg, for two levels [[(amp1_l1,note1_l1],(amp1_l2,note1_l2)],[(amp2_l1,note2_l1),(amp2_l2,note2_l2)]...]
    Length should just spread from the bottom note of the bottom octave to the top note of the top octave, with
    all overlapping tones. Should get a single uninterrupted scale at least and getting back to index 0 after n-1 should
    produce the same as generate_cycles
    """

    level_cycles = generate_cycles(scale,levels=levels)
    note_lists = []

    for i in scale*length:
        chord = []
        for c in level_cycles:
            chord.append(c.next())
        chord = sorted(chord, key=lambda note: note[1].octave*12+note[1].semitones)
        note_lists.append(chord)

    return note_lists


def generate_from_values(scale, values):
    pass

def generate_shepard_risset_glissando():
    """ This is basically the same thing but with a glissando instead of individual notes
    We will need a specific instrument that performs a glissando from the lowest to the highest note (eg C2-C5)
    As soon as the instrument reaches the next octave (eg, C3, if staring at C2) another note should be
    fired that starts at the same point (eg C2). Every glissando note should have an amplitude distribution of 
    raised cosine, peaking at the center and disappearing at the beginning and the end"""
    pass

