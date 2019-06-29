import logging as log
import data.constants as cc
import data.spline as s
import music.transpose as t


def get_notes_following_spline(dataset,parameter_name, scale, starting_note, octave_adjust=0, step=6):
        """ Generate a stream of notes from a extended scale
        that follow the movement of one or several parameters
        octave_adjust: Tranpose this number of octaves
        step: Number of notes by original data value"""

        mad2t = dataset
        log.debug("Loaded data for spline %s" % mad2t)

        # Temperature vs Music Range
        # -30/+50 -> From Octave 0 to Octave 9

        d_major = t.transpose(scale,starting_note)
        d_major_note_range = t.extend(d_major, 5, transpose=True)
        for i in d_major_note_range:
            i.octave += octave_adjust

        f1 = s.generate_spline(mad2t, step=step)
        upper_range = cc.RANGES[parameter_name][1]
        lower_range = cc.RANGES[parameter_name][0]
        notes = []
        for i in range(0,(len(mad2t)-1)*step+1):
                note = note_for_value(f1(i),lower_range,upper_range,d_major_note_range)
                #print "X:%s, Y:%s, \tNote:%s" % (i,f1(i),note)
                notes.append(note)
        return notes

def get_events_following_spline(dataset,parameter_name, list_of_events, step=6):

        mad2t = dataset

        f1 = s.generate_spline(mad2t,step=step)
        upper_range = cc.RANGES[parameter_name][1]
        lower_range = cc.RANGES[parameter_name][0]
        events = []
        for i in range(0,(len(mad2t)-1)*step+1):
                event_idx = index_for_value(f1(i),lower_range,upper_range,0,len(list_of_events)-1)
                event = list_of_events[event_idx]
                #print "X:%s, Y:%s, \tNote:%s" % (i,f1(i),note)
                events.append(event)
        return events


def note_for_value(value, lower_range, upper_range, scale):

        nnotes = len(scale)
        note_pos = index_for_value(value,lower_range,upper_range,0,nnotes)
        if note_pos>(nnotes-1):
            log.error("ERROR: Note index for %s is %s, while max is %s" % (value, note_pos, nnotes-1))
            note_pos = nnotes-1
        return scale[note_pos]

def index_for_value(value, lower_value_range, upper_value_range, lower_index, upper_index):

        rng = upper_value_range - lower_value_range
        indices = upper_index - lower_index
        norm_value = value - lower_value_range
        return int(norm_value * indices / rng + lower_index)


