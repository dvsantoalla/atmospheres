from music.notes import *

# Load up all notes from the NOTES array in the notes module
# exec(foo + " = 'something else'")
# Or even better, just load up the notes first
C = find("C")
D = find("D")
E = find("E")
F = find("F")
G = find("G")
A = find("A")
B = find("B")
Eb = find("Eb")
Gb = find("Gb")
Gs = find("G#")
Bb = find("Bb")

# All chords and scales can be transposed to other keys with the "notes.transpose" function

SCALES = {
    "major": [C, D, E, F, G, A, B],
    "minor": [C, D, Eb, F, G, A, Bb],
    "pentatonicminor": [C, Eb, F, G, Bb],
    "pentatonicmajor": [C, E, F, G, B]
}

CHORDS = {
    "unison": [C],
    "perfectfifth": [C, G],
    "augfifth": [C, Gs],
    "dimfifth": [C, Gb],
    "major": [C, E, G],
    "minor": [C, Eb, G]
}

STABILITY_GRADIENT = [
    CHORDS["unison"],
    CHORDS["perfectfifth"],
    CHORDS["major"],
    SCALES["pentatonicmajor"],
    SCALES["major"],
    SCALES["pentatonicminor"],
    SCALES["minor"],
    CHORDS["dimfifth"],
    CHORDS["augfifth"]
]

# Stable to unstable rhythm subdivisions over a crotchet beat
# We should offer other bases here, eg over two quavers, over 
# a triplet over a fiver, seven, semiquavers, etc
RHYTHM_STABILITY = [1, 2, 4, 8, 3, 5, 7]

#
# Drum beats with increasing levels of complexity according to
# to the layer of sound
#

DBD = 'bass'
DSN = 'snare'
DHI = 'hihat'
DCY = 'cymbal'

DINSTR = [DBD, DSN, DHI, DCY]

# Each successive level only records whatever is different from the
# previous, empty meaning the instrument does not sound
# All these beats are based in a pattern of 16 notes per bar
# A zero means no sound (default), a number>0 represents the volume

BEAT16_LEVELS = [
    {
        DBD: [[.1, 0, 0, 0], [0], [0], [0]]
    },
    {
        DBD: [[.250, 0, 0, 0], [0], [0], [0]]
    },
    {
        DBD: [[.5, 0, 0, 0], [0], [0], [0]]
    },
    {
        DBD: [[.75, 0, 0, 0], [0], [0], [0]]
    },
    {
        DBD: [[1, 0, 0, 0], [0], [0], [0]]
    },
    {
        DBD: [[1, 0, 0, 0], [0]]
    },
    {
        DBD: [[1, 0, 0, 0], [0, 0, .75, 0]]
    },

    {
        DBD: [[1, 0, 0, 0], [0, 0, .75, 0]],
        DSN: [[0, 0, 0, 0], [1, 0, 0, 0]]
    },
    {
        DHI: [[1, 0, 0, 0]]
    },
    {
        DCY: [[1, 0, 0, 0], [0], [0], [0]]
    },
    {
        DSN: [[0], [1, 0, .75, 0]]
    },
    {
        DHI: [[.75, 0, .5, 0]]
    },
    {
        DBD: [[1, 0, .9, 0], [0, 0, .8, 0]]
    },
    {
        DSN: [[0, 0, .75, 0], [1, 0, .6, 0]]
    },
    {
        DSN: [[0, 0, .8, 0], [1, 0, .75, .5], [0, 0, .8, 0], [1, .5, 1, .75]]
    },
    {
        DBD: [[1, 0, .8, 0], [0, 0, .75, 0], [1, 0, .75, 0], [0, 0, 0, 0]],
        DSN: [[0, 0, 0, 0], [1, 0,  0, .75], [0, .75, 0, 0], [1, 0, 0, 0]]
    },
    {
        DBD: [[1, 0, .8, 0], [0, 0, .75, 0], [1, 0, .75, 0], [0, 0, 0, 0]],
        DSN: [[0, 0, 0, 0], [1, 0,  0, .75], [0, .75, 0, 0], [1, 0, .8, .60]]
    },
    {
        DBD: [[1, 0, .8, 0], [0, 0, .75, 0], [1, 0, .75, 0], [0, 0, 0, 0]],
        DSN: [[0, 0, 0, 0], [1, 0, 0, .75], [0, .75, 0, 0], [1, 0, .8, .60]]
    },
    {
        DBD: [[1, 0, .75, 0], [0, 0, .75, 0]],
        DSN: [[0, .75, 0, 0], [1, 0, .0, .75]]
    },
    {
        DBD: [[1, 0, .75, 0], [0, 0, .75, 0]],
        DSN: [[0, .75, 0, 0], [1, 0, .0, .75]]
    },
    {
        DBD: [[1]],
    },
    {
        DBD: [[1]],
    },

]


def expand_rhythm(beat):
    """ Always return 4 bars of 4 notes each for a total of 16 notes"""

    beat = list(map(lambda x: expand_bar(x), beat))
    missing = 4-len(beat)
    if missing == 1:
        return beat.append(beat[2])
    elif missing == 2:
        return beat + [beat[0], beat[1]]
    elif missing == 3:
        return beat + [beat[0]] * 3
    elif missing == 4:
        return [[0] * 4] * 4
    else:
        return beat[0:4]


def expand_bar(bar):
    """ Expand a bar into 4 notes """
    missing = 4-len(bar)
    # log.debug("Expanding bar %s, missing %s elements" % (bar,missing))
    if missing == 1:
        return bar.append(bar[2])
    elif missing == 2:
        return bar + [bar[0], bar[1]]
    elif missing == 3:
        return bar + [bar[0]]*3
    elif missing == 4:
        return [0] * 4
    else:
        return bar[0:4]
