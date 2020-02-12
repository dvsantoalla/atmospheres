import unittest
import logging as log
from studios import Studio

from music import concepts as cnc
from music import shepard as shep
from csound import orchestra, output


class Studio01(Studio):

    def play(self):
    
        scale = cnc.SCALES["major"]
        for n in scale:
            n.octave += 2
    
        notes =  shep.generate_list(scale,length=30,levels=10)
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
                score.append("i1 %s %s %s %s   ; %s " % (time, duration, amp*5000, pitch, note))
            time += step

        #pluck = orchestra.wgpluck2(instrument_number=1,krefl=0.95)
        #pluck = orchestra.wgpluck(instrument_number=1)
        score.insert(0,"f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth")
        score.insert(0,"f 1 0 16384 10 1")
        pluck = orchestra.basic_wave(instrument_number=1)
        output.write_and_play(output.get_csd([pluck], score))
    
    
        pluck = orchestra.basic_wave(instrument_number=1, function_number=2)
        output.write_and_play(output.get_csd([pluck], score))




