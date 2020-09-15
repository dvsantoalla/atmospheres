import logging as log

import csound.mikelson_drums as mkdrums
import music.concepts as c
import music.generation as gen


def get_rhythm_level(beat, level):
    if level >= len(beat) + 1:
        log.warn("We cannot get rhythm level %s from beat, as there are only %s levels" % (level, len(beat)))
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


def get_all_beats():
    result = []
    beat = c.BEAT16_LEVELS
    for i in range(0, len(beat) + 1):
        bar = get_rhythm_level(beat, i)
        # log.debug("Level %s, instruments %s" % (i, bar))
        result.append(bar)
    return result


def generate_drums(data=None, rng=None, amplitude=30000):
    # TODO: Select Beats index from list of values and range
    bars = get_all_beats()

    score = ["f1 0 65536 10 1", "f5 0 1024 -8 1 256 1 256 .7 256 .1 256 .01"]

    time_count = 0
    inner_step = 0
    step = 0.125 / 2.0

    if data is not None and rng is not None:
        result = []
        upper = rng[1]
        lower = rng[0]
        for d in data:
            index = gen.index_for_value(d, lower, upper, 0, len(bars) - 1)
            # log.debug("Appending bar %s out of %s for value %s in range %s" % (index,len(bars),d,range))
            result.append(bars[index])
        bars = result

    # The pink noise should last all piece, to be able to mix it from the zak output channel
    len_ticks = (len(bars))
    score += ['i1     0       %s      .5      1 ; Pink noise, all piece long' % len_ticks]
    score += ['i1     0       %s      .5      2 ; Pink noise, all piece long' % len_ticks]
    instr = [mkdrums.get_pinkish_noise()]

    log.info("From %s values, the drum part has %s bars, %s beats" % (len(data), len(bars), len_ticks))
    nbar = 0
    for b in bars:
        nbar += 1
        # log.debug("Generating bar %s" % b)
        score += ["; **** Generating bar #%s: %s" % (nbar, b)]
        for i in ["bass", "snare", "hihat"]:
            data = b.get(i, [])
            score += ["; generating instrument '%s' bar %s " % (i, data)]
            gen_instr, gen_note = mkdrums.get_drum_function(i)
            if len(data) > 0:
                inner_step = 0
                for beat in data:
                    for accent in beat:
                        if accent > 0:
                            score += [gen_note(start=time_count + inner_step, amplitude=amplitude * accent, hit=accent)]
                        inner_step += step
        time_count += inner_step

    for i in ["bass", "snare", "hihat"]:
        gen_instr, gen_note = mkdrums.get_drum_function(i)
        instr.append(gen_instr())

    # log.info(score)
    return instr, score, ["zakinit	50,50	; Initialize the zak system"]
