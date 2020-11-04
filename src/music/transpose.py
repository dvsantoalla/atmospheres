import logging as log
from itertools import cycle

from music.notes import NOTE_NAMES, calculate_note_semitones, get_note


def get_note_name_distance(a, b):
    distance = 0
    found = False
    notenames = cycle(NOTE_NAMES)

    name = next(notenames)
    while True:
        if found and name == b.name:
            return distance + 1
        elif found:
            distance += 1
        elif name == a.name:
            found = True
        name = next(notenames)


def arrange_octaves(note_list, ascending=True):
    current_octave = note_list[0].octave
    current_semis = note_list[0].semitones
    for i in note_list[1:]:
        if i.semitones < current_semis and ascending:
            i.octave = current_octave + 1
        elif i.semitones > current_semis and not ascending:
            i.octave = current_octave - 1
        else:
            i.octave = current_octave

        current_semis = i.semitones
        current_octave = i.octave
    return note_list


def transpose(scale, destination):
    """Transposes a escale to another starting with destination_first_note .
		Total transposition will be the distance from the first note of the scale to destination_first_note"""

    transposed = [destination.clone()]
    origin = scale[0]
    steps = destination.semitones - origin.semitones
    stepo = destination.octave - origin.octave
    step = stepo * 12 + steps

    log.info("Transposing %s from %s to %s, step %s" % (scale, origin, destination, step))
    notenames = cycle(NOTE_NAMES)
    while next(notenames) != destination.name:
        pass
    for i in range(1, len(scale)):
        note = scale[i]
        nextsemis = calculate_note_semitones(note.semitones, semitones=step)
        distance = get_note_name_distance(scale[i - 1], note)
        for j in range(0, distance):
            nextname = next(notenames)
            nextnote = get_note(semitones=nextsemis, name=nextname, alteration=None)
        transposed.append(nextnote.clone())

    return arrange_octaves(transposed)


def extend(scale, times, updown=False, transpose=True):
    """Extends the scale a number of times, either into different octaves or swirling up and down in the same octave """
    result = [x.clone() for x in scale]
    for i in range(0, times):
        result += [x.clone() for x in scale]
    if transpose:
        result = arrange_octaves(result)

    return result
