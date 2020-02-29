import logging as log
import unittest

from csound import orchestra, output
from music import concepts as cnc
from music import shepard as shep


class TestShepard(unittest.TestCase):


    def test_shepard(self):

        scale = cnc.SCALES["major"]
        for n in scale:
            n.octave += 1

        notes = shep.generate_list(scale,length=30,levels=10)
        log.debug("Notes: %s " % (notes))

        step = 0.25
        duration = step / 2.0
        time = 1
        score = []
        for chord in notes:

            score.append("; Writing out %s" % chord)
            for note in chord:
                amp = note[0]
                pitch = "%s.%02d" % (note[1].octave,note[1].semitones)
                score.append("i1 %s %s %s %s %s  ; %s " % (time, duration, amp*5000, pitch, note))
            time += step

        score.insert(0,"f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth")
        score.insert(0,"f 1 0 16384 10 1")
        pluck = orchestra.basic_wave(instrument_number=1)
        output.write_and_play(output.get_csd([pluck], score))


        pluck = orchestra.basic_wave(instrument_number=1, function_number=2)
        output.write_and_play(output.get_csd([pluck], score))


    def test_shepard_hanning(self):

        use_index = True

        scale = cnc.SCALES["major"]
        length = 30
        levels = 10
        seq_length = len(scale) * (levels + 1)
        log.debug("Testing Hanning Shepard with a cycle (following Hanning function) length of %s" % (seq_length))

        for n in scale:
            n.octave += 1

        notes = shep.generate_list(scale, length=length, levels=levels, give_index_instead_of_amplitudes=use_index)
        log.debug("Using index to Hanning window as amplitude: %s " % use_index)
        log.debug("Notes: %s " % (notes))

        step = 0.25
        duration = step / 2.0
        time = 1
        score = []

        score.append("f 1 0 16384 10 1")
        score.append("f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth")
        score.append("f3 0 16384 20 2 1 ; Hanning window")

        if use_index:
            instr1 = orchestra.table_modulated_basic_wave(instrument_number=1, modulating_function_number=3,
                                                        seq_length=seq_length)
            instr2 = orchestra.table_modulated_basic_wave(instrument_number=1, oscillator_function_number=2,
                                                          modulating_function_number=3, seq_length=seq_length)
        else:
            instr1 = orchestra.basic_wave(instrument_number=1) # Sine wave
            instr2 = orchestra.basic_wave(instrument_number=1, function_number=2) # That is, sawtooth

        for chord in notes:

            score.append("; Writing out %s" % chord)
            for note in chord:
                amp = note[0]
                pitch = "%s.%02d" % (note[1].octave, note[1].semitones)
                if use_index:
                    # Amplitude is an index to a window function
                    score.append("i1 %s %s %s %s   ; %s " % (time, duration, amp, pitch, note))
                else:
                    # Amplitude is the "true" expected amplitude
                    score.append("i1 %s %s %s %s   ; %s " % (time, duration, amp * 5000, pitch, note))
            time += step

        # instr = orchestra.wgpluck2(instrument_number=1,krefl=0.95)
        # instr = orchestra.wgpluck(instrument_number=1)

        output.write_and_play(output.get_csd([instr1], score))
        output.write_and_play(output.get_csd([instr2], score))


 	


