from notes import *
from transpose import transpose, extend

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
