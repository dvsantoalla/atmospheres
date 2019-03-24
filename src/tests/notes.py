import unittest
import logging as log
from pprint import pprint
from data import constants as cc
from data import get
from data import spline as s
from music import notes as n
from music import transpose as t
from music import concepts as cnc
from music import generation as gen
from music import shepard as shep
from csound import orchestra,output


class TestNotes(unittest.TestCase):

    def test_notes_following_spline(self):
        """ Generate a stream of notes from a extended scale
        that follow the movement of one or several parameters"""
        gen.get_notes_following_spline(get(cc.T, location='Madrid'),cc.T,cnc.SCALES["major"], n.find("D"))


    def test_transpose(self):

        for i in (n.find("D"), n.find("B")):
            c = n.find("A").clone()
            log.debug("=" * 20)
            log.debug("Original %s" % c)
            t.transpose([c],i)
            log.debug("Transposed %s sem: %s" % (i,c))

        for i in (n.find("A"),n.find("E"),n.find("C")):
            c = n.find("B").clone()
            log.debug("=" * 20)
            log.debug("Original %s" % c)
            t.transpose([c],i)
            log.debug("Transposed %s sem: %s" % (i,c))
 
        major = cnc.SCALES["major"]
        stream = []
        for i in range(-3,2):
            for j in major:
                stream.append(t.extend([j.clone()],i))

        log.debug(stream)


    def no_test_shepard(self):

        scale = cnc.SCALES["major"]
        for n in scale:
            n.octave += 2

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

        #pluck = orchestra.wgpluck2(instrument_number=1,krefl=0.95)
        #pluck = orchestra.wgpluck(instrument_number=1)
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
            n.octave += 2

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
            instr1 = orchestra.basic_wave(instrument_number=1)
            instr2 = orchestra.basic_wave(instrument_number=1, function_number=2)

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


 	


