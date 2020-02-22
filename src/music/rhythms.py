import logging as log
import music.concepts as c


def get_rhythm_level(beat, level):

    if level >= len(beat) + 1:
        log.debug("We cannot get rhythm level %s from beat, as there are only %s levels" % (level, len(beat)))
        return None
    # Set initial empty values
    result = {}
    for i in c.DINSTR:
        result[i] = []
    for i in range(0, level):
        level_beat = beat[i]
        for k in level_beat.keys():
            result[k] = c.expand_rhythm(level_beat[k])

    return result


def get_rhythm_sequence(beat, levels):

    result = []
    for i in levels:
        result.append(get_rhythm_level(beat, i))
    return result