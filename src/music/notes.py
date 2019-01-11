OCTAVE=3


class Note():

	def __init__(self,name,semitones,octave=OCTAVE):
		if len(name)==2:
			self.alteration = name[1]
		else:
			self.alteration = ""
		self.name = name[0]
		self.octave = octave
		self.semitones = semitones


	def clone(self):
		return Note(self.name+self.alteration,self.semitones,octave=self.octave)

	def __repr__(self):
		return "%s%s (%s.%s)" % (self.name,self.alteration,self.octave,self.semitones)

def calculate_note_semitones(initial, semitones=0):
	result = initial
	semis = initial + semitones
	result = (semis % 12) 
	#print "Calculating note %s + %s semitones = %s" % (initial, semitones, result)
	return result 

def generate_octaves(note_group, start, end):
	output = note_group
	for i in range(start,end):
		output += map(lambda x:x.octave)		
	return note_group

def get_note(semitones=None, name=None, alteration=""):

	for i in NOTES:
		if (semitones is None or i.semitones == semitones) and \
			(name is None or i.name==name) and \
			(alteration is None or i.alteration==alteration):
			#print "get_note(semitones=%s, name=%s, alteration=%s => %s" % (semitones,name,alteration,i)
			return i	
	#print "get_note(semitones=%s, name=%s, alteration=%s => NOT FOUND" % (semitones,name,alteration)
	return None 


def find(name_and_alteration):
	name = name_and_alteration[0]
	if len(name_and_alteration)==2:
		alteration = name_and_alteration[1]
	else:
		alteration = ""
	return get_note(name=name, alteration=alteration)

NOTE_NAMES = ["C","D","E","F","G","A","B"]
NOTES=[
	Note("Cb",11), Note("C",0), Note("C#",1),
	Note("Db",1), Note("D",2), Note("D#",3),
	Note("Eb",3), Note("E",4), Note("E#",5),
	Note("Fb",4), Note("F",5), Note("F#",6),
	Note("Gb",6), Note("G",7), Note("G#",8),
	Note("Ab",8), Note("A",9), Note("A#",10),
	Note("Bb",10), Note("B",11), Note("B#",0)
]


